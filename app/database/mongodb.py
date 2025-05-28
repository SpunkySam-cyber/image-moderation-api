import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "image_moderation")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_token_collection():
    return db["tokens"]

def get_usage_collection():
    return db["usages"]

def get_user_collection():
    return db["users"]
