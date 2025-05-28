from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, moderation
from app.routes import admin
import os

app = FastAPI(
    title="Image Moderation API",
    version="1.0.0",
    description="Detects and blocks unwanted images via token-protected API.",
)

# Serve your frontend static files
# Serve frontend only at /frontend (e.g., http://127.0.0.1:8000/frontend/index.html)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Add CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware to track all incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"{request.method} {request.url.path} called.")
    response = await call_next(request)
    print(f"{request.method} {request.url.path} responded with {response.status_code}")
    return response

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(moderation.router, prefix="/moderate", tags=["Moderation"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


# app.router.redirect_slashes = True


# Health check route
@app.get("/")
def root():
    return {"message": "Image Moderation API is up and running"}

