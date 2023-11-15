from telegram import Update, Bot
from telegram.ext import ContextTypes
import re

from elma_api import ElmaAPI
from env_variables import EnvironmentVariables as ev
from core import Logger

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #print(f'Update "{update}" caused error "{context.error}"')
    pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = update.get_bot()
    bot_me = await bot.get_me()
    bot_name: str = str(bot_me.username)
    message_type: str = update.message.chat.type
    text: str = update.message.text
    Logger('INFO', f'User ({update.message.from_user.username}) in {update.message.chat.title}: "{text}"')
    if message_type == 'group':
        if bot_name in text:
            new_text: str = text.replace(f'@{bot_name}', '').strip()
            response: str = handle_response(new_text, update, bot_name)
        else:
            return
    else:
        return
    await update.message.reply_text(response)
    
def handle_response(text: str, update: Update, bot_name: str) -> str:
    key, processed_text = get_bot_key_and_command(text)
    if (key != None):
        create_bot_event_handler(key, processed_text, update, bot_name)
        return None
    else:
        has_active_processes, bot_event_id = check_for_active_bot_process(username=update.message.from_user.username)
        if has_active_processes == True:
            message = save_data_and_get_next_bot_process_field(bot_event_id=bot_event_id, message=text)
            return str(message)
        if has_active_processes == False or has_active_processes == None:
            return 'Не удалось распознать команду'

def get_bot_key_and_command(text: str) -> {str, str} | {None, None}:
    pattern = r'#(\w+)( .*)?'
    match = re.match(pattern, text)
    if match:
        key = match.group(1)
        rest_of_text = match.group(2)
        return key, rest_of_text
    else:
        return None, None

def create_bot_event_handler(key: str, processed_text: str, update: Update, bot_name: str) -> None:
    data = {'action': key,
            'message': processed_text,
            'author': update.message.from_user.username,
            'message_id': str(update.message.message_id),
            'chat_id': str(update.message.chat.id),
            'bot_name': f'@{bot_name}'
            }
    response = ElmaAPI().send_module_request('POST', ev.get_elma_service_module_endpoint_create_bot_event(), data)
    if response.status_code == 200:
        Logger('INFO', 'Bot event created')
    else:
        Logger('ERROR', 'Error creating bot event')
        
async def send_answer(bot_token: str, chat_id: str, message_id: str, response_text: str | None) -> None:
    bot = Bot(token=bot_token)
    if message_id != None:
        await bot.send_message(chat_id=chat_id, text=response_text, reply_to_message_id=message_id)
    else:
        await bot.send_message(chat_id=chat_id, text=response_text)


def check_for_active_bot_process(username: str):
    filter = {'event_author_username': username, 'active_process': True}
    app_elements_list = ElmaAPI().get_app_elements_list(
            section=ev.get_elma_tgbot_section(),
            app_name=ev.get_elma_tgbot_event_application(),
            filter=filter,
            active=True,
            size=100
        )
    if app_elements_list == None or len(app_elements_list) == 0:
        return False
    else:
        return True, app_elements_list[0]['__id']

def save_data_and_get_next_bot_process_field(bot_event_id: str, message: str):
    data = {'bot_event_id': bot_event_id, 'message': message}
    response = ElmaAPI().send_module_request('POST', ev.get_elma_service_module_endpoint_bot_next_field(), data)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return None

def set_active_bots_service():
    from app import BOTS
    from models import TelegramBot, TelegramBotManager
    try:
        app_elements_list = ElmaAPI().get_app_elements_list(
            section=ev.get_elma_tgbot_section(),
            app_name=ev.get_elma_tgbot_application(),
            status_code=["active"],
            active=True,
            size=100
        )
        if not app_elements_list is None:
            for active_bot in app_elements_list:
                name_to_check = active_bot['bot_name']
                is_bot_present = any(bot.name == name_to_check for bot in BOTS)
                if is_bot_present == False:
                    Logger('INFO', 'New bot: ' + name_to_check)
                    new_bot = TelegramBot(name=name_to_check, token=active_bot['token'])
                    TelegramBotManager(new_bot).start_bot()
                    BOTS.append(new_bot)
            result_set = set(item["bot_name"] for item in app_elements_list)
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
        Logger('INFO', 'Active bots: ' + str(len(BOTS)))
        return {
            'status': 'Success',
            'message': 'Active bots',
            'bots': str([str(bot.name) for bot in BOTS])
        }
    except Exception as e:
        Logger('ERROR', 'Error getting active bots: ' + str(e))
        return {
            'status': 'Error',
            'message': str(e),
            'BOTS': BOTS
        }