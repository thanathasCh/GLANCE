# Status
IS_TEST = True
IS_PROCESS_RUNNING = False

# String
WEB_NAME = 'Glance'

# Base Directory
OBJECT_DETECTION = 'cv/object_detection'
FEATURE_PATH = 'test_db'

# Path
WEIGHTS_FILE = f'{OBJECT_DETECTION}/yolo/yolov4.weights'
CONFIG_FILE = f'{OBJECT_DETECTION}/yolo/yolov4.cfg'
CLASS_FILE = f'{OBJECT_DETECTION}/yolo/obj.names'

LOCAL_DB = 'common/local.db'

# Configuration
BATCH_SIZE = 1
THRESH = .25
CONFIDENCE = .3
CONFIDENCE = .3

# Shape
OBJ_INPUT_SIZE = (640, 640)
FX_INPUT_SIZE = (500, 500)
FX_IMAGE_SIZE = (500, 500, 3)
FX_IMAGE_SIZE_EMB = (-1, 500, 500, 3)

# Colors
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)

# Feature matching
MIN_MATCH = 10
RATIO = .8
ORB_NUM = 1000
INDEX_PARAMS = dict(
    algorithm=6,
    table_number=6,
    key_size=12,
    multi_probe_level=1
)
SEARCH_PARAMS = dict(checks=64)
EMB_SIZE = 128
DIS_ALG = 'euclidean'
K_NUM = 15