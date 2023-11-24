from flask import Flask, request, jsonify, render_template

from models import TelegramBot
from services import send_answer, set_active_bots_service
from services_monitoring import run_active_bots_monitoring_service
from core import logo_log


app = Flask(__name__)
BOTS: list[TelegramBot] = []


@app.route("/health", methods=['GET'])
def health():
    return jsonify(
        status = 'UP'
    )

@app.route('/answer', methods=['POST'])
async def answer():
    if request.method == 'POST':
        try:
            data = request.get_json(silent=True)
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

@app.route('/set_active_bots', methods=['GET'])
async def set_active_bots():
    if request.method == 'GET':
        try:
            service_response = set_active_bots_service()
            if service_response['status'] == 'Error':
                return jsonify(
                    status = 'Error',
                    message = service_response['message']
                ) , 400
            else:
                return jsonify(
                    status = 'Success',
                    message = service_response['message'],
                    bots = service_response['bots']
                ) , 200
        except Exception as e:
            return jsonify(
                status = 'Error',
                message = str(e)
            ) , 400
            

if __name__ == "__main__":
    logo_log()
    print('SERVICE: TBOT HELPER')
    #run_active_bots_monitoring_service()
    set_active_bots_service()
    app.run(host='0.0.0.0', port=5000, debug=False)