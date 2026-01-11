import os
import time
import threading
import requests
import yt_dlp
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# --- [ ᴄᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ ] ---
API_ID = 20579940
API_HASH = "6fc0ea1c8dacae05751591adedc177d7"
BOT_TOKEN = "7832927526:AAHLt_pVQfGBXQ7DNEBu0Q_trgALvvCiUzY"
OWNER_IDS = [6703335929] # Ekhane aro ID add korte parbe [ID1, ID2]
B = "ᴅx"

# Render-e deploy korar por App URL ekhane obossoi dibe
URL = "https://dark-music-2.onrender.com" 

bot = Client("dx_advanced_pro", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return f"✨ {B} ᴀᴅᴠᴀɴᴄᴇᴅ ꜱʏꜱᴛᴇᴍ ɪꜱ ʀᴜɴɴɪɴɢ!"

# --- [ ᴀᴜᴛᴏ ᴀᴄᴛɪᴠᴇ / ꜱᴇʟꜰ-ᴘɪɴɢ ꜱʏꜱᴛᴇᴍ ] ---
def keep_alive():
    while True:
        try:
            # Bot nijei nijeke ping korbe jeno Render ghumai na jay
            requests.get(URL, timeout=10)
            print(f"🛰️ {B} ꜱʏꜱᴛᴇᴍ: ᴘɪɴɢ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ")
        except: 
            pass
        time.sleep(300) # 5 Minutes interval

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

# --- [ ᴠɪᴅᴇᴏ ᴅᴀᴛᴀ ᴇxᴛʀᴀᴄᴛᴏʀ ] ---
def get_video_details(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filesize = info.get('filesize') or info.get('filesize_approx') or 0
        size_mb = f"{filesize / (1024 * 1024):.2f} MB" if filesize > 0 else "𝚄𝚗𝚔𝚗𝚘𝚠𝚗"
        
        return {
            'title': info.get('title', 'ɴᴏ ᴛɪᴛʟᴇ'),
            'duration': time.strftime('%H:%M:%S', time.gmtime(info.get('duration', 0))),
            'resolution': info.get('resolution', '720p'),
            'size': size_mb
        }

def download_video(url):
    filename = f"dx_{int(time.time())}.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

# --- [ ʙᴏᴛ ʟᴏɢɪᴄ ᴡɪᴛʜ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴɪᴍᴀᴛɪᴏɴ ] ---

@bot.on_message(filters.command("start") & filters.user(OWNER_IDS))
async def start(client, message):
    await message.reply_text(
        f"👋 ʜᴇʟʟᴏ ᴍᴀꜱᴛᴇʀ,\n\n"
        f"🤖 ɪ ᴀᴍ ʏᴏᴜʀ <b>{B} ᴀᴅᴠᴀɴᴄᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ</b>\n"
        f"💎 ꜱᴛᴀᴛᴜꜱ: <code>ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ</code>\n"
        f"🛡️ ᴘᴏᴡᴇʀ: <code>ᴏᴡɴᴇʀ ᴀᴄᴄᴇꜱꜱ ᴏɴʟʏ</code>\n\n"
        f"📥 ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀ ʟɪɴᴋ ᴛᴏ ꜱᴛᴀʀᴛ!"
    )

@bot.on_message(filters.text & filters.user(OWNER_IDS))
async def handle_url(client, message: Message):
    url = message.text
    if not any(x in url for x in ["facebook.com", "fb.watch", "pin.it", "pinterest.com"]):
        return

    # --- [ ᴀɴɪᴍᴀᴛɪᴏɴ ꜱᴇǫᴜᴇɴᴄᴇ ] ---
    status = await message.reply_text(f"🔍 <code>{B} ꜱʏꜱᴛᴇᴍ: ɪᴅᴇɴᴛɪꜰʏɪɴɢ ᴜʀʟ...</code>")
    time.sleep(1)
    await status.edit(f"⚙️ <code>{B} ꜱʏꜱᴛᴇᴍ: ᴇxᴛʀᴀᴄᴛɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ...</code>")
    
    try:
        data = get_video_details(url)
        await status.edit(f"📥 <code>{B} ꜱʏꜱᴛᴇᴍ: ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰɪʟᴇ...</code>")
        
        file_path = download_video(url)
        platform = "ᴘɪɴᴛᴇʀᴇꜱᴛ" if "pin" in url else "ꜰᴀᴄᴇʙᴏᴏᴋ"
        
        # --- [ ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴀᴘᴛɪᴏɴ ] ---
        caption = (
            f"✅ <b>{B} ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ</b>\n\n"
            f"📝 <b>ᴛɪᴛʟᴇ:</b> <code>{data['title'][:50]}...</code>\n"
            f"⏱️ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{data['duration']}</code>\n"
            f"📺 <b>ǫᴜᴀʟɪᴛʏ:</b> <code>{data['resolution']}</code>\n"
            f"📦 <b>ꜱɪᴢᴇ:</b> <code>{data['size']}</code>\n"
            f"📡 <b>ᴘʟᴀᴛꜰᴏʀᴍ:</b> <code>{platform}</code>\n\n"
            f"🏷️ #ᴅx_ᴅᴏᴡɴʟᴏᴀᴅᴇʀ #ᴀᴅᴠᴀɴᴄᴇᴅ_ᴀɪ\n"
            f"✨ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ: <b>{B} ꜱʏꜱᴛᴇᴍ</b>"
        )

        await message.reply_video(
            video=file_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ ᴄʟᴇᴀʀ ᴄᴀᴄʜᴇ", callback_data="del")]])
        )
        await status.delete()
        
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await status.edit(f"❌ <b>{B} ᴇʀʀᴏʀ:</b> <code>ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇꜱꜱ ʟɪɴᴋ</code>")
        print(f"Error: {e}")

@bot.on_callback_query(filters.regex("del"))
async def delete_msg(client, callback_query):
    await callback_query.message.delete()

# --- [ ᴍᴀɪɴ ᴇxᴇᴄᴜᴛɪᴏɴ ] ---
if __name__ == "__main__":
    # Web server thread
    threading.Thread(target=run_web, daemon=True).start()
    # Keep-alive thread
    threading.Thread(target=keep_alive, daemon=True).start()
    
    print(f"--- {B} BOT IS RUNNING ON RENDER ---")
    bot.run()
