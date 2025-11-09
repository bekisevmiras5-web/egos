import os
from flask import Flask, request, jsonify, send_file, abort
import requests
from io import BytesIO
import qrcode
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # optional .env

DEEPSEEK_KEY = os.environ.get('DEEPSEEK_API_KEY')  # set this in env
OPENWEATHER_KEY = os.environ.get('OPENWEATHER_API_KEY')  # set this in env

app = Flask(__name__, static_folder='.', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Weather proxy: frontend calls this, server uses OPENWEATHER_KEY
@app.route('/api/weather')
def weather():
    if not OPENWEATHER_KEY:
        return jsonify({"error":"NO_API_KEY"}), 500
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({"error":"missing coords"}), 400
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric&lang=ru'
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return jsonify({"error":"weather_failed","status":r.status_code}), 500
    d = r.json()
    result = {
        "name": d.get("name"),
        "temp": d.get("main",{}).get("temp"),
        "desc": d.get("weather",[{}])[0].get("description")
    }
    return jsonify(result)

# Chat proxy: frontend posts {message:"..."}
@app.route('/api/chat', methods=['POST'])
def chat():
    if not DEEPSEEK_KEY:
        return jsonify({"error":"NO_DEEPSEEK_KEY"}), 500
    data = request.get_json() or {}
    msg = data.get('message','').strip()
    if not msg:
        return jsonify({"error":"no_message"}), 400

    # basic protections:
    if len(msg) > 2000:
        return jsonify({"error":"message_too_long"}), 400

    # Forward to DeepSeek (example endpoint; adjust if API differs)
    deepseek_url = "https://api.deepseek.com/v1/chat/completions"
    payload = {
        "model": "deepseek-chat",  # change if your model name differs
        "messages": [{"role":"user","content": msg}],
        "max_tokens": 800
    }
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    try:
        r = requests.post(deepseek_url, json=payload, headers=headers, timeout=20)
        r.raise_for_status()
        j = r.json()
        # Parse reply depending on DeepSeek response shape; adjust if necessary:
        # Example: j["choices"][0]["message"]["content"]
        reply = ""
        if "choices" in j and len(j["choices"])>0:
            choice = j["choices"][0]
            msg_obj = choice.get("message", {}) or {}
            reply = msg_obj.get("content") or choice.get("text") or str(j)
        else:
            reply = j.get("reply") or str(j)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error":"deepseek_error", "detail": str(e)}), 500

# QR generation endpoint: returns PNG
@app.route('/api/qr')
def qr():
    url = request.args.get('url') or 'https://bekisevmiras5-web.github.io/egos/'
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
