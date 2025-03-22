from flask import Flask, request
import requests
import telegram

app = Flask(__name__)
TOKEN = "YOUR_TOKEN"
bot = telegram.Bot(token=TOKEN)

@app.route('/port')
def home():
    return "Bot Running!"

@app.route('/uid', methods=['POST'])
def uid():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text.startswith('/check'):
            parts = text.split()
            if len(parts) > 1:
                uid = parts[1]
                url = f'http://minhnguyen3004.x10.mx/infofreefire.php?id={uid}'
                res = requests.get(url)
                info = res.json()
                bot.send_message(chat_id, f"UID: {info.get('Account UID')}, Tên: {info.get('Account Name')}")
            else:
                bot.send_message(chat_id, "Vui lòng nhập UID sau lệnh.")
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
