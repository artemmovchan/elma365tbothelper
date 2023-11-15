import schedule
import time
import threading

from services import set_active_bots_service
from core import Logger


schedule.every(0.5).minutes.do(set_active_bots_service)


def _start_active_bots_monitoring_service():
    Logger('INFO', 'Starting ACTIVE BOTS MONITORING...')
    set_active_bots_service()
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_active_bots_monitoring_service():
    background_thread = threading.Thread(target=_start_active_bots_monitoring_service)
    background_thread.start()

if __name__ == '__main__':
    _start_active_bots_monitoring_service()