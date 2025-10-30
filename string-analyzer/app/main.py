from fastapi import FastAPI
from app.routes.string_routes import router
from app.models.database import init_db

# Initialize FastAPI application
app = FastAPI(
    title="String Analyzer API",
    description="An API for analyzing strings and performing various string operations",
    version="1.0.0"
)

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables when the application starts"""
    init_db()

# Include the string routes
app.include_router(router, prefix="/api/v1")
