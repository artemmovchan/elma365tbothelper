from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests
import json


TOKEN: Final = '2104392816:AAEYhyP2-DDhdOGtunNgG4Lcu46FaZNqJFw'
BOT_NAME: Final = '@test_elma_bot'

ELMA_URL = 'https://cybb4fnhq6ehs.elma365.ru'
ELMA_TOKEN = '76855565-f566-47b6-9ae1-654c1ab3cb2f'

CREATE_TASK_ENDPOINT = '/api/extensions/6d0bba44-347a-4982-aa04-242d66abb37d/script/task_creation'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет, я бот!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Это help!')

async def new_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username
    if username != 'movchanartem':
        await update.message.reply_text(f'Слышь. Не ломись в мою ELMA, чувак!')
    else:
        message: str | None = update.message.text.replace(f'{BOT_NAME}', '').strip()
        message = update.message.text.replace(f'/new_task', '').strip()
        if not message is None and message != '':
            url = f'{ELMA_URL}{CREATE_TASK_ENDPOINT}'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ELMA_TOKEN}'
            }
            data = {'subject': 'Это тема задачи', 'text': message, 'username': username}
            data_json = json.dumps(data)
            response = requests.post(url, data=data_json, headers=headers)
            if response.status_code == 200:
                await update.message.reply_text(f'Для вас все что угодно милорд')
            else:
                await update.message.reply_text(f'Хм... Не получилось создать задачу в ELMA. Попробуй позже.')
        else:
            await update.message.reply_text(f'Вообще что-то пошло не так. Попробуй позже.')
    
def handle_response(text: str) -> str:
    processed_text: str = text.lower()
    if 'прослушивают' in processed_text:
        return 'Тебе не кажется, чувак...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.from_user.username}) in {update.message.chat.title}: "{text}"')
    
    if message_type == 'group':
        if BOT_NAME in text:
            new_text: str = text.replace(BOT_NAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update "{update}" caused error "{context.error}"')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('new_task', new_task_command))
    
    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Error
    app.add_error_handler(error)
    
    print('Polling...')
    app.run_polling(poll_interval=3)