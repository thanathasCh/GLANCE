class path():
    def __init__(self) -> None:
        self.IMAGES = 'images'
        self.VIDEOS = 'videos'
        self.IMAGE = f'{self.IMAGES}/1.jpg'
        self.VIDEO = f'{self.VIDEOS}/1.mp4'


PATH = path()
BATCH_SIZE = 1
INPUT_SIZE = (640, 640)
WEIGHTS_FILE = 'yolo/yolov4.weights'
CONFIG_FILE = 'yolo/yolov4.cfg'
CLASS_FILE = 'yolo/obj.names'
THRESH = 0.25
CONFIDENCE = 0.3
COLOR = (255, 0, 0)