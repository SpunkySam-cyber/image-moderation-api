from fastapi import Depends, Header, HTTPException, status
from app.database.mongodb import get_token_collection

async def verify_admin_token(
    authorization: str = Header(...),
    token_collection=Depends(get_token_collection)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")

    token = authorization.split(" ")[1]
    token_doc = await token_collection.find_one({"token": token})

    if not token_doc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not found")

    if not token_doc.get("isAdmin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return token_doc

from app.database.mongodb import db

async def verify_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    
    token = authorization.split(" ")[1]
    token_doc = await db.tokens.find_one({"token": token})
    
    if not token_doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return token
