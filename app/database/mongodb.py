import motor.motor_asyncio
import os

# Only load .env locally — Railway sets env vars via dashboard
if os.getenv("RAILWAY_ENVIRONMENT") is None:
    from dotenv import load_dotenv
    load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "image_moderation")

# Debug: check if env vars are actually loaded (remove in prod)
print("MONGO_URI:", repr(MONGO_URI))
print("DATABASE_NAME:", repr(DATABASE_NAME))

# Connect to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_token_collection():
    return db["tokens"]

def get_usage_collection():
    return db["usages"]

def get_user_collection():
    return db["users"]
