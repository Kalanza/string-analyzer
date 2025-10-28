from fastapi import APIRouter, HTTPException, status, Body, Path, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from app.utils import analyzer
from app.models.database import add_string, get_string_by_hash, get_all_strings, StringRecord
from app.db import get_db

# Pydantic models for request/response validation
class StringAnalyzeRequest(BaseModel):
    value: str = Field(..., min_length=1, description="The string to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "value": "Hello, World!"
            }
        }

class StringAnalysisResponse(BaseModel):
    id: str
    value: str
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    character_frequency_map: Dict[str, int]
    sha256_hash: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "value": "Racecar",
                "length": 7,
                "is_palindrome": True,
                "unique_characters": 5,
                "word_count": 1,
                "character_frequency_map": {"r": 2, "a": 2, "c": 2, "e": 1},
                "sha256_hash": "hash_value"
            }
        }

# Create router instance
router = APIRouter(prefix="/strings", tags=["Strings"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_string_record(request: StringAnalyzeRequest):
    """
    Create a new string record with analysis
    
    - Validates input string through Pydantic model
    - Analyzes the string using analyzer utility
    - Checks for duplicates using SHA256 hash
    - Stores results in database
    - Returns analyzed data with 201 Created status
    """
    # Analyze the string
    analysis = analyzer.analyze_string(request.value)
    
    # Check for duplicate using hash
    existing_record = get_string_by_hash(analysis["sha256_hash"])
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This string has already been analyzed and stored"
        )
    
    # Add analysis text field
    analysis["text"] = request.value
    
    # Store the analysis in database
    record = add_string(analysis)
    
    # Return success response with analyzed data
    return StringAnalysisResponse(
        id=record.id,
        value=record.value,
        length=record.length,
        is_palindrome=record.is_palindrome,
        unique_characters=record.unique_characters,
        word_count=record.word_count,
        character_frequency_map=record.character_frequency_map,
        sha256_hash=record.sha256_hash
    )


@router.get("/{string_value}", response_model=StringAnalysisResponse)
async def get_string_analysis(
    string_value: str = Path(
        ...,
        min_length=1,
        description="The string to look up",
        example="Racecar"
    )
):
    """
    Retrieve analysis for a previously stored string.
    
    Parameters:
        string_value (str): The string to look up in the database
        
    Returns:
        StringAnalysisResponse: Complete analysis of the stored string
        
    Raises:
        HTTPException: 404 if string not found in database
    """
    # Compute hash for lookup
    analysis = analyzer.analyze_string(string_value)
    hash_value = analysis["sha256_hash"]
    
    # Fetch record by hash
    record = get_string_by_hash(hash_value)
    
    # Check result
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String not found in database"
        )
    
    # Return response
    return StringAnalysisResponse(
        id=record.id,
        value=record.value,
        length=record.length,
        is_palindrome=record.is_palindrome,
        unique_characters=record.unique_characters,
        word_count=record.word_count,
        character_frequency_map=record.character_frequency_map,
        sha256_hash=record.sha256_hash
    )


@router.get("/", response_model=Dict[str, Any])
async def list_strings(
    is_palindrome: Optional[bool] = Query(None, description="Filter by palindrome status"),
    min_length: Optional[int] = Query(None, ge=0, description="Minimum string length"),
    max_length: Optional[int] = Query(None, ge=0, description="Maximum string length"),
    word_count: Optional[int] = Query(None, ge=0, description="Filter by word count"),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1, 
                                           description="Filter by character presence"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all string records with optional filters.
    
    Parameters:
        is_palindrome: Filter by palindrome status
        min_length: Minimum string length
        max_length: Maximum string length
        word_count: Filter by exact word count
        contains_character: Filter by character presence
        db: Database session dependency
        
    Returns:
        Dict containing filtered results and metadata
        
    Raises:
        HTTPException: 500 if database operation fails
    """
    try:
        filters = {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character,
        }

        results = get_all_strings(db, filters)
        
        # Remove None values from filters
        applied_filters = {k: v for k, v in filters.items() if v is not None}

        return {
            "status": "success",
            "filters_applied": applied_filters,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve strings: {str(e)}"
        )



