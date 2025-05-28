from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import secrets
from passlib.context import CryptContext
from app.database.mongodb import get_token_collection, get_user_collection
from app.services.auth_service import verify_admin_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Registration model
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

# Register route
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister, user_collection=Depends(get_user_collection)):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = pwd_context.hash(user.password)
    await user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_pw
    })
    return {"message": f"User {user.username} registered successfully."}

# Login route
@router.post("/login", response_model=TokenResponse)
async def login(login_req: LoginRequest, user_collection=Depends(get_user_collection), token_collection=Depends(get_token_collection)):
    user = await user_collection.find_one({"username": login_req.username})
    if not user or not pwd_context.verify(login_req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_hex(16)
    await token_collection.insert_one({
        "token": token,
        "username": user["username"],
        "isAdmin": False,
        "createdAt": datetime.utcnow()
    })

    return TokenResponse(access_token=token)

# Admin-only: Create token
class TokenCreateRequest(BaseModel):
    is_admin: bool = False

@router.post("/tokens")
async def create_token(request: TokenCreateRequest, token_collection=Depends(get_token_collection), current_user=Depends(verify_admin_token)):
    token = secrets.token_hex(16)
    await token_collection.insert_one({
        "token": token,
        "isAdmin": request.is_admin,
        "createdAt": datetime.utcnow()
    })
    return {"token": token, "isAdmin": request.is_admin}

# Admin-only: List tokens
@router.get("/tokens")
async def get_tokens(token_collection=Depends(get_token_collection), current_user=Depends(verify_admin_token)):
    tokens = await token_collection.find().to_list(length=None)
    return tokens

# Admin-only: Delete token
@router.delete("/tokens/{token}")
async def delete_token(token: str, token_collection=Depends(get_token_collection), current_user=Depends(verify_admin_token)):
    result = await token_collection.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"message": "Token deleted"}
