# String Analyzer API

A FastAPI-based service that provides comprehensive string analysis and filtering capabilities.

## Features

- **String Analysis**: Analyze strings for various properties including:
  - Length
  - Palindrome check
  - Unique character count
  - Word count
  - Character frequency map
  - SHA256 hash

- **Storage**: Persistent storage of analyzed strings with duplicate detection
- **Filtering**: Multiple filtering options including:
  - Palindrome status
  - String length (min/max)
  - Word count
  - Character presence
  - Natural language queries

## API Endpoints

### Create String Analysis
```http
POST /strings/
```
Creates a new string analysis record.

### Get String Analysis
```http
GET /strings/{string_value}
```
Retrieves analysis for a previously stored string.

### List Strings with Filters
```http
GET /strings/
```
Retrieve all string records with optional filters:
- `is_palindrome`: Filter by palindrome status
- `min_length`: Minimum string length
- `max_length`: Maximum string length
- `word_count`: Filter by exact word count
- `contains_character`: Filter by character presence

### Natural Language Filtering
```http
GET /strings/filter-by-natural-language
```
Filter strings using natural language queries.
Example: `?query=single word palindromic strings`

### Delete String
```http
DELETE /strings/{string_value}
```
Delete a previously stored string analysis.

## Project Structure

```
string-analyzer/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── models/
│   │   └── database.py
│   ├── routes/
│   │   └── string_routes.py
│   ├── services/
│   ├── utils/
│   │   ├── analyzer.py
│   │   └── filters.py
│   ├── db.py
│   └── main.py
├── tests/
└── requirements.txt
```

## Dependencies

See `requirements.txt` for a full list of dependencies.

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python init_db.py
   ```
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
