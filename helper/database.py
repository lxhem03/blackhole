from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            Config.MONGO_URI,
            maxPoolSize=50,
            minPoolSize=5,
            serverSelectionTimeoutMS=5000
        )
        self.db = self.client[Config.DB_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]
        try:
            self.client.admin.command('ping')
            print("MongoDB connection successful")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
    
    defaults = {
        "crf": 24,
        "preset": "veryfast",
        "resolution": "640x360",
        "audio_b": "64k",
        "audio_codec": "aac",
        "video_codec": "libx264",
        "video_bitrate": 0,
        "bits": "8",
        "watermark": 0
    }
    
    async def get_crf(self):
        doc = await self.collection.find_one({"_id": "crf"})
        return doc["value"] if doc else self.defaults["crf"]
    
    async def set_crf(self, value):
        await self.collection.replace_one({"_id": "crf"}, {"_id": "crf", "value": value}, upsert=True)
    
    async def get_watermark(self):
        doc = await self.collection.find_one({"_id": "watermark"})
        value = doc["value"] if doc else self.defaults["watermark"]
        return None if value == 0 else value
    
    async def set_watermark(self, value):
        await self.collection.replace_one({"_id": "watermark"}, {"_id": "watermark", "value": value}, upsert=True)

    # Save chat
    async def save_chat(self, chat_id: int):
        await self.collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"chat_id": chat_id}},
            upsert=True
        )

    # Remove chat
    async def remove_chat(self, chat_id: int):
        await self.collection.delete_one({"chat_id": chat_id})

    # Modify chat ID
    async def modify_chat(self, old_id: int, new_id: int):
        await self.collection.update_one(
            {"chat_id": old_id},
            {"$set": {"chat_id": new_id}}
        )

    # Check if authorized
    async def is_authorized(self, chat_id: int) -> bool:
        doc = await self.collection.find_one({"chat_id": chat_id})
        return doc is not None

    # List all authorized chats
    async def all_chats(self) -> list:
        cursor = self.collection.find({"chat_id": {"$exists": True}})
        return [doc["chat_id"] async for doc in cursor]  # Only return the ID, not full doc

    
    async def get_resolution(self):
        doc = await self.collection.find_one({"_id": "resolution"})
        return doc["value"] if doc else self.defaults["resolution"]
    
    async def set_resolution(self, value):
        await self.collection.replace_one({"_id": "resolution"}, {"_id": "resolution", "value": value}, upsert=True)
    
    async def get_audio_b(self):
        doc = await self.collection.find_one({"_id": "audio_b"})
        return doc["value"] if doc else self.defaults["audio_b"]
    
    async def set_audio_b(self, value):
        await self.collection.replace_one({"_id": "audio_b"}, {"_id": "audio_b", "value": value}, upsert=True)
    
    async def get_preset(self):
        doc = await self.collection.find_one({"_id": "preset"})
        return doc["value"] if doc else self.defaults["preset"]
    
    async def set_preset(self, value):
        await self.collection.replace_one({"_id": "preset"}, {"_id": "preset", "value": value}, upsert=True)
    
    async def get_audio_codec(self):
        doc = await self.collection.find_one({"_id": "audio_codec"})
        return doc["value"] if doc else self.defaults["audio_codec"]
    
    async def set_audio_codec(self, value):
        await self.collection.replace_one({"_id": "audio_codec"}, {"_id": "audio_codec", "value": value}, upsert=True)
    
    async def get_video_codec(self):
        doc = await self.collection.find_one({"_id": "video_codec"})
        return doc["value"] if doc else self.defaults["video_codec"]
    
    async def set_video_codec(self, value):
        await self.collection.replace_one({"_id": "video_codec"}, {"_id": "video_codec", "value": value}, upsert=True)
    
    async def get_video_bitrate(self):
        doc = await self.collection.find_one({"_id": "video_bitrate"})
        value = doc["value"] if doc else self.defaults["video_bitrate"]
        return None if value == 0 else value
    
    async def set_video_bitrate(self, value):
        await self.collection.replace_one({"_id": "video_bitrate"}, {"_id": "video_bitrate", "value": value}, upsert=True)

    async def get_bits(self):
        doc = await self.collection.find_one({"_id": "bits"})
        return doc["value"] if doc else self.defaults["bits"]
    
    async def set_bits(self, value):
        await self.collection.replace_one({"_id": "bits"}, {"_id": "bits", "value": value}, upsert=True)
            

db = Database()
