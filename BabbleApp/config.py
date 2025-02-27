import json
import os.path
import shutil

from tab import Tab
from pydantic import BaseModel
from typing import Union

CONFIG_FILE_NAME: str = "babble_settings.json"
BACKUP_CONFIG_FILE_NAME: str = "babble_settings.backup"

class BabbleCameraConfig(BaseModel):
    rotation_angle: int = 0
    roi_window_x: int = 0
    roi_window_y: int = 0
    roi_window_w: int = 0
    roi_window_h: int = 0
    capture_source: Union[int, str, None] = None
    use_calibration: bool = False
    use_n_calibration: bool = True
    gui_vertical_flip: bool = False
    gui_horizontal_flip: bool = False

class BabbleSettingsConfig(BaseModel):
    gui_min_cutoff: str = "10.5004"
    gui_speed_coefficient: str = "0.62"
    gui_osc_address: str = "127.0.0.1"
    gui_osc_port: int = 8888
    gui_osc_receiver_port: int = 9001
    gui_osc_recalibrate_address: str = "/avatar/parameters/babble_recalibrate"
    gui_update_check: bool = True
    gui_ROSC: bool = False
    gui_osc_location: str = ""
    gui_multiply: int = 1
    gui_model_file: str = 'Models/ENEXTXXE100D4/'
    gui_backend: str = "OpenVino"
    gui_use_gpu: bool = False
    gui_gpu_index: int = 0
    gui_inference_threads: int = 1
    gui_use_red_channel: bool = False
    calib_array: str = "[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]"
    gui_cam_resolution_x: int = 0    
    gui_cam_resolution_y: int = 0
    gui_cam_framerate: int = 0

class BabbleConfig(BaseModel):
    version: int = 1
    cam: BabbleCameraConfig = BabbleCameraConfig()
    settings: BabbleSettingsConfig = BabbleSettingsConfig()
    cam_display_id: Tab = Tab.CAM

    @staticmethod
    def load():
        if not os.path.exists(CONFIG_FILE_NAME):
            print("No settings file, using base settings")
            return BabbleConfig()
        try:
            with open(CONFIG_FILE_NAME, "r") as settings_file:
                return BabbleConfig(**json.load(settings_file))
        except json.JSONDecodeError:
            print("[INFO] Failed to load settings file")
            load_config = None
            if os.path.exists(BACKUP_CONFIG_FILE_NAME):
                try:
                    with open(BACKUP_CONFIG_FILE_NAME, "r") as settings_file:
                        load_config = BabbleConfig(**json.load(settings_file))
                    print("[INFO] Using backup settings")
                except json.JSONDecodeError:
                    pass
            if load_config is None:
                print("[INFO] using base settings")
                load_config = BabbleConfig()
            return load_config

    def save(self):
        # make sure this is only called if there is a change
        if os.path.exists(CONFIG_FILE_NAME):
            try:
                # Verify existing configuration files.
                with open(CONFIG_FILE_NAME, "r") as settings_file:
                    BabbleConfig(**json.load(settings_file))
                shutil.copy(CONFIG_FILE_NAME, BACKUP_CONFIG_FILE_NAME)
                # print("Backed up settings files.") # Comment out because it's too loud.
            except json.JSONDecodeError:
                # No backup because the saved settings file is broken.
                pass
        with open(CONFIG_FILE_NAME, "w") as settings_file:
            json.dump(obj=self.dict(), fp=settings_file)
        print("[INFO] Config Saved Successfully")
