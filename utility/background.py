import atexit
from common import config
from utility import remote
from cv import backend
from apscheduler.schedulers.background import BackgroundScheduler

def _print_test():
    print('Background thread is running')


def _check_tasks():
    if not config.IS_PROCESS_RUNNING:
        config.IS_PROCESS_RUNNING = True
        process_queue_return = remote.check_process_queue()

        if process_queue_return is not None:
            backend.process_video(process_queue_return)
            config.IS_PROCESS_RUNNING = False
            _check_tasks()

def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(id='test_scheduler', func=_print_test, trigger='interval', seconds=5)
    scheduler.add_job(id='check_tasks_scheduler', func=_check_tasks, trigger='interval', hour=1)

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    _check_tasks()