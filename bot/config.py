from bot.get_cfg import get_config

class Config(object):
    #Session
    SESSION_NAME = get_config("SESSION_NAME", "EncoderX") 
    #Telegram Credentials 
    APP_ID = int(get_config("APP_ID", "26387127"))
    API_HASH = get_config("API_HASH", "19718ab7acd97d0f71ada2807ddfe47a")

    # Bot Credentials 
    TG_BOT_TOKEN = get_config("TG_BOT_TOKEN", "7672683596:AAE2pJ95BtP15Mi7xZS7kCYy78y5EoQxK40")
    BOT_USERNAME = get_config("BOT_USERNAME", "Tjggursgjybot")

    # User or group id 
    AUTH_USERS = [7660990923, -1002762108584]

    #Channels
    LOG_CHANNEL = get_config("LOG_CHANNEL", "Lod_krishna")
    UPDATES_CHANNEL = get_config("UPDATES_CHANNEL", None) # Without `@` LOL

    #Mongo DB: (Added by @Telegram_Guyz in github 🌚) 
    MONGO_URI = get_config("MONGO_URI", "") #Required 
    DB_NAME = get_config("DB_NAME", "") #Required
    COLLECTION_NAME = get_config("COLLECTION_NAME", "") #Required

    
    # Download location of your server 
    DOWNLOAD_LOCATION = get_config("DOWNLOAD_LOCATION", "/app/downloads")
    
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 4194304000
    TG_MAX_FILE_SIZE = 4194304000
    FREE_USER_MAX_FILE_SIZE = 4194304000
    
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = get_config("DEF_THUMB_NAIL_VID_S", "https://envs.sh/CQU.jpg")
    
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = get_config("HTTP_PROXY", None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    
    # add config vars for the display progress
    FINISHED_PROGRESS_STR = get_config("FINISHED_PROGRESS_STR", "▣")
    UN_FINISHED_PROGRESS_STR = get_config("UN_FINISHED_PROGRESS_STR", "▢")
    LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC", "Log.txt")
    SHOULD_USE_BUTTONS = get_config("SHOULD_USE_BUTTONS", False)
