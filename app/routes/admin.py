from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import verify_token, verify_admin_token
from app.database.mongodb import db

router = APIRouter()

@router.get("/users", summary="List all users (admin only)")
async def list_users(current_user: str = Depends(verify_admin_token)):
    users = await db.users.find().to_list(100)
    return [
        {
            "user_id": str(u.get("_id")),
            "username": u.get("username"),
            "email": u.get("email"),
            "created_at": u.get("created_at", None),
        }
        for u in users
    ]

@router.get("/tokens", summary="List all tokens (admin only)")
async def list_tokens(current_user: str = Depends(verify_admin_token)):
    tokens = await db.tokens.find().to_list(100)
    return [
        {
            "token": t.get("token", "N/A"),
            "isAdmin": t.get("isAdmin", False),
            "revoked": t.get("revoked", False),
            "user_id": str(t.get("_id")) if t.get("_id") else "N/A",
            "username": t.get("username", "N/A"),
        }
        for t in tokens
    ]

@router.get("/usages", summary="List usage logs (admin only)")

async def list_usages(current_user: str = Depends(verify_admin_token)):
    usages = await db.usages.find().to_list(100)
    formatted_usages = []
    for u in usages:
        u["_id"] = str(u["_id"])  # Convert ObjectId to string
        formatted_usages.append(u)
    return formatted_usages


@router.post("/tokens/revoke", summary="Revoke a token (admin only)")
async def revoke_token(token: str, current_user: str = Depends(verify_admin_token)):
    result = await db.tokens.update_one({"token": token}, {"$set": {"revoked": True}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Token not found or already revoked")
    return {"message": f"Token {token} revoked successfully"}
