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

bot = Client("dx_ultra_pro", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return f"🚀 <b>{B}</b> ᴜʟᴛʀᴀ ꜱʏꜱᴛᴇᴍ ɪꜱ ᴀʟɪᴠᴇ!"

# --- [ ᴀᴜᴛᴏ ᴀᴄᴛɪᴠᴇ ꜱʏꜱᴛᴇᴍ ] ---
def keep_alive():
    while True:
        try:
            requests.get(URL, timeout=10)
        except: pass
        time.sleep(300)

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

# --- [ 5-ENGINE PRO DOWNLOADER LOGIC ] ---
def download_video(url):
    filename = f"dx_{int(time.time())}.mp4"
    
    # 1. ʏᴛ-ᴅʟᴘ ᴇɴɢɪɴᴇ (Primary High Quality)
    try:
        ydl_opts = {'format': 'best', 'outtmpl': filename, 'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename, "ʏᴛ-ᴅʟᴘ ᴠ1"
    except: pass

    # 2. ᴠᴋʀ-ᴀᴘɪ ᴇɴɢɪɴᴇ (Social Media Backup)
    try:
        res = requests.get(f"https://api.vkrdown.com/api/item.php?url={url}", timeout=10).json()
        v_url = res['data']['medias'][0]['url']
        with requests.get(v_url, stream=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024): f.write(chunk)
        return filename, "ᴠᴋʀ-ᴀᴘɪ ᴠ2"
    except: pass

    # 3. ꜱɴᴀᴘ-ꜱᴀᴠᴇ ʟᴏɢɪᴄ (FB & Pinterest Special)
    try:
        # Simplified SnapSave alternative/backup logic
        res = requests.get(f"https://api.reveandyou.com/api/download?url={url}", timeout=10).json()
        v_url = res['data']['url']
        with requests.get(v_url, stream=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024): f.write(chunk)
        return filename, "ꜱɴᴀᴘ-ꜱᴀᴠᴇ ᴠ3"
    except: pass

    # 4. ʟᴏᴀᴅᴇʀ-ᴛᴏ ᴇɴɢɪɴᴇ (Universal Backup)
    try:
        res = requests.get(f"https://loader.to/api/button/?url={url}&f=mp4", timeout=10).json()
        v_url = res['url']
        with requests.get(v_url, stream=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024): f.write(chunk)
        return filename, "ʟᴏᴀᴅᴇʀ-ᴛᴏ ᴠ4"
    except: pass

    # 5. ᴅɪʀᴇᴄᴛ ꜱᴛʀᴇᴀᴍ ᴇɴɢɪɴᴇ (Emergency)
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        if "video" in r.headers.get('content-type', ''):
            with open(filename, 'wb') as f: f.write(r.content)
            return filename, "ᴅɪʀᴇᴄᴛ-ꜱᴛʀᴇᴀᴍ ᴠ5"
    except: pass

    return None, None

# --- [ ʙᴏᴛ ʟᴏɢɪᴄ ᴡɪᴛʜ ᴘʀᴇᴍɪᴜᴍ ʜᴛᴍʟ ꜱᴛʏʟᴇ ] ---

@bot.on_message(filters.command("start") & filters.user(OWNER_IDS))
async def start(client, message):
    text = (
        f"👋 <b>ʜᴇʟʟᴏ ᴍᴀꜱᴛᴇʀ,</b>\n\n"
        f"🤖 <b>ɪ ᴀᴍ ʏᴏᴜʀ</b> <b>{B}</b> <b>ᴜʟᴛʀᴀ ʙᴏᴛ</b>\n"
        f"💎 <b>ꜱᴛᴀᴛᴜꜱ:</b> <code>ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ</code>\n"
        f"🛡️ <b>ᴘᴏᴡᴇʀ:</b> <code>ᴏᴡɴᴇʀ ᴏɴʟʏ</code>\n"
        f"⚙️ <b>ᴇɴɢɪɴᴇꜱ:</b> <code>5 ᴘᴏᴡᴇʀꜰᴜʟ ᴍᴇᴛʜᴏᴅꜱ</code>\n\n"
        f"📥 <b>ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀ ʟɪɴᴋ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ!</b>"
    )
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"✨ {B} ꜱʏꜱᴛᴇᴍ", url=URL)]]))

@bot.on_message(filters.text & filters.user(OWNER_IDS))
async def handle_url(client, message: Message):
    url = message.text
    if not any(x in url for x in ["facebook.com", "fb.watch", "pin.it", "pinterest.com"]):
        return

    # --- ᴀɴɪᴍᴀᴛɪᴏɴ ---
    status = await message.reply_text(f"🔍 <b>{B}</b> <b>ꜱʏꜱᴛᴇᴍ:</b> <code>ɪᴅᴇɴᴛɪꜰʏɪɴɢ...</code>")
    time.sleep(0.8)
    await status.edit(f"⚙️ <b>{B}</b> <b>ꜱʏꜱᴛᴇᴍ:</b> <code>ᴄʜᴇᴄᴋɪɴɢ ᴇɴɢɪɴᴇꜱ...</code>")
    time.sleep(0.8)
    await status.edit(f"📥 <b>{B}</b> <b>ꜱʏꜱᴛᴇᴍ:</b> <code>ᴇxᴛʀᴀᴄᴛɪɴɢ ᴍᴇᴅɪᴀ...</code>")
    
    file_path, engine = download_video(url)
    
    if file_path:
        await status.edit(f"🚀 <b>{B}</b> <b>ꜱʏꜱᴛᴇᴍ:</b> <code>ꜱᴇɴᴅɪɴɢ ᴛᴏ ᴍᴀꜱᴛᴇʀ...</code>")
        platform = "ᴘɪɴᴛᴇʀᴇꜱᴛ" if "pin" in url else "ꜰᴀᴄᴇʙᴏᴏᴋ"
        
        caption = (
            f"✅ <b>{B}</b> <b>ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ</b>\n\n"
            f"📡 <b>ᴘʟᴀᴛꜰᴏʀᴍ:</b> <code>{platform}</code>\n"
            f"⚙️ <b>ᴇɴɢɪɴᴇ:</b> <code>{engine}</code>\n"
            f"🏷️ <b>ᴛᴀɢ:</b> <code>#ᴅx_ᴜʟᴛʀᴀ_ᴅᴏᴡɴʟᴏᴀᴅ</code>\n\n"
            f"✨ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ:</b> <b>{B}</b> <b>ꜱʏꜱᴛᴇᴍ ᴀɪ</b>"
        )

        await message.reply_video(video=file_path, caption=caption)
        await status.delete()
        if os.path.exists(file_path): os.remove(file_path)
    else:
        await status.edit(f"❌ <b>{B}</b> <b>ᴇʀʀᴏʀ:</b> <code>ᴀʟʟ 5 ᴇɴɢɪɴᴇꜱ ꜰᴀɪʟᴇᴅ!</code>")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    
    while True:
        try:
            bot.run()
            break
        except FloodWait as e:
            time.sleep(e.value + 1)
        except Exception:
            time.sleep(10)
