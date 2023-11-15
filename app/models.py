from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import multiprocessing

from core import Logger
from services import handle_message, error

processes = []


class TelegramBot:
    def __init__(self, name, token):
        self.is_running = True
        self.name = name
        self.token = token
        self.process = None


class TelegramBotManager:
    def __init__(self, bot: TelegramBot):
        self.bot = bot
    
    def start_bot(self):
        process = multiprocessing.Process(target=self._run_bot)
        processes.append(process)
        process.start()
        self.bot.process = process
        Logger('INFO', f'Starting process with name {process.name} for bot {self.bot.name}')
    
    def _run_bot(self):
        app = Application.builder().token(self.bot.token).build()
        app.add_handler(MessageHandler(filters.TEXT, handle_message))
        app.add_error_handler(error)
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    
    def stop_bot(self):
        process = self.bot.process
        try:
            process.terminate()
            process.join()
        except:
            pass
        Logger('WARNING', f'Stopping process with name {process.name} for bot {self.bot.name}')