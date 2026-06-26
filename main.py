import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. إعداد البوت بتوكن خاص بك
BOT_TOKEN = "8985389453:AAFMC94DtQks9GPXcwL"  # التوكن الخاص بك
bot = telebot.TeleBot(BOT_TOKEN)

# 2. معرف قناتك الإلزامية
CHANNEL_ID = "@TeamBacDZ"

# خادم وهمي لإرضاء منصة Render ومنع توقف البوت
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# دالة التحقق من اشتراك المستخدم
def is_user_subscribed(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# معالج الرسائل والتحقق من الاشتراك الإلزامي
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not is_user_subscribed(CHANNEL_ID, user_id):
        markup = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("➕ الاشتراك في القناة", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")
        btn_check = types.InlineKeyboardButton("🔄 تحقق من الاشتراك", callback_data="check_sub")
        markup.add(btn_channel, btn_check)
        
        bot.reply_to(
            message,
            f"عذراً يا {first_name}! عليك الاشتراك في القناة أولاً لاستخدام البوت.",
            reply_markup=markup
        )
    else:
        bot.reply_to(message, f"مرحباً بك يا {first_name}! أنت مشترك بالفعل في القناة وجاهز لاستخدام الخدمة.")

# معالج زر التحقق بعد الاشتراك
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription_callback(call):
    user_id = call.from_user.id
    if is_user_subscribed(CHANNEL_ID, user_id):
        bot.answer_callback_query(call.id, "✅ تم تأكيد الاشتراك بنجاح!")
        bot.edit_message_text("شكرًا لاشتراكك! يمكنك الآن إرسال أي رسالة للبوت.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد، يرجى الاشتراك أولاً.", show_alert=True)

# تشغيل السيرفر الوهمي في الخلفية
Thread(target=run).start()

# تشغيل البوت الفعلي بشكل مستمر
if __name__ == '__main__':
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()
