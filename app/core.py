from env_variables import EnvironmentVariables as ev
import requests

def logo_log():
    print('')
    print('##     ## ##     ##  ######  ##     ## ##    ##     ######  ##    ##  ######  ######## ######## ##     ##  ######')
    print('###   ### ##     ## ##    ## ##     ## ###   ##    ##    ##  ##  ##  ##    ##    ##    ##       ###   ### ##    ## ')
    print('#### #### ##     ## ##       ##     ## ####  ##    ##         ####   ##          ##    ##       #### #### ##       ')
    print('## ### ## ##     ## ##       ######### ## ## ##     ######     ##     ######     ##    ######   ## ### ##  ######  ')
    print('##     ##  ##   ##  ##       ##     ## ##  ####          ##    ##          ##    ##    ##       ##     ##       ## ')
    print('##     ##   ## ##   ##    ## ##     ## ##   ###    ##    ##    ##    ##    ##    ##    ##       ##     ## ##    ## ')
    print('##     ##    ###     ######  ##     ## ##    ##     ######     ##     ######     ##    ######## ##     ##  ######  ')
    print('')
    
class Logger:
    def __init__(self, log_type: str, message: str):
        if ev.get_service_debug() == 'True':
            requests.post(ev.get_webhook(), json={'text': f'[{log_type}] {message}'})
            if log_type == 'INFO':
                print(f'   [i] {message}')
            elif log_type == 'WARNING':
                print(f'   [!] {message}')
            elif log_type == 'ERROR':
                print(f'   [x] {message}')