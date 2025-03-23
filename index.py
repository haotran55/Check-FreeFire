import telebot
import os
from telebot import types

# Lấy token từ biến môi trường trên Render
TOKEN = os.getenv("8127007530:AAG1b4w__xXvIrAr7woZjN8BrC_l3g1hBwI")
bot = telebot.TeleBot(TOKEN)

# Lệnh /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id  # ✔ Thụt vào đúng
    bot.send_message(user_id, "Chào mừng bạn đến với bot!")  


@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.chat.id
    cursor.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result and result[0] == 1:
        bot.send_message(user_id, "Bạn là admin!")
    else:
        bot.send_message(user_id, "Bạn không phải admin!")


# Lệnh chơi Tài Xỉu
@bot.message_handler(commands=['taixiu'])
def taixiu(message):
    dice_1 = random.randint(1, 6)
    dice_2 = random.randint(1, 6)
    dice_3 = random.randint(1, 6)
    total = dice_1 + dice_2 + dice_3

    result = "🎲 Xỉu!" if total <= 10 else "🎲 Tài!"
    
    bot.send_message(
        message.chat.id,
        f"🎲 Xúc xắc: {dice_1} - {dice_2} - {dice_3}\n"
        f"✨ Tổng điểm: {total}\n"
        f"👉 Kết quả: {result}")


# Lệnh spam tin nhắn
@bot.message_handler(commands=['spam'])
def spam_message(message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            bot.reply_to(message, "Cú pháp: /spam [số đt] [Số lần]")
            return

        times = int(parts[1])
        text = parts[2]

        if times > 20:
            bot.reply_to(message, "Bạn chỉ có thể spam tối đa 20 lần!")
            return

        for _ in range(times):
            bot.send_message(message.chat.id, text)

    except ValueError:
        bot.reply_to(message, "Số lần phải là số nguyên!")

# Chạy bot
print("Bot đang chạy.")
bot.infinity_polling()
