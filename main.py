import os
import time
import threading
import requests
import yt_dlp
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# --- CONFIGURATION ---
API_ID = 20579940
API_HASH = "6fc0ea1c8dacae05751591adedc177d7"
BOT_TOKEN = "7832927526:AAHLt_pVQfGBXQ7DNEBu0Q_trgALvvCiUzY"
OWNER_ID = 6703335929
B = "ᴅx"
# Render-e deploy korar por oi URL-ta ekhane boshabe (e.g., https://mybot.onrender.com)
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://dark-music-2.onrender.com/")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "ᴅx ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ ᴀɴᴅ ʀᴜɴɴɪɴɢ!"

# --- SELF-KEEP-ALIVE SYSTEM ---
def keep_alive():
    """Bot nijei nijeke active rakhar jonno protite 10 min por ping korbe"""
    while True:
        try:
            # Render URL-e ping pathay
            requests.get(RENDER_EXTERNAL_URL)
            print(f"--- {B} ꜱʏꜱᴛᴇᴍ: ᴘɪɴɢ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ ---")
        except Exception as e:
            print(f"Ping Error: {e}")
        time.sleep(600) # 600 seconds = 10 minutes

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

# --- DOWNLOAD LOGIC ---
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- BOT HANDLERS ---
@app.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(client, message):
    await message.reply_text(f"🚀 <b>{B} ᴀᴅᴠᴀɴᴄᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ɪꜱ ʀᴜɴɴɪɴɢ!</b>\n\n✨ ꜱᴛᴀᴛᴜꜱ: <code>ᴀʟɪᴠᴇ & ᴀᴄᴛɪᴠᴇ</code>")

@app.on_message(filters.text & filters.user(OWNER_ID))
async def handle_url(client, message: Message):
    url = message.text
    if not ("facebook.com" in url or "fb.watch" in url or "pinterest.com" in url or "pin.it" in url):
        return

    status = await message.reply_text(f"🔄 <b>{B} ꜱʏꜱᴛᴇᴍ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ...</b>\n<code>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ</code>")
    
    try:
        platform = "ᴘɪɴᴛᴇʀᴇꜱᴛ" if "pin" in url else "ꜰᴀᴄᴇʙᴏᴏᴋ"
        file_path = download_video(url)
        
        caption = (
            f"✅ <b>{B} ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>\n\n"
            f"📡 ᴘʟᴀᴛꜰᴏʀᴍ: <code>{platform}</code>\n"
            f"🏷️ ᴛᴀɢ: #ᴅx_ᴅᴏᴡɴʟᴏᴀᴅ\n"
            f"🔗 ʟɪɴᴋ: <code>ꜱᴇᴄᴜʀᴇᴅ</code>"
        )

        await message.reply_video(video=file_path, caption=caption)
        await status.delete()
        if os.path.exists(file_path): os.remove(file_path)

    except Exception as e:
        await status.edit(f"❌ <b>{B} ᴇʀʀᴏʀ:</b> <code>ʟɪɴᴋ ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ</code>")

if __name__ == "__main__":
    # Web server thread
    threading.Thread(target=run_web, daemon=True).start()
    # Keep-alive thread
    threading.Thread(target=keep_alive, daemon=True).start()
    
    print(f"--- {B} BOT IS RUNNING ---")
    app.run()
