import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. إعداد البوت بالتوكن الصحيح الكامل الخاص بك
BOT_TOKEN = "8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. معرف قناتك الإلزامية
CHANNEL_ID = "@TeamBacDZ"

# خادم وهمي لإبقاء السيرفر نشطاً على Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# دالة التحقق من اشتراك المستخدم في القناة
def is_user_subscribed(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        # في حال حدوث خطأ (مثل عدم وجود البوت كأدمن)، نمرر المستخدم مؤقتاً لكي لا يتوقف البوت
        return True

# استقبال أمر /start والرسائل
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    
    if not is_user_subscribed(CHANNEL_ID, user_id):
        # رسالة الاشتراك الإلزامي إذا لم يكن مشتركاً
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اضغط هنا للاشتراك في القناة 📢", url=f"https://t.me/TeamBacDZ")
        markup.add(btn)
        
        bot.reply_to(
            message, 
            "⚠️ عذراً يا صديقي! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت المطور.\n\nاشترك ثم أعد إرسال /start", 
            reply_markup=markup
        )
    else:
        # الرد الطبيعي إذا كان مشتركاً
        if message.text == '/start':
            bot.reply_to(message, "أهلاً بك خويا! البوت جاهز لخدمتك الآن بنجاح مجاناً وبدون توقف. 🚀")
        else:
            bot.reply_to(message, "تم استقبال رسالتك بنجاح! السيرفر شغال والتوكن صحيح 100%. ✅")

# تشغيل خادم Flask في خلفية مستقلة
def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("تنبيه: بدأ البوت في استقبال الرسائل الآن...")
    bot.infinity_polling()
