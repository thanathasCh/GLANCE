import atexit
from common import config
from utility import remote
from cv import backend
from apscheduler.schedulers.background import BackgroundScheduler


def _check_tasks():
    if not config.IS_PROCESS_RUNNING:
        config.IS_PROCESS_RUNNING = True
        unpro_video = remote.check_process_queue()

        if unpro_video is not None:
            backend.process_video(unpro_video)
            config.IS_PROCESS_RUNNING = False
            _check_tasks()


def _check_tasks_poc():
    if not config.IS_PROCESS_RUNNING:
        config.IS_PROCESS_RUNNING = True
        images = remote.get_poc_shelf_images()

        if images:
            backend.process_image_poc(images)
            config.IS_PROCESS_RUNNING = False
            _check_tasks_poc()
         

def start():
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(id='check_tasks_scheduler', func=_check_tasks, trigger='interval', hours=1)

    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())

    # _check_tasks()
    _check_tasks_poc()