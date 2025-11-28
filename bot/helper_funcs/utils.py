import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os, asyncio, pyrogram, psutil, platform, time
from bot import data
from bot.plugins.incoming_message_fn import incoming_compress_message_f
from pyrogram.types import Message
import psutil
import subprocess
from urllib.request import urlopen

def checkKey(dict, key):
  if key in dict.keys():
    return True
  else:
    return False

def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

async def on_task_complete():
    del data[0]
    if len(data) > 0:
      await add_task(data[0])

async def add_task(message: Message):
    try:
        os.system('rm -rf /app/downloads/*')
        await incoming_compress_message_f(message)
    except Exception as e:
        LOGGER.info(e)  
    await on_task_complete()

def human(n: int) -> str:
    return psutil._common.bytes2human(n)


async def sysinfo(e):
    # 1. CPU – first call returns 0.0, so we call it once and discard
    psutil.cpu_percent(interval=None)         
    cpu_usage = psutil.cpu_percent(interval=1) 

    # 2. CPU frequency
    freq = psutil.cpu_freq()
    freq_current = (
        f"{round(freq.current / 1000, 2)} GHz"
        if freq else "N/A"
    )

    # 3. Core counts
    cpu_physical = psutil.cpu_count(logical=False) or "E"
    cpu_logical  = psutil.cpu_count(logical=True)  or "E"

    # 4. RAM
    ram = psutil.virtual_memory()

    # 5. Disk – root filesystem
    disk = psutil.disk_usage('/')

    # 6. Network I/O
    net = psutil.net_io_counters()
    ul_size = net.bytes_sent
    dl_size = net.bytes_recv

    # Additional features
    # Python version
    python_version = platform.python_version()

    # FFmpeg version
    try:
        ffmpeg_output = subprocess.check_output(['ffmpeg', '-version']).decode('utf-8')
        ffmpeg_version = ffmpeg_output.split('\n')[0].strip()  # e.g., "ffmpeg version X.Y.Z"
    except Exception:
        ffmpeg_version = "FFmpeg not installed or not found"

    # Additional FFmpeg-related checks
    # Check for key encoders (e.g., libx264 for H.264, libx265 for H.265)
    try:
        encoders_output = subprocess.check_output(['ffmpeg', '-encoders']).decode('utf-8')
        has_libx264 = "libx264" in encoders_output
        has_libx265 = "libx265" in encoders_output
        encoders_info = f"libx264: {'Available' if has_libx264 else 'Missing'}, libx265: {'Available' if has_libx265 else 'Missing'}"
    except Exception:
        encoders_info = "Unable to check encoders"

    # Check for hardware acceleration (e.g., NVENC for NVIDIA)
    try:
        hwaccel_output = subprocess.check_output(['ffmpeg', '-hwaccels']).decode('utf-8')
        has_nvenc = "nvenc" in hwaccel_output.lower()
        has_vaapi = "vaapi" in hwaccel_output.lower()
        has_videotoolbox = "videotoolbox" in hwaccel_output.lower()
        hwaccel_info = f"NVENC: {'Available' if has_nvenc else 'No'}, VAAPI: {'Available' if has_vaapi else 'No'}, VideoToolbox: {'Available' if has_videotoolbox else 'No'}"
    except Exception:
        hwaccel_info = "Unable to check hardware acceleration"

    # Hosting server speed (download speed test using a 10MB file)
    try:
        url = 'http://speedtest.tele2.net/10MB.zip'
        expected_size_mb = 10.0
        start_time = time.perf_counter()
        with urlopen(url) as response:
            data = response.read()
        end_time = time.perf_counter()
        duration = end_time - start_time
        download_speed_mbps = (expected_size_mb * 8) / duration  # Convert MB/s to Mbps (megabits per second)
        download_speed = f"{round(download_speed_mbps, 2)} Mbps"
    except Exception:
        download_speed = "Unable to measure download speed"

    text = (
        "<u><b>Sʏꜱᴛᴇᴍ Sᴛᴀᴛꜱ</b></u>\n"
        "<blockquote>"
        f"<b>CPU Freq:</b> <i>{freq_current}</i>\n"
        f"<b>CPU Cores [ Physical:</b> <i>{cpu_physical}</i> | <b>Total:</b> <i>{cpu_logical}</i> ]\n\n"

        f"<b>Total Disk :</b> <i>{human(disk.total)}B</i>\n"
        f"<b>Used:</b> <i>{human(disk.used)}B</i> | <b>Free:</b> <i>{human(disk.free)}B</i>\n\n"

        f"<b>Total Upload:</b> <i>{human(ul_size)}B</i>\n"
        f"<b>Total Download:</b> <i>{human(dl_size)}B</i>\n\n"

        f"<b>Total Ram :</b> {human(ram.total)}B\n"
        f"<b>Used:</b> <i>{human(ram.used)}B</i> | <b>Free:</b> <i>{human(ram.available)}B</i>\n\n"

        f"<b>CPU:</b> <i>{cpu_usage}%</i>\n"
        f"<b>RAM:</b> <i>{int(ram.percent)}%</i>\n"
        f"<b>DISK:</b> <i>{int(disk.percent)}%</i>\n\n"

        f"<b>Python Version:</b> <i>{python_version}</i>\n"
        f"<b>FFmpeg Version:</b> <i>{ffmpeg_version}</i>\n"
        f"<b>Key Encoders:</b> <i>{encoders_info}</i>\n"
        f"<b>Hardware Acceleration:</b> <i>{hwaccel_info}</i>\n"
        f"<b>Download Speed:</b> <i>{download_speed}</i>"
        "</blockquote>"
    )

    await e.reply_text(text, disable_web_page_preview=True)
