import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Hàm lấy thông tin tài khoản Free Fire
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
                return f"⚠️ Không tìm thấy thông tin cho ID {account_id}."

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

            return account_info
    except Exception as e:
        return f"⚠️ Đã xảy ra lỗi: {str(e)}"

# Hàm xử lý lệnh /getinfo
async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        account_id = context.args[0]  # Lấy ID từ tham số người dùng nhập
        info = get_free_fire_info(account_id)
        await update.message.reply_text(info)
    except IndexError:
        await update.message.reply_text("⚠️ Vui lòng cung cấp ID tài khoản. Ví dụ: /getinfo 123456")

# Hàm chính để khởi tạo bot
async def main():
    # Sử dụng token bạn nhận từ BotFather
    TOKEN = '8127007530:AAG1b4w__xXvIrAr7woZjN8BrC_l3g1hBwI'
    WEBHOOK_URL = 'https://yourdomain.com/webhook'  # Cập nhật với URL webhook của bạn

    # Cấu hình ứng dụng
    application = Application.builder().token(TOKEN).build()

    # Đăng ký lệnh /getinfo
    application.add_handler(CommandHandler("getinfo", get_info))

    # Cài đặt webhook (cần await)
    await application.bot.set_webhook(WEBHOOK_URL)

    # Bắt đầu bot với webhook thay vì polling
    await application.run_webhook(listen="0.0.0.0", port=443, url_path="webhook", webhook_url=WEBHOOK_URL)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
