import os
from flask import Flask, request
import telebot

# التوكن المحدث والخاص ببوتك
API_TOKEN = '8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4'
bot = telebot.TeleBot(API_TOKEN, threaded=False)

app = Flask(__name__)

# معرف قناتك الإلزامية المشترطة للاشتراك
CHANNEL_USERNAME = "@TeamBacDZ"

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            return True
        return False
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if check_subscription(user_id):
        # لوحة أزرار تحتوي على الزر الشفاف (رابط التطبيق المصغر)
        markup = telebot.types.InlineKeyboardMarkup()
        # هنا يمكنك مستقبلاً استبدال الرابط برابط تطبيقك المصغر (PWA) الخاص بـ Team BAC Gestion
        app_button = telebot.types.InlineKeyboardButton(
            text="📱 فتح التطبيق المصغر", 
            url="https://t.me/your_bot/app"
        )
        markup.add(app_button)
        
        bot.reply_to(message, "أهلاً بك في منصة إدارة واقتصاد! يمكنك فتح التطبيق الآن:", reply_markup=markup)
    else:
        # رسالة الاشتراك الإجباري
        markup = telebot.types.InlineKeyboardMarkup()
        btn_join = telebot.types.InlineKeyboardButton(text="📢 اشترك في القناة أولاً", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        btn_check = telebot.types.InlineKeyboardButton(text="✅ تحقق من الاشتراك", callback_data="check_sub")
        markup.add(btn_join)
        markup.add(btn_check)
        bot.reply_to(message, f"عذراً يا صديقي، يجب عليك الاشتراك في قناة المنصة أولاً لاستخدام البوت:\n{CHANNEL_USERNAME}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check_sub(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح! أرسل /start الآن.")
        bot.edit_message_text("شكرًا لاشتراكك! أرسل أمر /start لتشغيل المنصة.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد!", show_alert=True)

# النقطة التي يستقبل فيها سيرفر Vercel طلبات تليجرام (POST)
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid Request', 403

# واجهة برمجية بسيطة للتأكد من عمل السيرفر عند فتحه من المتصفح (GET)
@app.route('/', methods=['GET'])
def index():
    return "Bot is running perfectly on Vercel!", 200
