import os
import json
os.environ["OMP_NUM_THREADS"] = "1"
from openvino.inference_engine import IECore
import onnxruntime as ort
import time
import PySimpleGUI as sg
import cv2
import numpy as np
from pythonosc import udp_client
from torchvision.transforms.functional import to_grayscale
import PIL.Image as Image
from torchvision import transforms
from threading import Thread
from one_euro_filter import OneEuroFilter


def run_model(self):
    if self.backend == "OpenVino":
        frame = cv2.resize(self.current_image_gray, (256, 256))
        # make it pil
        frame = Image.fromarray(frame)
        # make it grayscale
        frame = to_grayscale(frame)
        # make it a tensor
        frame = transforms.ToTensor()(frame)
        # make it a batch
        frame = frame.unsqueeze(0)
        # make it a numpy array
        frame = frame.numpy()
        out = self.sess.infer(inputs={self.input_name: frame})
        #out = self.sess.run([self.output_name], {self.input_name: frame})
        #end = time.time()
        output = out[self.output_name]
        output = output[0]
        output = self.one_euro_filter(output)
        for i in range(len(output)):  # Clip values between 0 - 1
            output[i] = max(min(output[i], 1), 0)
        self.output = output

    if self.backend == "ONNX":
        frame = cv2.resize(self.current_image_gray, (256, 256))
        # make it pil
        frame = Image.fromarray(frame)
        # make it grayscale
        frame = to_grayscale(frame)
        # make it a tensor
        frame = transforms.ToTensor()(frame)
        # make it a batch
        frame = frame.unsqueeze(0)
        # make it a numpy array
        frame = frame.numpy()

        out = self.sess.run([self.output_name], {self.input_name: frame})
        #end = time.time()
        output = out[0]
        output = output[0]
        output = self.one_euro_filter(output)
        for i in range(len(output)):  # Clip values between 0 - 1
            output[i] = max(min(output[i], 1), 0)
        self.output = output