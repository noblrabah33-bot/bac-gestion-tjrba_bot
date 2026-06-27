import os
import sqlite3
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. إعداد البوت والآدمن
BOT_TOKEN = "8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4"
ADMIN_ID = 7414732163  # تم استخراج الآيدي الخاص بك لترقية صلاحياتك كمالك للبوت
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_ID = "@TeamBacDZ"
WELCOME_IMAGE_ID = "AgACAgQAAxkBAAPZaj8V7WPdrrse91QHxH02OZHm3ysAAmsNaxt6CvhRbhdA44-0VUoBAAMCAAN5AAM8BA"

# 2. إعداد قاعدة البيانات تلقائياً
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        conn.close()
        return True # مستخدم جديد فعلاً
    conn.close()
    return False # مسجل مسبقاً

def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

init_db()

app = Flask('')

@app.route('/')
def home():
    return "Bot is running and database is active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def is_user_subscribed(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return True

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
    except:
        bot.send_message(chat_id, caption_text, reply_markup=markup)

# أمر الإذاعة الجماعية (خاص بك أنت فقط كآدمن)
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    # أخذ النص المكتوب بعد أمر /broadcast
    text_to_send = message.text.replace("/broadcast", "").strip()
    if not text_to_send:
        bot.reply_to(message, "❌ يرجى كتابة نص الرسالة بعد الأمر. مثال:\n`/broadcast أهلاً بالجميع`", parse_mode="Markdown")
        return
    
    all_users = get_all_users()
    success_count = 0
    
    bot.reply_to(message, f"📢 جاري بدء الإذاعة إلى {len(all_users)} مستخدم...")
    
    for user in all_users:
        try:
            bot.send_message(user, text_to_send)
            success_count += 1
        except Exception as e:
            # إذا قام المستخدم بحظر البوت يتخطاه تلقائياً
            print(f"Could not send to {user}: {e}")
            
    bot.send_message(ADMIN_ID, f"✅ تم الانتهاء من الإذاعة بنجاح!\n\nوصلت الرسالة إلى: {success_count} طالب من أصل {len(all_users)}.")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    # حفظ المستخدم عند تفاعله وضغط الزر
    is_new = add_user(user_id, call.from_user.username)
    if is_new:
        try:
            bot.send_message(ADMIN_ID, f"🔔 **مستخدم جديد انضم للبوت!**\nالاسم: {call.from_user.first_name}\nالمعرف: @{call.from_user.username}")
        except:
            pass

    if is_user_subscribed(CHANNEL_ID, user_id):
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        send_main_menu(chat_id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد! يرجى الاشتراك أولاً ثم الضغط على الزر مجدداً.", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # حفظ وتخزين بيانات المستخدم في قاعدة البيانات فور إرساله رسالة
    is_new = add_user(user_id, message.from_user.username)
    
    # إذا كان مستخدم جديد، يرسل البوت إشعاراً خاصاً لك فوراً تنبيهاً بدخوله
    if is_new:
        try:
            bot.send_message(ADMIN_ID, f"🔔 **مستخدم جديد انضم للبوت!**\nالاسم: {message.from_user.first_name}\nالمعرف: @{message.from_user.username}")
        except:
            pass
    
    if not is_user_subscribed(CHANNEL_ID, user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton("📢 اضغط هنا للاشتراك في القناة", url="https://t.me/TeamBacDZ")
        btn_check = types.InlineKeyboardButton("🟢 التحقق من الاشتراك", callback_data="check_sub")
        markup.add(btn_channel, btn_check)
        
        bot.reply_to(
            message, 
            "يسعدنا انضمامك إلينا!\n\nللاستمرار، يرجى الاشتراك في القناة الرسمية أولًا، ثم اضغط على زر التحقق من الاشتراك بالأسفل لتبدأ استخدام البوت 👇", 
            reply_markup=markup
        )
        return

    send_main_menu(chat_id)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
