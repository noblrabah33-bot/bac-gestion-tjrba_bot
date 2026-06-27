from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '8985389453:AAF1w50e2nIieAAK39lu5T1qq8Rzpbc0OF4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إرسال الصورة مع الأزرار
    photo_url = "AgACAgQAAxkBAAEfyRtqPy2mGD_j3zFUBhicy68sdmyy9QACeQ1rG3oK-FG-ci9P3ZZQRwEAAwIAA3kAAzwE"
    keyboard = [
        [InlineKeyboardButton("اشترك في القناة", url="https://t.me/bac_gestion7")],
        [InlineKeyboardButton("ادخل للتطبيق", url="https://t.me/Grdxesss_bot")],
        [InlineKeyboardButton("تواصل مع المطور", url="https://t.me/Nabil1r")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=photo_url,
        caption="مرحباً بك! اشترك في القناة ليصلك كل جديد واستخدم التطبيق.",
        reply_markup=reply_markup
    )

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
