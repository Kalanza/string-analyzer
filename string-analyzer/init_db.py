from app.models.database import init_db
from app.db import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init():
    logger.info("Creating database tables...")
    init_db()
    logger.info("Database tables created successfully!")

if __name__ == "__main__":
    init()