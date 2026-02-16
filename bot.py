from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

from pyrogram import Client, filters
import os
from handlers.upload_handler import upload_file
from handlers.rename_handler import rename_file
from handlers.admin_handler import promote_premium, stats
from utils.database import init_db

app = Client(
    "UploaderBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

init_db()

@app.on_message(filters.command("start"))
async def start(client, message):
    print("Received /start")
    await message.reply("👋 हेलो! मैं फाइल अपलोडर बॉट हूँ। कोई वीडियो या डॉक्युमेंट भेजें।")

@app.on_message(filters.document | filters.video)
async def handle_upload(client, message):
    await upload_file(client, message)

@app.on_message(filters.command("rename"))
async def handle_rename(client, message):
    await rename_file(client, message)

@app.on_message(filters.command("addpremium") & filters.user(int(os.getenv("OWNER_ID"))))
async def handle_premium(client, message):
    await promote_premium(client, message)

@app.on_message(filters.command("stats") & filters.user(int(os.getenv("OWNER_ID"))))
async def handle_stats(client, message):
    await stats(client, message)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()

import threading
import time

def heartbeat():
    while True:
        print("Bot is alive...")
        time.sleep(15)

threading.Thread(target=heartbeat, daemon=True).start()
