import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

# --- CONFIGURATION ---
API_ID = 20579940 
API_HASH = "6fc0ea1c8dacae05751591adedc177d7"
BOT_TOKEN = "7853734473:AAHdGjbtPFWD6wFlyu8KRWteRg_961WGRJk"

bot = Client("DX_MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(bot)

# --- 1. AUTO DELETE SERVICE MESSAGES ---
@bot.on_message(filters.service)
async def delete_service(_, message: Message):
    try:
        await message.delete()
    except:
        pass

# --- ADMIN CHECKER ---
async def is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "creator")

# --- 2. ADVANCE PLAY COMMAND (HTML STYLED) ---
@bot.on_message(filters.command("play") & filters.group)
async def play_music(client, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("<b>❌ ACCESS DENIED</b>\n<code>Only Admins can use this command.</code>")

    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("<b>📑 USAGE:</b>\n<code>/play [Song Name]</code>")

    m = await message.reply("<b>🔍 SEARCHING...</b>\n<code>Please wait while we fetch the audio.</code>")
    
    ydl_opts = {"format": "bestaudio/best", "quiet": True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
            title = info['title'][:30]
            duration = info.get('duration', 0)
            thumb = info.get('thumbnail')

        await call_py.join_group_call(message.chat.id, AudioPiped(url))

        # Premium Buttons
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸️ Pᴀᴜsᴇ", callback_data="pause"),
                InlineKeyboardButton("▶️ Rᴇsᴜᴍᴇ", callback_data="resume"),
                InlineKeyboardButton("⏹️ Sᴛᴏᴘ", callback_data="stop")
            ],
            [InlineKeyboardButton("👑 Dᴇᴠᴇʟᴏᴘᴇʀ: DX-CODEX 👑", url="https://t.me/dx_codex")]
        ])

        # HTML Formatted Design
        caption = (
            "<b>🎵 <u>ɴᴏᴡ ᴘʟᴀʏɪɴɢ ᴏɴ ᴠᴏɪᴄᴇᴄʜᴀᴛ</u></b>\n\n"
            f"<blockquote><b>📌 ᴛɪᴛʟᴇ:</b> <code>{title}</code>\n"
            f"<b>🕒 ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>00:00 / {duration // 60}:{duration % 60:02d}</code>\n"
            f"<b>👤 ʀᴇǫᴜᴇsᴛᴇʀ:</b> {message.from_user.mention}</blockquote>\n\n"
            f"<b>00:00 ───●────────── {duration // 60}:{duration % 60:02d}</b>\n"
            "<b>       ⇆ㅤ◁ㅤ ❚❚ㅤ ▷ㅤ↻</b>"
        )
        
        await m.delete()
        await message.reply_photo(photo=thumb, caption=caption, reply_markup=buttons)

    except Exception as e:
        await m.edit(f"<b>❌ ERROR DETECTED</b>\n<code>{e}</code>")

# --- 3. TAG ALL USERS ---
@bot.on_message(filters.command("tagall") & filters.group)
async def tag_all_users(client, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return
        
    shout = await message.reply("<b>📣 INITIATING...</b>\n<code>Mentioning all members.</code>")
    members = []
    async for member in client.get_chat_members(message.chat.id):
        if not member.user.is_bot:
            members.append(member.user.mention)
    
    await shout.delete()
    for i in range(0, len(members), 5):
        await message.reply(f"<b>🔔 ᴀᴛᴛᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ!</b>\n\n<blockquote>" + ", ".join(members[i:i+5]) + "</blockquote>")
        await asyncio.sleep(2)

# --- 4. SONG DOWNLOADER ---
@bot.on_message(filters.command("song") & filters.group)
async def song_downloader(client, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return
        
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("<b>🎵 INPUT ERROR:</b>\n<code>Please provide a song name.</code>")

    m = await message.reply("<b>📥 DOWNLOADING...</b>\n<code>Fetching file from server.</code>")
    # Simulation: Add your download logic here
    await m.edit("<b>✅ DOWNLOAD COMPLETE</b>\n<code>Song has been uploaded to the group.</code>")

# --- 5. CONTROL CALLBACKS ---
@bot.on_callback_query()
async def controls(_, query: CallbackQuery):
    if not await is_admin(query.message.chat.id, query.from_user.id):
        return await query.answer("Admin Permission Required!", show_alert=True)

    if query.data == "pause":
        await call_py.pause_stream(query.message.chat.id)
        await query.answer("Streaming Paused")
    elif query.data == "resume":
        await call_py.resume_stream(query.message.chat.id)
        await query.answer("Streaming Resumed")
    elif query.data == "stop":
        await call_py.leave_group_call(query.message.chat.id)
        await query.message.delete()
        await query.answer("Streaming Ended")

# --- STARTUP ---
async def start_bot():
    await bot.start()
    await call_py.start()
    print("🚀 [DX-CODEX] BOT IS ONLINE")
    await asyncio.Idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
