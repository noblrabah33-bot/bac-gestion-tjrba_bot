import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# قراءة التوكن من إعدادات Render (الأكثر أماناً)
TOKEN = os.getenv('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة نصية فقط (لضمان عمل البوت دون مشاكل الصورة)
    text = "مرحباً بك في بوت التسيير والاقتصاد! \n\nاشترك في القناة ليصلك كل جديد واستخدم التطبيق من الأزرار أدناه:"
    
    keyboard = [
        [InlineKeyboardButton("اشترك في القناة", url="https://t.me/bac_gestion7")],
        [InlineKeyboardButton("ادخل للتطبيق", url="https://t.me/Grdxesss_bot")],
        [InlineKeyboardButton("تواصل مع المطور", url="https://t.me/Nabil1r")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text=text, reply_markup=reply_markup)

if __name__ == '__main__':
    # بناء التطبيق
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # التشغيل
    print("البوت يعمل الآن...")
    app.run_polling()
