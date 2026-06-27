from http.server import BaseHTTPRequestHandler
import json
import requests

TOKEN = "8985389453:AAFMC94DtQks9GPXcwLPtm_beOBnYwpJle4"
URL = f"https://api.telegram.org/bot{TOKEN}/"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                self.send_message(chat_id, "أهلاً بك في بوت إدارة البكالوريا! كيف يمكنني مساعدتك؟")

        self.send_response(200)
        self.end_headers()
        return

    def send_message(self, chat_id, text):
        requests.post(URL + "sendMessage", json={"chat_id": chat_id, "text": text})

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Bot is active!'.encode('utf-8'))
        return
