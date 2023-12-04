import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

class EnvironmentVariables:
        _SERVICE_DEBUG = os.environ.get("SERVICE_DEBUG")
        _WEBHOOK = os.environ.get("WEBHOOK")
        _ELMA_URL = os.environ.get("ELMA_URL")
        _ELMA_TOKEN = os.environ.get("ELMA_TOKEN")
        _ELMA_SERVICE_MODULE_UID = os.environ.get("ELMA_SERVICE_MODULE_UID")
        
        _ELMA_TGBOT_SECTION = os.environ.get("ELMA_TGBOT_SECTION")
        _ELMA_TGBOT_APPLICTION = os.environ.get("ELMA_TGBOT_APPLICTION")
        _ELMA_TGBOT_EVENT_APPLICTION= os.environ.get("ELMA_TGBOT_EVENT_APPLICTION")
        _ELMA_SERVICE_MODULE_ENDPOINT_CREATE_BOT_EVENT = os.environ.get("ELMA_SERVICE_MODULE_ENDPOINT_CREATE_BOT_EVENT")
        _ELMA_SERVICE_MODULE_ENDPOINT_BOT_NEXT_FIELD = os.environ.get("ELMA_SERVICE_MODULE_ENDPOINT_BOT_NEXT_FIELD")
        
        @classmethod
        def get_service_debug(cls):
            return cls._SERVICE_DEBUG
        
        @classmethod
        def get_webhook(cls):
            return cls._WEBHOOK
        
        @classmethod
        def get_elma_url(cls):
            return cls._ELMA_URL
        
        @classmethod
        def get_elma_token(cls):
            return cls._ELMA_TOKEN
        
        @classmethod
        def get_elma_service_module_uid(cls):
            return cls._ELMA_SERVICE_MODULE_UID
        
        @classmethod
        def get_elma_tgbot_section(cls):
            return cls._ELMA_TGBOT_SECTION
        
        @classmethod
        def get_elma_tgbot_application(cls):
            return cls._ELMA_TGBOT_APPLICTION
        
        @classmethod
        def get_elma_tgbot_event_application(cls):
            return cls._ELMA_TGBOT_EVENT_APPLICTION
        
        @classmethod
        def get_elma_service_module_endpoint_create_bot_event(cls):
            return cls._ELMA_SERVICE_MODULE_ENDPOINT_CREATE_BOT_EVENT
        
        @classmethod
        def get_elma_service_module_endpoint_bot_next_field(cls):
            return cls._ELMA_SERVICE_MODULE_ENDPOINT_BOT_NEXT_FIELD