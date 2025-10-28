from collections import Counter
import hashlib
import string

def analyze_string(text: str) -> dict:
    """
    Analyze a string and return key metrics:
    - length
    - is_palindrome
    - unique_characters
    - word_count
    - sha256_hash
    - character_frequency_map
    """

    # --- 1️⃣ Basic properties ---

    length = len(text)
    words = text.split()
    word_count = len(words)
    unique_characters = set(text)
    
    # --- 2️⃣ Palindrome check (normalized) ---
    cleaned = ''.join(ch.lower() for ch in text if ch.isalnum())
    is_palindrome = cleaned == cleaned[::-1]

    # --- 3️⃣ SHA256 hash ---
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()

    # --- 4️⃣ Character frequency map ---
    character_frequency_map = dict(Counter(text.lower()))
    
    # --- 5️⃣ Bundle results ---
    result = {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": len(unique_characters),
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": character_frequency_map
    }
    return result

# Test the function with some example text
if __name__ == "__main__":
    test_string = "Hello World!"
    result = analyze_string(test_string)
    print("\nAnalyzing string:", test_string)
    print("\nResults:")
    for key, value in result.items():
        print(f"{key}: {value}")