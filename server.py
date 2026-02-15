from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Токен берём из переменных окружения Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'HerVibe Proxy Running'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    chat_id = data.get('chat_id')
    text = data.get('text')
    
    if not TOKEN:
        return jsonify({'ok': False, 'description': 'Нет токена'}), 500
    
    try:
        response = requests.post(
            f'https://api.telegram.org/bot{TOKEN}/sendMessage',
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'ok': False, 'description': str(e)}), 500

@app.route('/get-updates')
def get_updates():
    if not TOKEN:
        return jsonify({'ok': False, 'description': 'Нет токена'}), 500
    
    offset = request.args.get('offset')
    timeout = request.args.get('timeout', 10)
    
    try:
        params = {'offset': offset, 'timeout': timeout}
        r = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params=params,
            timeout=15
        )
        return jsonify(r.json())
    except Exception as e:
        return jsonify({'ok': False, 'description': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
