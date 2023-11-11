import json
from telegram import Update, Bot
from telegram.ext import ContextTypes
import re
import requests


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update "{update}" caused error "{context.error}"')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = update.get_bot()
    bot_me = await bot.get_me()
    bot_name: str = str(bot_me.username)
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.from_user.username}) in {update.message.chat.title}: "{text}"')
    if message_type == 'group':
        if bot_name in text:
            new_text: str = text.replace(f'@{bot_name}', '').strip()
            response: str = handle_response(new_text, update, bot_name)
        else:
            return
    else:
        return
    print('Bot:', response)
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
    from app import ELMA_URL, ELMA_TOKEN, ELMA_BOT_EVENTS_CREATE
    url = f'{ELMA_URL}{ELMA_BOT_EVENTS_CREATE}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ELMA_TOKEN}'
    }
    data = {'action': key,
            'message': processed_text,
            'author': update.message.from_user.username,
            'message_id': str(update.message.message_id),
            'chat_id': str(update.message.chat.id),
            'bot_name': f'@{bot_name}'
            }
    data_json = json.dumps(data)
    response = requests.post(url, data=data_json, headers=headers)
    if response.status_code == 200:
        print('Bot event created')
    else:
        print('Error creating bot event')
        
async def send_answer(bot_token: str, chat_id: str, message_id: str, response_text: str | None) -> None:
    bot = Bot(token=bot_token)
    if message_id != None:
        await bot.send_message(chat_id=chat_id, text=response_text, reply_to_message_id=message_id)
    else:
        await bot.send_message(chat_id=chat_id, text=response_text)


def check_for_active_bot_process(username: str):
    from app import ELMA_URL, ELMA_TOKEN, ELMA_BOT_EVENTS_LIST
    url = f'{ELMA_URL}{ELMA_BOT_EVENTS_LIST}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ELMA_TOKEN}'
    }
    data = {'active': True, 'filter': {'tf': {'event_author_username': username, 'active_process': True}}}
    data_json = json.dumps(data)
    response = requests.post(url, data=data_json, headers=headers)
    if response.status_code == 200:
        result = response.json()['result']['result']
        if len(result) == 0:
            return False
        else:
            return True, result[0]['__id']
    else:
        return None

def save_data_and_get_next_bot_process_field(bot_event_id: str, message: str):
    from app import ELMA_URL, ELMA_TOKEN, ELMA_BOT_NEXT_FIELD
    url = f'{ELMA_URL}{ELMA_BOT_NEXT_FIELD}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ELMA_TOKEN}'
    }
    data = {'bot_event_id': bot_event_id, 'message': message}
    data_json = json.dumps(data)
    response = requests.post(url, data=data_json, headers=headers)
    if response.status_code == 200:
        result = response.json()['message']
        return result
    else:
        return None