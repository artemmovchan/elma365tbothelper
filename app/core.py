from env_variables import EnvironmentVariables as ev

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
            if log_type == 'INFO':
                print(f'   [i] {message}')
            elif log_type == 'WARNING':
                print(f'   [!] {message}')
            elif log_type == 'ERROR':
                print(f'   [x] {message}')