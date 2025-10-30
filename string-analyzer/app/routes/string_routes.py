from app.utils.filters import parse_nlp_filter
from fastapi import APIRouter, HTTPException, status, Body, Path, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from app.utils import analyzer
from app.models.database import add_string, get_string_by_hash, get_all_strings, delete_string, StringRecord
from hashlib import sha256

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
                                           description="Filter by character presence")
):
    """
    Retrieve all string records with optional filters.
    
    Parameters:
        is_palindrome: Filter by palindrome status
        min_length: Minimum string length
        max_length: Maximum string length
        word_count: Filter by exact word count
        contains_character: Filter by character presence
        
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

        results = get_all_strings(filters)
        
        # Convert SQLAlchemy objects to dictionaries
        results_dict = [
            {
                "id": r.id,
                "value": r.value,
                "length": r.length,
                "is_palindrome": r.is_palindrome,
                "unique_characters": r.unique_characters,
                "word_count": r.word_count,
                "character_frequency_map": r.character_frequency_map,
                "sha256_hash": r.sha256_hash,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in results
        ]
        
        # Remove None values from filters
        applied_filters = {k: v for k, v in filters.items() if v is not None}

        return {
            "status": "success",
            "filters_applied": applied_filters,
            "count": len(results_dict),
            "results": results_dict
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve strings: {str(e)}"
        )



@router.get("/filter-by-natural-language")
def filter_nlp(query: str):
    """
    Interpret natural language filter queries and return results.
    Example: ?query=single word palindromic strings
    """
    filters = parse_nlp_filter(query)

    # Here you would apply filters to your data source or DB
    # For now, let's mock some filtered results:
    mock_data = ["madam", "racecar", "deed", "hello", "zoom"]

    result = []

    for text in mock_data:
        if filters.get("is_palindrome") and text != text[::-1]:
            continue
        if filters.get("contains_character") and filters["contains_character"] not in text:
            continue
        if filters.get("min_length") and len(text) < filters["min_length"]:
            continue
        if filters.get("word_count") and len(text.split()) != filters["word_count"]:
            continue
        result.append(text)

    return {"filters": filters, "results": result}


@router.delete("/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_string_record(string_value: str = Path(..., min_length=1, description="The string to delete")):
    """
    Delete a string record by its value.
    
    Parameters:
        string_value (str): The string to delete from the database
        
    Returns:
        204 No Content on successful deletion
        
    Raises:
        HTTPException: 404 if string not found in database
        HTTPException: 500 if database operation fails
    """
    # Compute hash for lookup
    analysis = analyzer.analyze_string(string_value)
    hash_value = analysis["sha256_hash"]
    
    # Attempt to delete the record
    deleted = delete_string(hash_value)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String not found in database"
        )
    
    # Return None for 204 No Content (no response body)
    return None
