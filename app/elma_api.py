import json
import requests
from env_variables import EnvironmentVariables as ev


class ElmaAPI:
    def __init__(self):
        self._base_url = ev.get_elma_url()
        self._token = ev.get_elma_token()
        self._module_uid = ev.get_elma_service_module_uid()
    
    def send_request(self, method: str, endpoint: str, data: dict | None) -> requests.Response:
        url = f'{self._base_url}{endpoint}'
        if ev.get_service_debug() == True:
            print('   [→] Sending request to ELMA')
            print('       Method:', method)
            print('       URL:', url)
            print('       Data:', data)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._token}'
        }
        if data == None:
            response = requests.request(method, url, headers=headers)
        else:
            data_json = json.dumps(data)
            response = requests.request(method, url, data=data_json, headers=headers)
        return response
    
    def get_app_elements_list(self, section: str, app_name: str, filter: dict | None = None, status_code: list | None = None , active: bool = True, size: int = 100) -> dict:
        endpoint = f'/pub/v1/app/{section}/{app_name}/list'
        data = {
                'active': active,
                'size': size
            }
        if filter != None:
            data['filter'] = {
                            'tf': filter
                        }
        if status_code != None:
            data['statusCode'] = status_code
        response = self.send_request('POST', endpoint, data)
        if response.status_code == 200:
            return response.json()['result']['result']
        else:
            print(f'   [x] Error getting list of {app_name} elements: {response.text}')
            return None
    
    def send_module_request(self, method: str, function_name: str, data: dict) -> requests.Response:
        endpoint = f'/api/extensions/{self._module_uid }/script/{function_name}'
        response = self.send_request(method, endpoint, data)
        return response