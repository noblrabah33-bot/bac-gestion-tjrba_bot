import os
from threading import Thread
from flask import Flask
import telebot
from telebot import import types

# 1. إعداد البوت بتوكن خاص بك
BOT_TOKEN = "8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. معرف قناتك الإلزامية
CHANNEL_ID = "@TeamBacDZ"

# ومنع توقف البوت خادم وهمي لإرضاء منصة Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def is_user_subscribed(chat_id, user_id):
    try:
