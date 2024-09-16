import time
import threading
import cv2
import picamera2
import libcamera
from picamera2 import Picamera2

class CameraEvent:
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = threading.get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].is_set():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[threading.get_ident()][0].clear()

class BaseCamera:
    thread = None
    frame = None
    last_access = 0
    event = CameraEvent()

    def __init__(self):
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        BaseCamera.last_access = time.time()
        BaseCamera.event.wait()
        BaseCamera.event.clear()
        return BaseCamera.frame

    @staticmethod
    def frames():
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()
            time.sleep(0)
        BaseCamera.thread = None

class Picamera2Camera(BaseCamera):
    @staticmethod
    def frames():
        picam2 = Picamera2()
        preview_config = picam2.preview_configuration
        preview_config.size = (640, 480)
        preview_config.format = 'RGB888'
        preview_config.buffer_count = 4
        preview_config.queue = True
        preview_config.transform = libcamera.Transform(hflip=0, vflip=0)
        preview_config.colour_space = libcamera.ColorSpace.Sycc()

        if not picam2.is_open:
            raise RuntimeError('Could not start camera.')

        try:
            picam2.start()
        except Exception as e:
            print(f"Error: {e}")
            print("Please check camera connection and settings.")
        
        while True:
            img = picam2.capture_array()
            if img is None:
                continue
            if cv2.imencode('.jpg', img)[0]:
                yield cv2.imencode('.jpg', img)[1].tobytes()

