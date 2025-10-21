import datetime
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
import os, time, asyncio, json
from bot.localisation import Localisation
from bot import (
  DOWNLOAD_LOCATION, 
  AUTH_USERS,
  LOG_CHANNEL,
  UPDATES_CHANNEL,
  SESSION_NAME,
  data,
  app  
)
from bot.helper_funcs.ffmpeg import (
  convert_video,
  media_info,
  take_screen_shot
)
from bot.helper_funcs.display_progress import (
  progress_for_pyrogram,
  TimeFormatter,
  humanbytes
)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid


os.system("wget https://telegra.ph/file/0e369e097843b0dc4b771.jpg -O thumb.jpg")

CURRENT_PROCESSES = {}
CHAT_FLOOD = {}
broadcast_ids = {}
bot = app

async def incoming_start_message_f(bot, update):
    """/start command"""
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('👨‍💻 Oᴡɴᴇʀ 👨‍💻', url='https://t.me/itsme123c')
                ]
            ]
        ),
        reply_to_message_id=update.id,
    )

async def incoming_compress_message_f(update):
    """/compress command"""
    if update.from_user.id not in AUTH_USERS:
        await update.reply_text("<blockquote>Aᴅᴍɪɴ Oɴʟʏ 🔒</blockquote>")
        return

    d_start = time.time()
    status = os.path.join(DOWNLOAD_LOCATION, "status.json")

    # Send initial status messages
    sent_message = await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.DOWNLOAD_START,
        reply_to_message_id=update.id
    )
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
    ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
    bst_now = utc_now + datetime.timedelta(minutes=0, hours=6)
    bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
    now = f"\n{ist} (GMT+05:30)\n{bst} (GMT+06:00)"
    download_start = await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<blockquote>**𝙱𝚘𝚝 𝙱𝚎𝚌𝚘𝚖𝚎 𝙱𝚞𝚜𝚢 𝙽𝚘𝚠...⛈**{now}</blockquote>"
    )

    # Download video
    try:
        video = await bot.download_media(
            message=update,
            file_name=os.path.join(DOWNLOAD_LOCATION, f"{update.id}.{update.video.file_name.split('.')[-1]}"),
            progress=progress_for_pyrogram,
            progress_args=(bot, Localisation.DOWNLOAD_START, sent_message, d_start)
        )
        if not video or not os.path.exists(video):
            await sent_message.edit_text("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴏᴘᴘᴇᴅ 🛑")
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"<blockquote>**𝙵𝚒𝚕𝚎 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚂𝚝𝚘𝚙𝚙𝚎ᴅ{now}</blockquote>"
            )
            await download_start.delete()
            return
    except Exception as e:
        LOGGER.error(f"Download failed: {e}")
        await sent_message.edit_text(f"<blockquote>Error: {str(e)}</blockquote>")
        await bot.send_message(
            chat_id=LOG_CHANNEL,
            text=f"<blockquote>**𝙵𝚒𝚕𝚎 𝙳𝚊𝚠𝚗𝚕𝚘𝚊𝚍 𝙴𝚛𝚛𝚘𝚛!{now}</blockquote>"
        )
        await download_start.delete()
        return

    await sent_message.edit_text(Localisation.SAVED_RECVD_DOC_FILE)

    # Get video metadata
    duration, bitrate = await media_info(video)
    if duration is None or bitrate is None:
        LOGGER.error("Failed to get video metadata")
        await sent_message.edit_text("⚠️ Gᴇᴛᴛɪɴɢ Vɪᴅᴇᴏ Mᴇᴛᴀ Dᴀᴛᴀ Fᴀɪʟᴇᴅ ⚠️")
        await bot.send_message(
            chat_id=LOG_CHANNEL,
            text=f"<blockquote>**𝙵𝚒𝚕𝚎 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚊𝚒𝚕𝚎𝚍{now}</blockquote>"
        )
        await download_start.delete()
        if os.path.exists(video):
            os.remove(video)
        return

    # Take screenshot for thumbnail
    thumb_image_path = await take_screen_shot(
        video,
        os.path.dirname(os.path.abspath(video)),
        duration / 2
    )

    # Update status for compression
    await download_start.delete()
    compress_start = await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<blockquote>**𝙴𝚗𝚌𝚘𝚍𝚒𝚗𝚐 𝚅𝚒𝚍𝚎𝚘...⚙**{now}</blockquote>"
    )
    await sent_message.edit_text(Localisation.COMPRESS_START)

    # Write status file
    with open(status, 'w') as f:
        json.dump({"running": True, "message": sent_message.id}, f, indent=2)

    # Call convert_video
    c_start = time.time()
    encoded_file = await convert_video(
        video_file=video,
        output_directory=DOWNLOAD_LOCATION,
        total_time=duration,
        bot=bot,
        message=sent_message,
        chan_msg=compress_start
    )

    compressed_time = TimeFormatter((time.time() - c_start) * 1000)
    if not encoded_file or not os.path.exists(encoded_file):
        LOGGER.error("Compression failed, no output file")
        await sent_message.edit_text("⚠️ Cᴏᴍᴘʀᴇꜱꜱɪᴏɴ Fᴀɪʟᴇᴅ ⚠️")
        await bot.send_message(
            chat_id=LOG_CHANNEL,
            text=f"<blockquote>**𝚅𝚒𝚍𝚎𝚘 𝙲𝚘𝚖𝚙𝚛𝚎𝚜𝚜𝚒𝚘𝚗 𝚏𝚊𝚒𝚕𝚎𝚍{now}</blockquote>"
        )
        await compress_start.delete()
        if os.path.exists(video):
            os.remove(video)
        return

    # Upload encoded video
    u_start = time.time()
    await compress_start.delete()
    upload_start = await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<blockquote>**𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 𝚅𝚒𝚍𝚎𝚘 𝚘𝚗 𝚃𝙶...📥**{now}</blockquote>"
    )
    await sent_message.edit_text(Localisation.UPLOAD_START)

    # Use input video's caption or default
    caption = update.caption if update.caption else "Encoded by @Itsme123c"
    
    try:
        upload = await bot.send_document(
            chat_id=update.chat.id,
            document=encoded_file,
            caption=caption,
            force_document=True,
            thumb=thumb_image_path if os.path.exists(thumb_image_path) else "thumb.jpg",
            reply_to_message_id=update.id,
            progress=progress_for_pyrogram,
            progress_args=(bot, Localisation.UPLOAD_START, sent_message, u_start)
        )
        if not upload:
            await sent_message.edit_text("Uᴘʟᴏᴀᴅ Sᴛᴏᴘᴘᴇᴅ 🛑")
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"<blockquote>**𝙵𝚒𝚕𝚎 𝚄𝚙𝚕𝚘𝚊𝚍 𝚜𝚝𝚘𝚙𝚙𝚎𝚍{now}</blockquote>"
            )
            await upload_start.delete()
            if os.path.exists(video):
                os.remove(video)
            if os.path.exists(encoded_file):
                os.remove(encoded_file)
            return
    except Exception as e:
        LOGGER.error(f"Upload failed: {e}")
        await sent_message.edit_text(f"<blockquote>Error: Upload failed - {str(e)}</blockquote>")
        await bot.send_message(
            chat_id=LOG_CHANNEL,
            text=f"<blockquote>**𝙵𝚒𝚕𝚎 𝚄𝚙𝚕𝚘𝚊𝚍 𝙴𝚛𝚛𝚘𝚛{now}</blockquote>"
        )
        await upload_start.delete()
        if os.path.exists(video):
            os.remove(video)
        if os.path.exists(encoded_file):
            os.remove(encoded_file)
        return

    # Finalize
    uploaded_time = TimeFormatter((time.time() - u_start) * 1000)
    await sent_message.delete()
    await upload_start.delete()
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<blockquote>**𝙴𝙽𝙲𝙾𝙳𝙴𝙳 𝚄𝚙𝚕𝚘𝚊𝚍 𝙳𝚘𝚗𝚎{now}</blockquote>"
    )
    try:
        await upload.edit_caption(
            caption=caption.replace('{}', uploaded_time)
        )
    except:
        pass

    # Cleanup
    if os.path.exists(video):
        os.remove(video)
    if os.path.exists(encoded_file):
        os.remove(encoded_file)
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)


async def incoming_cancel_message_f(bot, update):
  """/cancel command"""
  #if update.from_user.id != 1391975600 or 888605132 or 1760568371:
  if update.from_user.id not in AUTH_USERS:      
        
    try:
      await update.message.delete()
    except:
      pass
    return

  status = DOWNLOAD_LOCATION + "/status.json"
  if os.path.exists(status):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton("Yᴇꜱ 🚫", callback_data=("fuckingdo").encode("UTF-8")))
    ikeyboard.append(InlineKeyboardButton("Nᴏ 🤗", callback_data=("fuckoff").encode("UTF-8")))
    inline_keyboard.append(ikeyboard)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.reply_text("Aʀᴇ Yᴏᴜ Sᴜʀᴇ? 🚫 Tʜɪꜱ ᴡɪʟʟ Sᴛᴏᴘ ᴛʜᴇ Cᴏᴍᴘʀᴇꜱꜱɪᴏɴ!", reply_markup=reply_markup, quote=True)
  else:
   # delete_downloads()
    await bot.send_message(
      chat_id=update.chat.id,
      text="<blockquote>No active compression exists</blockquote>",
      reply_to_message_id=update.id
    )
