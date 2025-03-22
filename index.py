from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_safe(data, key, default="Không Có"):
    return data.get(key, default) if key in data else default

def get_free_fire_info(account_id):
    url = f'http://minhnguyen3004.x10.mx/infofreefire.php?id={account_id}'
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '').lower()

    if 'application/json' in content_type:
        data = response.json()

        if "Account Name" not in data:
            return {"error": f"Không tìm thấy thông tin cho ID {account_id}."}

        account_info = {
            "Tên Tài Khoản": get_safe(data, 'Account Name'),
            "UID Tài Khoản": get_safe(data, 'Account UID'),
            "Cấp Độ": get_safe(data, 'Account Level'),
            "XP": get_safe(data, 'Account XP'),
            "Likes": get_safe(data, 'Account Likes'),
            "Ngôn Ngữ": get_safe(data, 'Account Language'),
            "Lần Đăng Nhập Cuối": get_safe(data, 'Account Last Login (GMT 0530)'),
            "Ngày Tạo": get_safe(data, 'Account Create Time (GMT 0530)'),
            "Trạng Thái Nổi Tiếng": get_safe(data, 'Account Celebrity Status')
        }
        return account_info
    return {"error": "Phản hồi không hợp lệ từ API"}

@app.route('/')
def home():
    return "API Free Fire Info is running!"

@app.route('/info', methods=['GET'])
def info():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "Vui lòng cung cấp UID: /info?uid=123456"}), 400
    info = get_free_fire_info(uid)
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
