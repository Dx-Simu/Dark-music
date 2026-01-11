import os
import time
import requests
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# --- CONFIGURATION ---
API_ID = 20579940
API_HASH = "6fc0ea1c8dacae05751591adedc177d7"
BOT_TOKEN = "7832927526:AAHLt_pVQfGBXQ7DNEBu0Q_trgALvvCiUzY"
OWNER_ID = 6703335929
B = "ᴅx"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web_server = Flask(__name__)

@web_server.route('/')
def home():
    return "Bot is Running!"

def run_web():
    web_server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- BOT LOGIC ---

@app.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(client, message):
    welcome_text = (
        f"👋 ʜᴇʟʟᴏ ꜱɪʀ, ɪ ᴀᴍ ʏᴏᴜʀ ᴀᴅᴠᴀɴᴄᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ!\n\n"
        f"✨ ꜱᴛᴀᴛᴜꜱ: <code>ᴏɴʟɪɴᴇ</code>\n"
        f"🛡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ: <b>{B} ꜱʏꜱᴛᴇᴍ</b>\n\n"
        f"📥 ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀ ꜰᴀᴄᴇʙᴏᴏᴋ ᴏʀ ᴘɪɴᴛᴇʀᴇꜱᴛ ʟɪɴᴋ!"
    )
    await message.reply_text(welcome_text)

@app.on_message(filters.text & filters.user(OWNER_ID))
async def downloader(client, message: Message):
    url = message.text
    
    # URL Validation
    if "facebook.com" in url or "fb.watch" in url:
        platform = "ꜰᴀᴄᴇʙᴏᴏᴋ"
    elif "pinterest.com" in url or "pin.it" in url:
        platform = "ᴘɪɴᴛᴇʀᴇꜱᴛ"
    else:
        return await message.reply_text("❌ <code>Invalid URL! Please send FB or Pinterest link.</code>")

    editable = await message.reply_text(f"🔍 <b>{B} ꜱʏꜱᴛᴇᴍ ɪꜱ ᴀɴᴀʟʏᴢɪɴɢ...</b>")
    time.sleep(1)
    await editable.edit(f"📥 <b>{B} ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰʀᴏᴍ {platform}...</b>")

    try:
        # Using a public API for downloading (Replace with your preferred API if needed)
        api_url = f"https://api.vkrdown.com/api/item.php?url={url}"
        response = requests.get(api_url).json()
        
        video_url = response['data']['medias'][0]['url']
        caption = (
            f"✅ <b>{B} ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ!</b>\n\n"
            f"🌐 ᴘʟᴀᴛꜰᴏʀᴍ: <code>{platform}</code>\n"
            f"🔗 ᴜʀʟ: <a href='{url}'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n\n"
            f"✨ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ: <b>{B}</b>"
        )

        await message.reply_video(video=video_url, caption=caption)
        await editable.delete()

    except Exception as e:
        await editable.edit(f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{str(e)}</code>")

# --- KEEP ALIVE SYSTEM ---
def keep_alive():
    while True:
        try:
            # Replace 'your-app-name.onrender.com' with your actual Render URL
            requests.get("https://dark-music-1.onrender.com") 
        except:
            pass
        time.sleep(300) # Pings every 10 minutes

if __name__ == "__main__":
    # Start Web Server for Render
    threading.Thread(target=run_web, daemon=True).start()
    # Start Keep Alive
    threading.Thread(target=keep_alive, daemon=True).start()
    # Start Bot
    print(f"--- {B} BOT STARTED ---")
    app.run()
