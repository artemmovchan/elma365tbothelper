from flask import Flask, request, jsonify
from models import TelegramBot
from services import send_answer
from services_monitoring import run_active_bots_monitoring_service
from core import logo_log

ELMA_URL = 'https://cybb4fnhq6ehs.elma365.ru'
ELMA_TOKEN = '76855565-f566-47b6-9ae1-654c1ab3cb2f'

ELMA_BOTS_LIST = '/pub/v1/app/tgbot/bots/list'
ELMA_BOT_EVENTS_CREATE = '/api/extensions/6d0bba44-347a-4982-aa04-242d66abb37d/script/create_bot_event'

app = Flask(__name__)
BOTS: list[TelegramBot] = []

@app.route('/answer', methods=['POST'])
async def answer():
    if request.method == 'POST':
        try:
            data = request.get_json(silent=True)
            print(data)
            message_id = data['message_id'] if 'message_id' in data else None
            await send_answer(data['bot_token'], data['chat_id'], message_id, data['response_text'])
            return jsonify(
                status = 'Success',
                message = 'Send answer',
            ) , 200
        except Exception as e:
            return jsonify(
                status = 'Error',
                message = str(e)
            ) , 400

if __name__ == "__main__":
    logo_log()
    run_active_bots_monitoring_service()
    app.run(host='0.0.0.0', port=5000, debug=False)