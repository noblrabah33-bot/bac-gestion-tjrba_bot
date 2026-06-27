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

# دالة لإرسال القائمة الرئيسية مع صورتك الاحترافية
def send_main_menu(chat_id):
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
        bot.send_photo(chat_id, WELCOME_IMAGE_ID, caption=caption_text, reply_markup=markup)
    except Exception as e:
        print(f"Error sending photo: {e}")
        bot.send_message(chat_id, caption_text, reply_markup=markup)

# معالج الضغط على الأزرار الشفافة (التفاعل مع زر التحقق)
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if is_user_subscribed(CHANNEL_ID, user_id):
        # حذف رسالة الاشتراك القديمة لإبقاء المحادثة نظيفة
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        # إرسال القائمة الرئيسية فوراً
        send_main_menu(chat_id)
    else:
        # إظهار تنبيه داخلي للمستخدم بأنه لم يشترك بعد
        bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد! يرجى الاشتراك أولاً ثم الضغط على الزر مجدداً.", show_alert=True)

# استقبال كل الرسائل النصية المعتادة
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # التحقق من الاشتراك الإلزامي
    if not is_user_subscribed(CHANNEL_ID, user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton("اضغط هنا للاشتراك في القناة 📢", url="https://t.me/TeamBacDZ")
        btn_check = types.InlineKeyboardButton("🔄 التحقق من الاشتراك", callback_data="check_sub")
        markup.add(btn_channel, btn_check)
        
        bot.reply_to(
            message, 
            "يسعدنا انضمامك إلينا!\n\nللاستمرار، يرجى الاشتراك في القناة الرسمية أولًا، ثم اضغط على زر التحقق من الاشتراك بالأسفل لتبدأ استخدام البوت 👇", 
            reply_markup=markup
        )
        return

    # إذا كان مشتركاً بالفعل، تظهر القائمة الرئيسية مباشرة
    send_main_menu(chat_id)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
