from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, func
from sqlalchemy import JSON as SA_JSON
from sqlalchemy.orm import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Schema(Base):
    __tablename__ = "schema"
    id = Column(String(50), primary_key=True)                 # maps CharField
    value = Column(Text, nullable=False)                      # maps TextField
    length = Column(Integer, nullable=False)                  # maps IntegerField
    is_palindrome = Column(Boolean, nullable=False)           # maps BooleanField
    unique_characters = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    # Use JSONB for Postgres, otherwise sa.JSON for general DBs
    character_frequency_map = Column(sa.JSON, nullable=False)
    sha256_hash = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
