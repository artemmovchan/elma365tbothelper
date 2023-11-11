from flask import Flask, request, jsonify
from models import TelegramBot
from services import send_answer
from services_monitoring import run_active_bots_monitoring_service
from core import logo_log

ELMA_URL = 'https://ngvzc74rto7dw.elma365.ru'
ELMA_TOKEN = '169e0c94-c140-4bb9-8e08-47bdb0cd5fc0'

ELMA_BOTS_LIST = '/pub/v1/app/tgbots/bots/list'
ELMA_BOT_EVENTS_LIST = '/pub/v1/app/tgbots/bot_events/list'
ELMA_BOT_EVENTS_CREATE = '/api/extensions/8e2fc5e1-34f6-4890-b41e-96844f6a8449/script/create_bot_event'

ELMA_BOT_NEXT_FIELD = '/api/extensions/8e2fc5e1-34f6-4890-b41e-96844f6a8449/script/get_next_bot_process_field'

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