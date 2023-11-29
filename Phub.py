import os
import yt_dlp as ytdl
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from pyrogram.handlers import MessageHandler
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download
from ytdl.utils import DownloadError
from config import OWNER, BOT_NAME, REPO_BOT, X_API_KEY, UPDATES_CHANNEL, TOKEN
# Config Check-----------------------------------------------------------------

# ARQ API and Bot Initialize---------------------------------------------------
#async def main():
session = ClientSession()
arq = ARQ("https://arq.hamker.dev", "FIJROI-HUFQMF-REBCXR-EYQJFC-ARQ", session)
pornhub = arq.pornhub

app = Client(f"{BOT_NAME}", bot_token=f"{TOKEN}", api_id=25803426,
             api_hash="291b6bea4848d7606c0d3213c317b430")
print("\nʙᴏᴛ ʀᴇᴀᴅʏ ᴛᴏ ᴜsᴇ\n")


db = {}
async def down_data(item):
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"(title)s.mp4",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,

        "nocheckcertificate": True,
    }

    with ytdl(ydl_opts) as ydl:
            video = ydl.extract_info(item, download=True)
            return ydl.prepare_filename(video)

async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file

async def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
# Start  -----------------------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(_,message):
    m= await message.reply_text(
        text=f"🇬🇧 Hello, i'm {BOT_NAME}. you can download pornhub video with the quality up to 1080p, Just type a query or the video name you want to download and the bot will send you the result!\n\n🇮🇩 Halo, saya {BOT_NAME}, anda dapat mengunduh video dari pornhub dengan kualitas tinggi sampai 1080p, berikan saja nama/judul video yang ingin anda unduh maka saya akan memberikan hasil nya kepada anda.",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("📣 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=f"t.me/{UPDATES_CHANNEL}")
            ]
          ]
        )
    )

# Help-------------------------------------------------------------------------
@app.on_message(filters.command("help"))
async def help(_,message):
    await message.reply_text(
        """**🛠 available command:**
        
/help see the help message.\n
/repo get the repo link.\n

If you want to download phub video, just type any query."""
    )
    
# Repo  -----------------------------------------------------------------------
@app.on_message(filters.command("repo"))
async def repo(_, message):
    m= await message.reply_text(
        text="""Great, you can make your own bot now, tap the button below to get the repository link.""",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("🧩 ʀᴇᴘᴏ 🧩", url=f"{REPO_BOT}"),
              InlineKeyboardButton("👩‍💻 ᴏᴡɴᴇʀ 👩‍💻", url=f"t.me/{OWNER}")
              
              ]
            ]
          )
       )

# Let's Go----------------------------------------------------------------------
@app.on_message(filters.private)
async def search(_,message):
    try:
        if "/" in message.text.split(None,1)[0]:
            await message.reply_text(
                "**💡 usage:**\njust type the phub video name you want to download, and this bot will send you the result."
            )
            return
    except Exception:
        pass
    m = await message.reply_text("getting results...")
    search = message.text
    try:
        resp = await pornhub(search,thumbsize="large")
        res = resp.result
    except Exception as e:
     await message.reply(e)
     await m.edit("not found: 404")
     return
    if not resp.ok:
        await m.edit("not found, try again")
        return
    result = f"""
**🏷 ᴛɪᴛʟᴇ:** {res[0].title}
**⏰ ᴅᴜʀᴀᴛɪɪɴ:** {res[0].duration}
**👁‍🗨 ᴠɪᴇᴡᴇʀs:** {res[0].views}
**🌟 ʀᴀᴛɪɴɢ:** {res[0].rating}"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▶️ ɴᴇxᴛ",
                                         callback_data="next"),
                    InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ",
                                         callback_data="dload")
                ]
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except Exception:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("◀️ ᴘʀᴇᴠɪᴏᴜs",
                                         callback_data="previous"),
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ",
                                         callback_data="dload"),
                ],
                [
                    InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ",
                                         callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("◀️ ᴘʀᴇᴠɪᴏᴜs",
                                         callback_data="previous"),
                    InlineKeyboardButton("▶️ ɴᴇxᴛ",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ",
                                         callback_data="dload")
                ]
              ]
    result = f"""
**🏷 ᴛɪᴛʟᴇ:** {res[cur_page].title}
**⏰ ᴅᴜʀᴀᴛɪᴏɴ:** {res[curr_page].duration}
**👁‍🗨 ᴠɪᴇᴡᴇʀs:** {res[cur_page].views}
**🌟 ʀᴀᴛɪɴɢ:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except Exception:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("◀️ ᴘʀᴇᴠɪᴏᴜs",
                                         callback_data="previous"),
                    InlineKeyboardButton("▶️ ɴᴇxᴛ",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ",
                                         callback_data="dload")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("▶️ ɴᴇxᴛ",
                                         callback_data="next"),
                    InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ",
                                         callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ",
                                         callback_data="dload")
                ]
            ]
    result = f"""
**🏷 ᴛɪᴛʟᴇ:** {res[cur_page].title}
**⏰ ᴅᴜʀᴀᴛɪᴏɴ:** {res[curr_page].duration}
**👁‍🗨 ᴠɪᴇᴡᴇʀs:** {res[cur_page].views}
**🌟 ʀᴀᴛɪɴɢ:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("dload"))
async def callback_query_next(_, query):
    m = query.message
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    dl_links = await down_data(res[curr_page].url)
    db[m.chat.id]['result'] = dl_links.result.video
    db[m.chat.id]['thumb'] = res[curr_page].thumbnails[0].src
    db[m.chat.id]['dur'] = res[curr_page].duration
    result = f"""
**🏷 ᴛɪᴛʟᴇ:** {res[curr_page].title}
**⏰ ᴅᴜʀᴀᴛɪᴏɴ:** {res[curr_page].duration}
**👁‍🗨 ᴠɪᴇᴡᴇʀs:** {res[curr_page].views}
**🌟 ʀᴀᴛɪɴɢ:** {res[curr_page].rating}"""
    pos = 1
    cbb = []
    for results in dl_links.result.video:
        b= [InlineKeyboardButton(f"{resolts.quality} - {resolts.size}", callback_data=f"phubdl {pos}")]
        pos += 1
        cbb.append(b)
    cbb.append([InlineKeyboardButton("Delete", callback_data="delete")])
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button 2--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex(r"^phubdl"))
async def callback_query_dl(_, query):
    m = query.message
    capsion = m.caption
    entoty = m.caption_entities
    await m.edit(f"**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...** :\n\n{capsion}")
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    thomb = await download_url(data['thumb'])
    durr = await time_to_seconds(data['dur'])
    pos = int(query.data.split()[1])
    pos = pos-1
    try:
        vid = await download_url(res[pos].url)
    except Exception as e:
        print(e)
        await m.edit("download error..., try again")
        return
    await m.edit(f"**ᴜᴘʟᴏᴀᴅ sᴇᴋᴀʀᴀɴɢ** :\n\n{capsion}")
    await app.send_chat_action(m.chat.id, "upload_video")
    await m.edit_media(media=InputMediaVideo(vid,thumb=thomb, duration=durr, supports_streaming=True))
    await m.edit_caption(caption=capsion, caption_entities=entoty)
    if os.path.isfile(vid):
        os.remove(vid)
    if os.path.isfile(thomb):
        os.remove(thomb)
    
# Delete Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, query):
    await query.message.delete()
    
app.run()
