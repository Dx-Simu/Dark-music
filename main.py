import os
import time
import threading
import requests
import yt_dlp
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# --- [ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ] ---
API_ID = 20579940
API_HASH = "6fc0ea1c8dacae05751591adedc177d7"
BOT_TOKEN = "7832927526:AAHLt_pVQfGBXQ7DNEBu0Q_trgALvvCiUzY"
OWNER_IDS = [6703335929] 
B = "ᴅx"
URL = "https://dark-music-2.onrender.com" 

bot = Client("dx_pro_downloader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return f"✨ {B} ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜʟᴛɪ-ᴇɴɢɪɴᴇ ɪꜱ ᴀʟɪᴠᴇ!"

# --- [ ᴋᴇᴇᴘ ᴀʟɪᴠᴇ ] ---
def keep_alive():
    while True:
        try:
            requests.get(URL, timeout=10)
            print(f"🛰️ {B} ꜱʏꜱᴛᴇᴍ: ꜱᴇʟꜰ-ᴘɪɴɢ ᴅᴏɴᴇ")
        except: pass
        time.sleep(300)

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

# --- [ ᴍᴜʟᴛɪ-ᴍᴇᴛʜᴏᴅ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ] ---
def download_video(url):
    filename = f"dx_{int(time.time())}.mp4"
    
    # Method 1: yt-dlp (Primary)
    try:
        ydl_opts = {'format': 'best', 'outtmpl': filename, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename, "ʏᴛ-ᴅʟᴘ"
    except:
        # Method 2: External API (Backup)
        try:
            api_url = f"https://api.vkrdown.com/api/item.php?url={url}"
            res = requests.get(api_url).json()
            video_url = res['data']['medias'][0]['url']
            r = requests.get(video_url, stream=True)
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: f.write(chunk)
            return filename, "ᴠᴋʀ-ᴀᴘɪ"
        except:
            return None, None

# --- [ ʙᴏᴛ ʟᴏɢɪᴄ ] ---

@bot.on_message(filters.command("start") & filters.user(OWNER_IDS))
async def start(client, message):
    await message.reply_text(
        f"👋 ʜᴇʟʟᴏ ᴍᴀꜱᴛᴇʀ,\n\n"
        f"🤖 ɪ ᴀᴍ ʏᴏᴜʀ <b>{B} ᴍᴜʟᴛɪ-ᴇɴɢɪɴᴇ ʙᴏᴛ</b>\n"
        f"💎 ꜱᴛᴀᴛᴜꜱ: <code>ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ</code>\n"
        f"🛡️ ᴘᴏᴡᴇʀ: <code>ᴏᴡɴᴇʀ ᴀᴄᴄᴇꜱꜱ ᴏɴʟʏ</code>\n\n"
        f"📥 ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰʙ ᴏʀ ᴘɪɴᴛᴇʀᴇꜱᴛ ʟɪɴᴋ!"
    )

@bot.on_message(filters.text & filters.user(OWNER_IDS))
async def handle_url(client, message: Message):
    url = message.text
    if not any(x in url for x in ["facebook.com", "fb.watch", "pin.it", "pinterest.com"]):
        return

    status = await message.reply_text(f"🔍 <code>{B} ꜱʏꜱᴛᴇᴍ: ɪᴅᴇɴᴛɪꜰʏɪɴɢ...</code>")
    time.sleep(1)
    await status.edit(f"⚙️ <code>{B} ꜱʏꜱᴛᴇᴍ: ᴇxᴛʀᴀᴄᴛɪɴɢ ᴅᴀᴛᴀ...</code>")
    
    file_path, engine = download_video(url)
    
    if file_path:
        await status.edit(f"📥 <code>{B} ꜱʏꜱᴛᴇᴍ: ꜱᴇɴᴅɪɴɢ ᴠɪᴅᴇᴏ...</code>")
        platform = "ᴘɪɴᴛᴇʀᴇꜱᴛ" if "pin" in url else "ꜰᴀᴄᴇʙᴏᴏᴋ"
        
        caption = (
            f"✅ <b>{B} ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ</b>\n\n"
            f"📡 ᴘʟᴀᴛꜰᴏʀᴍ: <code>{platform}</code>\n"
            f"⚙️ ᴇɴɢɪɴᴇ: <code>{engine}</code>\n"
            f"🏷️ #ᴅx_ᴀᴅᴠᴀɴᴄᴇᴅ_ᴅᴏᴡɴʟᴏᴀᴅ\n\n"
            f"✨ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ: <b>{B} ꜱʏꜱᴛᴇᴍ</b>"
        )

        await message.reply_video(video=file_path, caption=caption)
        await status.delete()
        if os.path.exists(file_path): os.remove(file_path)
    else:
        await status.edit(f"❌ <b>{B} ᴇʀʀᴏʀ:</b> <code>ᴀʟʟ ᴇɴɢɪɴᴇꜱ ꜰᴀɪʟᴇᴅ!</code>")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    
    while True:
        try:
            bot.run()
            break
        except FloodWait as e:
            time.sleep(e.value + 1)
        except Exception as e:
            time.sleep(10)
