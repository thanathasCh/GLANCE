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

def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(id='check_tasks_scheduler', func=_check_tasks, trigger='interval', hour=1)

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    _check_tasks()