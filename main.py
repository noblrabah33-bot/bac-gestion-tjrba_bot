import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. إعداد البوت بالتوكن الخاص بك
BOT_TOKEN = "8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. معرف قناتك الإلزامية
CHANNEL_ID = "@TeamBacDZ"

# الرمز السري المضمون لـ صورتك الرسمية داخل تليجرام
WELCOME_IMAGE_ID = "AgACAgQAAxkBAAPZaj8V7WPdrrse91QHxH02OZHm3ysAAmsNaxt6CvhRbhdA44-0VUoBAAMCAAN5AAM8BA"

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
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return True

# استقبال كل الرسائل النصية
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    
    # أولاً: التحقق من الاشتراك الإلزامي
    if not is_user_subscribed(CHANNEL_ID, user_id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اضغط هنا للاشتراك في القناة 📢", url=f"https://t.me/TeamBacDZ")
        markup.add(btn)
        
        bot.reply_to(
            message, 
            "⚠️ عذراً يا صديقي! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت المطور.\n\nاشترك ثم أعد إرسال /start", 
            reply_markup=markup
        )
        return

    # ثانياً: القائمة بالأزرار والصورة الرسمية الخاصة بك (باستخدام الـ file_id المضمون)
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_app = types.InlineKeyboardButton("🟢 ادخل للتطبيق", url="https://t.me/TeamBacDZ")
    btn_share = types.InlineKeyboardButton("🔵 شارك التطبيق مع زملائك", url="https://t.me/share/url?url=https://t.me/TeamBacDZ")
    btn_group = types.InlineKeyboardButton("🟡 انضم لمجموعة المناقشة", url="https://t.me/TeamBacDZ")
    btn_admin = types.InlineKeyboardButton("🔴 تواصل مع المشرف", url="https://t.me/noblrabah33")
    
    markup.add(btn_app, btn_share, btn_group, btn_admin)
    
    caption_text = (
        "✨ أهلاً بك في منصة Team BAC Gestion المطور! ✨\n\n"
        "يسعدنا تواجدك معنا، يرجى اختيار الخدمة التي تريدها من الأزرار أدناه للبدء فوراً:"
    )
    
    try:
        # إرسال الصورة الرسمية باستخدام الـ ID لسرعة وظهور مضمون 100%
        bot.send_photo(message.chat.id, WELCOME_IMAGE_ID, caption=caption_text, reply_markup=markup)
    except Exception as e:
        print(f"Error sending photo: {e}")
        bot.send_message(message.chat.id, caption_text, reply_markup=markup)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
