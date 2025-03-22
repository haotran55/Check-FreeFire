import requests

def get_safe(data, key, default="Không Có"):
    """ Trả về giá trị của key trong dữ liệu, nếu không có trả về giá trị mặc định """
    return data.get(key, default) if key in data else default

def get_free_fire_info(account_id):
    try:
        url = f'http://minhnguyen3004.x10.mx/infofreefire.php?id={account_id}'
        response = requests.get(url)
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            data = response.json()

            if "Account Name" not in data:
                print(f"⚠️ Không tìm thấy thông tin cho ID {account_id}.")
                return

            # Định dạng tin nhắn
            account_info = "┌ THÔNG TIN TÀI KHOẢN 📊\n"
            account_info += f"├ Tên Tài Khoản: {get_safe(data, 'Account Name')}\n"
            account_info += f"├ UID Tài Khoản: {get_safe(data, 'Account UID')}\n"
            account_info += f"├ Cấp Độ Tài Khoản: {get_safe(data, 'Account Level')}\n"
            account_info += f"├ XP Tài Khoản: {get_safe(data, 'Account XP')}\n"
            account_info += f"├ Số Likes Tài Khoản: {get_safe(data, 'Account Likes')}\n"
            account_info += f"├ Ngôn Ngữ Tài Khoản: {get_safe(data, 'Account Language')}\n"
            account_info += f"├ Lần Đăng Nhập Cuối: {get_safe(data, 'Account Last Login (GMT 0530)')}\n"
            account_info += f"├ Thời Gian Tạo Tài Khoản: {get_safe(data, 'Account Create Time (GMT 0530)')}\n"
            account_info += f"├ Trạng Thái Nổi Tiếng: {get_safe(data, 'Account Celebrity Status')}\n"
            account_info += "└──────────────────────────\n"

            print(account_info)
        else:
            print("❌ Không nhận được dữ liệu JSON hợp lệ.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    # Test với ID bất kỳ
    test_id = input("Nhập UID tài khoản Free Fire: ")
    get_free_fire_info(test_id)
