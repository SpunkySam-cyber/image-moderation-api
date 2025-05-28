from fastapi import APIRouter, UploadFile, File, Depends
from app.services.auth_service import verify_token
from app.database.mongodb import db
from datetime import datetime
import random

router = APIRouter()

@router.post("/", summary="Moderate an uploaded image")
async def moderate_image(
    file: UploadFile = File(...),
    current_user: str = Depends(verify_token)
):
    # Fake moderation logic
    categories = {
        "nudity": round(random.uniform(0.0, 1.0), 2),
        "violence": round(random.uniform(0.0, 1.0), 2),
        "hate_symbols": round(random.uniform(0.0, 1.0), 2),
        "self_harm": round(random.uniform(0.0, 1.0), 2),
        "extremist_propaganda": round(random.uniform(0.0, 1.0), 2),
    }

    # Determine if image is safe (all scores < 0.5)
    safe = all(score < 0.5 for score in categories.values())
    approved = safe  # True if safe, False if blocked

    # Add a human-readable status message
    status_msg = "Image approved for upload." if approved else "Image blocked due to inappropriate content."

    # Log usage
    await db.usages.insert_one({
        "token": current_user,
        "endpoint": "/moderate",
        "timestamp": datetime.utcnow()
    })

    return {
        "approved": approved,
        "message": status_msg,
        "safe": safe,
        "categories": categories
    }
