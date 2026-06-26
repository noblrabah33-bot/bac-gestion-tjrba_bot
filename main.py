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

# رابط الصورة التي ستظهر مع الرسالة (يمكنك استبدال هذا الرابط برابط صورتك مستقبلاً)
WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1616469829581-73993eb86b02?q=80&w=600&auto=format&fit=crop"

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
        print(f"Error checking subscription: {e}")
        return True

# استقبال كل الرسائل
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

    # ثانياً: إذا كان مشتركاً، تظهر له القائمة الخاصة بك بالصورة والأزرار في كل مرة
    
    # إنشاء أزرار القائمة المخصصة مع الإيموجي الملون بديل الألوان
    markup = types.InlineKeyboardMarkup(row_width=1) # لجعل كل زر في سطر منفصل ومنظم
    
    # يمكنك تعديل الروابط (url) أدناه لتوجيه المستخدم لروابط تطبيقك ومجموعاتك الحقيقية
    btn_app = types.InlineKeyboardButton("🟢 ادخل للتطبيق", url="https://t.me/TeamBacDZ")
    btn_share = types.InlineKeyboardButton("🔵 شارك التطبيق مع زملائك", url="https://t.me/share/url?url=https://t.me/TeamBacDZ")
    btn_group = types.InlineKeyboardButton("🟡 انضم لمجموعة المناقشة", url="https://t.me/TeamBacDZ")
    btn_admin = types.InlineKeyboardButton("🔴 تواصل مع المشرف", url="https://t.me/noblrabah33") # ضع معرف حسابك هنا مكان noblrabah33
    
    markup.add(btn_app, btn_share, btn_group, btn_admin)
    
    caption_text = (
        "✨ أهلاً بك في خدماتنا المتطورة! ✨\n\n"
        "يسعدنا تواجدك معنا، يرجى اختيار الخدمة التي تريدها من الأزرار أدناه للبدء فوراً:"
    )
    
    try:
        # إرسال الصورة ومعها النص والأزرار الشفافة تحته
        bot.send_photo(message.chat.id, WELCOME_IMAGE_URL, caption=caption_text, reply_markup=markup)
    except Exception as e:
        # حل احتياطي في حال فشل تحميل رابط الصورة، يرسل نصاً فقط لكي لا يتوقف البوت
        bot.send_message(message.chat.id, caption_text, reply_markup=markup)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
