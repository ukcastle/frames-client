import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import time

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-mode=5 ! "
        "video/x-raw(memory:NVMM), "
        f"width=(int){capture_width}, height=(int){capture_height}, "
        f"format=(string)NV12, framerate=(fraction){framerate}/1 ! "
        # f"format=(string)NV12 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! "
        # f"video/x-raw, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
    )

class Video(QThread):

    signal = pyqtSignal(np.ndarray)

    def __init__(self, parent = None):
        super(Video, self).__init__(parent)
        self.frame = None
        self.cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        self.running = True
        
        print("Video Model 생성됨")
    
    def __del__(self):
        print("Video Model 삭제됨")
        self.cam.release()

    def stop(self):
        self.running = False
        self.cam.release()

    def run(self):
        while self.running:  
            ok, frame = self.cam.read()
            if ok:
                self.signal.emit(cv2.flip(frame, 1))
            del frame
            time.sleep(1/20)