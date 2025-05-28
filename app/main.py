from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.routes import auth, moderation, admin

app = FastAPI(
    title="Image Moderation API",
    version="1.0.0",
    description="Detects and blocks unwanted images via token-protected API.",
)

# Serve static frontend at root
frontend_dir = "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# ✅ Renamed to avoid conflict with /admin router
@app.get("/admin-page")
async def serve_admin():
    return FileResponse(os.path.join(frontend_dir, "admin.html"))

# ✅ Renamed to avoid conflict with /moderate router
@app.get("/moderation-page")
async def serve_moderation():
    return FileResponse(os.path.join(frontend_dir, "moderation.html"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"{request.method} {request.url.path} called.")
    response = await call_next(request)
    print(f"{request.method} {request.url.path} responded with {response.status_code}")
    return response

# API Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(moderation.router, prefix="/moderate", tags=["Moderation"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
