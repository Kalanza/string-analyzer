from fastapi import HTTPException, status

def parse_nlp_filter(query: str) -> dict:
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty query")

    query = query.lower()
    filters = {}

    # Detect palindromes
    if "palindromic" in query:
        filters["is_palindrome"] = True

    # Detect word count
    if "single word" in query or "one word" in query:
        filters["word_count"] = 1

    # Detect length
    if "longer than" in query:
        try:
            num = int(query.split("longer than")[1].split()[0])
            filters["min_length"] = num + 1
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid length format")

    # Detect 'containing the letter'
    if "containing the letter" in query:
        letter = query.split("containing the letter")[-1].strip().split()[0]
        filters["contains_character"] = letter

    # Basic validation
    if not filters:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not interpret query")

    # Example of conflicting filters (if any)
    if "min_length" in filters and filters.get("word_count") == 1 and filters["min_length"] > 20:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Conflicting filters")

    return filters
