from fastapi import FastAPI
from app.routes.string_routes import router

# Initialize FastAPI application
app = FastAPI(
    title="String Analyzer API",
    description="An API for analyzing strings and performing various string operations",
    version="1.0.0"
)

# Include the string routes
app.include_router(router, prefix="/api/v1")
