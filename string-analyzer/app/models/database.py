from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, JSON, and_, or_
from sqlalchemy.sql import func
from typing import Dict, Any, Optional, List
from app.db import Base, SessionLocal, engine
from fastapi import HTTPException, status
import uuid

class StringRecord(Base):
    """SQLAlchemy model for string records"""
    __tablename__ = "string_records"

    id = Column(String(36), primary_key=True, index=True)
    value = Column(Text, nullable=False)
    length = Column(Integer, nullable=False)
    is_palindrome = Column(Boolean, nullable=False)
    unique_characters = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    character_frequency_map = Column(JSON, nullable=False)
    sha256_hash = Column(String(64), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

def add_string(analysis: Dict[str, Any]) -> StringRecord:
    """
    Add a new string record to the database
    
    Args:
        analysis: Dictionary containing string analysis results
        
    Returns:
        StringRecord: Created database record
        
    Raises:
        HTTPException: If database operation fails
    """
    try:
        db = SessionLocal()
        
        # Create new record
        new_record = StringRecord(
            id=str(uuid.uuid4()),
            value=analysis["text"],
            length=analysis["length"],
            is_palindrome=analysis["is_palindrome"],
            unique_characters=analysis["unique_characters"],
            word_count=analysis["word_count"],
            character_frequency_map=analysis["character_frequency_map"],
            sha256_hash=analysis["sha256_hash"]
        )
        
        # Add and commit
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return new_record
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add string record: {str(e)}"
        )
    finally:
        db.close()

def get_string_by_hash(hash_value: str) -> Optional[StringRecord]:
    """
    Retrieve a string record by its SHA-256 hash
    
    Args:
        hash_value: SHA-256 hash of the string
        
    Returns:
        Optional[StringRecord]: Found record or None
    """
    try:
        db = SessionLocal()
        return db.query(StringRecord).filter(StringRecord.sha256_hash == hash_value).first()
    finally:
        db.close()

def get_all_strings(filters: Dict[str, Any] = None) -> List[StringRecord]:
    """
    Retrieve all string records with optional filters
    
    Args:
        filters: Dictionary of filter parameters
            - is_palindrome: bool
            - min_length: int
            - max_length: int
            - word_count: int
            - contains_character: str
            
    Returns:
        List[StringRecord]: List of matching records
        
    Raises:
        HTTPException: If database operation fails
    """
    if filters is None:
        filters = {}
        
    try:
        db = SessionLocal()
        query = db.query(StringRecord)
        
        # Apply filters
        if filters.get("is_palindrome") is not None:
            query = query.filter(StringRecord.is_palindrome == filters["is_palindrome"])
            
        if filters.get("min_length") is not None:
            query = query.filter(StringRecord.length >= filters["min_length"])
            
        if filters.get("max_length") is not None:
            query = query.filter(StringRecord.length <= filters["max_length"])
            
        if filters.get("word_count") is not None:
            query = query.filter(StringRecord.word_count == filters["word_count"])
            
        if filters.get("contains_character") is not None:
            query = query.filter(StringRecord.value.contains(filters["contains_character"]))
        
        return query.all()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve string records: {str(e)}"
        )
    finally:
        db.close()

def delete_string(hash_value: str) -> bool:
    """
    Delete a string record by its SHA-256 hash
    
    Args:
        hash_value: SHA-256 hash of the string to delete
        
    Returns:
        bool: True if deleted, False if not found
        
    Raises:
        HTTPException: If database operation fails
    """
    try:
        db = SessionLocal()
        
        # Find the record
        record = db.query(StringRecord).filter(StringRecord.sha256_hash == hash_value).first()
        
        if not record:
            return False
        
        # Delete the record
        db.delete(record)
        db.commit()
        
        return True
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete string record: {str(e)}"
        )
    finally:
        db.close()

# Create all tables
def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()