from app.models.database import add_string
import hashlib

def test_db_connection():
    # Create test data
    test_analysis = {
        "text": "Hello, World!",
        "length": 13,
        "is_palindrome": False,
        "unique_characters": 10,
        "word_count": 2,
        "character_frequency_map": {"H": 1, "e": 1, "l": 3, "o": 2, "W": 1, "r": 1, "d": 1, "!": 1},
        "sha256_hash": hashlib.sha256("Hello, World!".encode()).hexdigest()
    }
    
    # Try to add a record
    try:
        record = add_string(test_analysis)
        print(f"Test successful! Added record with ID: {record.id}")
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_db_connection()