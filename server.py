from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

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
    
    response = requests.post(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    )
    return jsonify(response.json())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)