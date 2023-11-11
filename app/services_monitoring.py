import schedule
import time
import requests
import json
from models import TelegramBot, TelegramBotManager
import threading

def _get_active_bots_service():
    from app import BOTS, ELMA_URL, ELMA_TOKEN, ELMA_BOTS_LIST
    print('   _____________________________________')
    print('   [→] Sending request to get active bots...')
    url = f'{ELMA_URL}{ELMA_BOTS_LIST}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ELMA_TOKEN}'
    }
    data = {'active': True, 'statusCode': ["active"]}
    data_json = json.dumps(data)
    try:
        response = requests.post(url, data=data_json, headers=headers)
        if response.status_code == 200:
            result = response.json()['result']['result']
            if not result is None:
                for active_bot in result:
                    name_to_check = active_bot['bot_name']
                    is_bot_present = any(bot.name == name_to_check for bot in BOTS)
                    if is_bot_present == False:
                        print('     New bot:', name_to_check)
                        new_bot = TelegramBot(name=name_to_check, token=active_bot['token'])
                        TelegramBotManager(new_bot).start_bot()
                        BOTS.append(new_bot)
                result_set = set(item["bot_name"] for item in result)
                NEW_BOTS = []
                for bot in BOTS:
                    if bot.name not in result_set:
                        TelegramBotManager(bot).stop_bot()
                        try:
                            BOTS.remove(bot)
                        except:
                            pass
                    else:
                        NEW_BOTS.append(bot)
                BOTS = NEW_BOTS
            print('    Active bots:', len(BOTS))
        else:
            print(f'   [x] Error getting active bots: {response.text}')
    except:
        print('   [x] Error getting active bots: Unknown error')


schedule.every(0.5).minutes.do(_get_active_bots_service)

def _start_active_bots_monitoring_service():
    print('Starting ACTIVE BOTS MONITORING...')
    _get_active_bots_service()
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_active_bots_monitoring_service():
    background_thread = threading.Thread(target=_start_active_bots_monitoring_service)
    background_thread.start()

if __name__ == '__main__':
    _start_active_bots_monitoring_service()