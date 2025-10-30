from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.string_routes import router
from app.models.database import init_db
import os

# Initialize FastAPI application
app = FastAPI(
    title="String Analyzer API",
    description="An API for analyzing strings and performing various string operations",
    version="1.0.0"
)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables when the application starts"""
    init_db()

# Root route - serve the main HTML page
@app.get("/")
async def read_root():
    """Serve the main web interface"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Include the string routes
app.include_router(router, prefix="/api/v1")
