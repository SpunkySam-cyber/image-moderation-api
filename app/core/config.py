import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "image_moderation")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")

settings = Settings()
