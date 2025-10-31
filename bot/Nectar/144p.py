import logging

logging.getLogger("pymongo").setLevel(logging.INFO)
logging.getLogger("motor").setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

from datetime import datetime as dt
import os, asyncio, pyrogram, psutil, platform
from bot import (
    APP_ID,
    API_HASH,
    AUTH_USERS,
    DOWNLOAD_LOCATION,
    LOGGER,
    TG_BOT_TOKEN,
    BOT_USERNAME,
    SESSION_NAME,
    data,
    app
)
from bot.helper_funcs.utils import add_task, on_task_complete, sysinfo
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message
from psutil import disk_usage, cpu_percent, virtual_memory, Process as psprocess

from bot.plugins.incoming_message_fn import (
    incoming_start_message_f,
    incoming_compress_message_f,
    incoming_cancel_message_f
)

from bot.plugins.status_message_fn import (
    eval_message_f,
    exec_message_f,
    upload_log_file
)

from bot.commands import Command
from bot.plugins.call_back_button_handler import button
from helper.database import db
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pymongo.errors import PyMongoError


uptime = dt.now()

@app.on_message(filters.incoming & filters.command(["crf1", f"crf1@{BOT_USERNAME}"]))
async def changecrf(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            cr = message.text.split(" ", maxsplit=1)[1]
            cr_int = int(cr)  # Validate as integer
            await db.set_crf1(cr_int)
            OUT = f"<blockquote>I will be using : {cr} crf</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide a CRF value, e.g., /crf1 24</blockquote>")
        except ValueError:
            await message.reply_text("<blockquote>CRF must be an integer, e.g., 24</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save CRF value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /crf1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /crf1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["resolution1", f"resolution1@{BOT_USERNAME}"]))
async def changer(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            res = message.text.split(" ", maxsplit=1)[1]
            await db.set_resolution1(res)
            OUT = f"<blockquote>I will be using : {res} </blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide a resolution value, e.g., /resolution1 640x360</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save resolution value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /resolution1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /resolution1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["preset1", f"preset1@{BOT_USERNAME}"]))
async def changepr(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            preset_val = message.text.split(" ", maxsplit=1)[1]
            await db.set_preset1(preset_val)
            OUT = f"<blockquote>I will be using : {preset_val} preset</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide a preset value, e.g., /preset1 veryfast</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save preset value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /preset1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /preset1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["v_codec1", f"v_codec1@{BOT_USERNAME}"]))
async def changevcodec(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            codec_val = message.text.split(" ", maxsplit=1)[1]
            await db.set_video_codec1(codec_val)
            OUT = f"<blockquote>I will be using : {codec_val} video codec</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide a video codec value, e.g., /v_codec1 libx264</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save video codec value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /v_codec1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /v_codec1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["a_codec1", f"a_codec1@{BOT_USERNAME}"]))
async def changeacodec(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            codec_val = message.text.split(" ", maxsplit=1)[1]
            await db.set_audio_codec1(codec_val)
            OUT = f"<blockquote>I will be using : {codec_val} audio codec</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide an audio codec value, e.g., /a_codec1 aac</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save audio codec value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /a_codec1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /a_codec1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["audio_b1", f"audio_b1@{BOT_USERNAME}"]))
async def changeab(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            aud = message.text.split(" ", maxsplit=1)[1]
            await db.set_audio_b1(aud)
            OUT = f"<blockquote>I will be using : {aud} audio bitrate</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide an audio bitrate value, e.g., /audio_b1 64k</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save audio bitrate value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /audio_b1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /audio_b1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["v_bitrate1", f"v_bitrate1@{BOT_USERNAME}"]))
async def changevbitrate(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            br = message.text.split(" ", maxsplit=1)[1]
            br_int = int(br)  # Validate as integer (0 for None)
            await db.set_video_bitrate1(br_int)
            display = "no video bitrate (auto)" if br_int == 0 else f"{br_int}"
            OUT = f"<blockquote>I will be using : {display} video bitrate</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide a video bitrate value, e.g., /v_bitrate1 1000 (or 0 for none/auto)</blockquote>")
        except ValueError:
            await message.reply_text("<blockquote>Video bitrate must be an integer, e.g., 1000 or 0</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save video bitrate value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /v_bitrate1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /v_bitrate1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")

@app.on_message(filters.incoming & filters.command(["bits1", f"bits1@{BOT_USERNAME}"]))
async def changebits(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            bits_val = message.text.split(" ", maxsplit=1)[1]
            if bits_val not in ["8", "10"]:
                await message.reply_text("<blockquote>Bits must be either 8 or 10, e.g., /bits1 10</blockquote>")
                return
            await db.set_bits1(bits_val)
            OUT = f"<blockquote>I will be using : {bits_val}-bit video encoding</blockquote>"
            await message.reply_text(OUT)
        except IndexError:
            await message.reply_text("<blockquote>Please provide a bits value, e.g., /bits1 10</blockquote>")
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not save bits value. Please try again later.</blockquote>")
            logger.error(f"DB Error in /bits1: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /bits1: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>") 

@app.on_message(filters.incoming & filters.command(["settings1", f"settings1@{BOT_USERNAME}"]))
async def settings(app, message):
    if message.from_user.id in AUTH_USERS:
        try:
            crf_val1 = await db.get_crf1()
            preset_val1 = await db.get_preset1()
            resolution_val1 = await db.get_resolution1()
            audio_b_val1 = await db.get_audio_b1()
            audio_codec_val1 = await db.get_audio_codec1()
            video_codec_val1 = await db.get_video_codec1()
            video_bitrate_val1 = await db.get_video_bitrate1()
            bits_val1 = await db.get_bits1()

            video_bitrate_display1 = "Auto" if video_bitrate_val1 is None else f"{video_bitrate_val}"

            reply_text = (
                f"<b>Tʜᴇ Cᴜʀʀᴇɴᴛ Sᴇᴛᴛɪɴɢꜱ ᴡɪʟʟ ʙᴇ Aᴅᴅᴇᴅ Yᴏᴜʀ Vɪᴅᴇᴏ Fɪʟᴇ ⚙️:</b>\n"
                f"<blockquote>"
                f"<b>➥ Video Codec</b> : {video_codec_val1} \n"
                f"<b>➥ Audio Codec</b> : {audio_codec_val1} \n"
                f"<b>➥ Crf</b> : {crf_val1} \n"
                f"<b>➥ Resolution</b> : {resolution_val1} \n"
                f"<b>➥ Preset</b> : {preset_val1} \n"
                f"<b>➥ Audio Bitrate</b> : {audio_b_val1} \n"
                f"<b>➥ Video Bitrate</b> : {video_bitrate_display1} \n"
                f"<b>➥ Bits</b> : {bits_val1} bits \n"
                f"</blockquote>\n"
                f"<b>🥇 Tʜᴇ Aʙɪʟɪᴛʏ ᴛᴏ Cʜᴀɴɢᴇ Sᴇᴛᴛɪɴɢꜱ ɪꜱ Oɴʟʏ ꜰᴏʀ Aᴅᴍɪɴ</b>"
            )
            await message.reply_text(reply_text)
        except PyMongoError as e:
            await message.reply_text("<blockquote>Database error: Could not retrieve settings. Please try again later.</blockquote>")
            logger.error(f"DB Error in /settings: {e}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text("<blockquote>Rate limit hit, please try again shortly.</blockquote>")
        except Exception as e:
            await message.reply_text("<blockquote>An unexpected error occurred. Please try again.</blockquote>")
            logger.error(f"Unexpected error in /settings: {e}")
    else:
        await message.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")
    
        
@app.on_message(filters.incoming & filters.command(["144p", f"144p@{BOT_USERNAME}"]))
async def help_message(app, message):
    query = await message.reply_text("Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ ⏰...\nPʟᴇᴀꜱᴇ ʙᴇ Pᴀᴛɪᴇɴᴛ, Cᴏᴍᴘʀᴇꜱꜱ ᴡɪʟʟ Sᴛᴀʀᴛ Sᴏᴏɴ", quote=True)
    data1.append(message.reply_to_message)
    if len(data) == 1:
        await query.delete()   
        await add_144(message.reply_to_message)     
            
@app.on_message(filters.incoming & filters.command(["clear", f"clear@{BOT_USERNAME}"]))
async def clr144(app, message):
    data1.clear()
    if message.chat.id not in AUTH_USERS:
        return await message.reply_text("<blockquote>Yᴏᴜ Aʀᴇ Nᴏᴛ Aᴜᴛʜᴏʀɪꜱᴇᴅ Tᴏ Uꜱᴇ Tʜɪꜱ Bᴏᴛ Cᴏɴᴛᴀᴄᴛ @Lord_Vasudev_Krishna</blockquote>")
    query = await message.reply_text("<blockquote>Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ Cʟᴇᴀʀᴇᴅ Qᴜᴇᴜᴇ...📚</blockquote>")
      
        
@app.on_message(filters.incoming & (filters.video | filters.document))
async def incom_message144(app, message):
    if message.chat.id not in AUTH_USERS:
        pass
    query = await message.reply_text("Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ ⏰...\nPʟᴇᴀꜱᴇ ʙᴇ Pᴀᴛɪᴇɴᴛ, Cᴏᴍᴘʀᴇꜱꜱ ᴡɪʟʟ Sᴛᴀʀᴛ Sᴏᴏɴ", quote=True)
    data.append(message)
    if len(data) == 1:
        await query.delete()   
        await add_144(message)
            
        
@app.on_message(filters.incoming & filters.command(["cancel", f"cancel@{BOT_USERNAME}"]))
async def canel_message144(app, message):
    await cancel_144(app, message)
        
@app.on_message(filters.incoming & filters.command(["stop", f"stop@{BOT_USERNAME}"]))
async def stop_message144(app, message):
    await stop_144p()    
