import telebot
from telebot import types

# 1. ضع توكن بوتك القادم من BotFather بين العلامتين
BOT_TOKEN = "8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. معرف قناتك الإلزامية
CHANNEL_ID = "@TeamBacDZ"

def is_user_subscribed(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not is_user_subscribed(CHANNEL_ID, user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton(text="📢 قناتنا الرسمية", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")
        btn_check = types.InlineKeyboardButton(text="✅ تحقق من الاشتراك", callback_data="check_subscription")
        markup.add(btn_channel, btn_check)
        
        bot.reply_to(
            message,
            f"🔻 للمتابعة واستخدام منصتنا بشكل عادي، يجب عليك الاشتراك في قناتنا الرسمية {CHANNEL_ID}.\n\nاشترك رجاءً واضغط على أيقونة 'التحقق من الاشتراك'.",
            reply_markup=markup
        )
        return

    show_main_menu(message.chat.id, first_name)

def show_main_menu(chat_id, first_name):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # يمكنك تعديل هذا الرابط لاحقاً برابط الـ PWA الخاص بك
    btn_web_app = types.InlineKeyboardButton(
        text="📥 الدخول إلى المنصة", 
        web_app=types.WebAppInfo(url="https://lovable.dev")
    )
    
    btn_share = types.InlineKeyboardButton(
        text="🤝 شاركني لصديق", 
        url=f"https://t.me/share/url?url=https://t.me/{bot.get_me().username}"
    )
    btn_visit_channel = types.InlineKeyboardButton(
        text="↗️ تابع قناتنا الرسمية", 
        url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"
    )
    
    markup.add(btn_web_app, btn_share, btn_visit_channel)
    
    bot.send_message(
        chat_id,
        f"🎉 مرحبًا بك يا {first_name} في المنصة التعليمية!\n\n🧠 يمكنك استخدام المنصة ببساطة عبر الزر الموجود في الأسفل أسفل هذه الرسالة 👇",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def callback_check_sub(call):
    user_id = call.from_user.id
    first_name = call.from_user.first_name

    if is_user_subscribed(CHANNEL_ID, user_id):
        bot.answer_callback_query(call.id, "✨ تم التحقق بنجاح! أهلاً بك.", show_alert=False)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id, first_name)
    else:
        bot.answer_callback_query(call.id, "❌ أنت غير مشترك في القناة بعد، رجاءً اشترك أولاً ثم اضغط تحقق.", show_alert=True)

if __name__ == "__main__":
    bot.infinity_polling()
