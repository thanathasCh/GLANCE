import atexit
from common import states
from utility import remote
from cv import backend
from apscheduler.schedulers.background import BackgroundScheduler


def _check_tasks():
    if not states.IS_PROCESS_RUNNING:
        states.IS_PROCESS_RUNNING = True
        unpro_video = remote.check_process_queue()

        if unpro_video is not None:
            backend.process_video(unpro_video)
            states.IS_PROCESS_RUNNING = False
            _check_tasks()


def _check_tasks_poc():
    if not states.IS_PROCESS_RUNNING:
        print('running')
        states.IS_PROCESS_RUNNING = True
        print('getting images')
        images = remote.get_poc_shelf_images()
        print('fetched images')

        if images:
            print('processing')
            backend.process_image_poc(images)
            states.IS_PROCESS_RUNNING = False
            # _check_tasks_poc()
         

def _check_tasks_embed_model():
    if not states.IS_PROCESS_RUNNING:
        print('running')
        states.IS_PROCESS_RUNNING = True
        print('getting images')
        images = remote.get_full_poc_shelf_images()
        print('fetched images')

        if images:
            print('processing')
            backend.process_image_emb_poc(images)
            states.IS_PROCESS_RUNNING = False
            # _check_tasks_embed_model()

def start():
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(id='check_tasks_scheduler', func=_check_tasks, trigger='interval', hours=1)

    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())

    # _check_tasks()
    _check_tasks_poc()