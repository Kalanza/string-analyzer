# String Analyzer API

A FastAPI-based service that provides comprehensive string analysis and filtering capabilities with persistent storage.

## 🌐 Live Demo

**Base URL**: *(will be updated after deployment)*
- Railway: `https://your-app-name.up.railway.app`
- DigitalOcean: `https://your-app-name.ondigitalocean.app`

## ✨ Features

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

## 📚 API Endpoints

All endpoints are prefixed with `/api/v1`

### Create String Analysis
```http
POST /api/v1/strings/
Content-Type: application/json

{
  "value": "Hello, World!"
}
```
**Response**: 201 Created with full analysis

### Get String Analysis
```http
GET /api/v1/strings/{string_value}
```
Retrieves analysis for a previously stored string.

**Response**: 200 OK or 404 Not Found

### List Strings with Filters
```http
GET /api/v1/strings/?is_palindrome=true&min_length=5
```
Query parameters:
- `is_palindrome`: Filter by palindrome status (boolean)
- `min_length`: Minimum string length (integer)
- `max_length`: Maximum string length (integer)
- `word_count`: Filter by exact word count (integer)
- `contains_character`: Filter by character presence (single char)

**Response**: 200 OK with filtered results

### Natural Language Filtering
```http
GET /api/v1/strings/filter-by-natural-language?query=single word palindromic strings
```
Filter strings using natural language queries.

**Examples**:
- `single word palindromic strings`
- `strings longer than 10 characters`
- `strings containing the letter z`

**Response**: 200 OK with interpreted filters and results

### Delete String
```http
DELETE /api/v1/strings/{string_value}
```
Delete a previously stored string analysis.

**Response**: 204 No Content or 404 Not Found

## 🏗️ Project Structure

```
string-analyzer/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── models/
│   │   └── database.py      # Database models and operations
│   ├── routes/
│   │   └── string_routes.py # API endpoints
│   ├── services/
│   ├── utils/
│   │   ├── analyzer.py      # String analysis logic
│   │   └── filters.py       # NLP filter parser
│   ├── db.py                # Database configuration
│   └── main.py              # FastAPI application
├── tests/
│   └── test_endpoints.http  # HTTP test file
├── .env.example             # Environment variables template
├── .gitignore
├── Procfile                 # Railway deployment config
├── railway.json             # Railway configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kalanza/string-analyzer.git
   cd string-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your settings (SQLite is default for local)
   ```

5. **Initialize the database**
   ```bash
   cd string-analyzer
   python init_db.py
   ```

6. **Run the application**
   ```bash
   cd ..
   uvicorn string-analyzer.app.main:app --reload
   ```

7. **Access the API**
   - API: `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## ☁️ Deployment Options

Choose your preferred deployment platform:

### 🚂 Railway (Recommended for Beginners)
**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide**

- ✅ $5 free credit per month
- ✅ Auto-deploy from GitHub
- ✅ Built-in PostgreSQL
- ✅ Easiest setup

**Quick Start:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Add PostgreSQL database
4. Deploy!

---

### 🌊 DigitalOcean App Platform
**See [DIGITALOCEAN.md](DIGITALOCEAN.md) for detailed guide**

- ✅ $200 free credit (60 days)
- ✅ Professional infrastructure
- ✅ Managed PostgreSQL
- ✅ Great for production

**Quick Start:**
1. Go to [digitalocean.com](https://www.digitalocean.com/products/app-platform)
2. Connect GitHub repo
3. Add PostgreSQL database
4. Deploy!

---

### Comparison

| Feature | Railway | DigitalOcean |
|---------|---------|--------------|
| Free Tier | $5/month credit | $200/60 days |
| Monthly Cost | ~$5-10 | ~$12 |
| Setup Difficulty | Easiest | Easy |
| Best For | MVPs, Hobby | Production |

---

## ☁️ Deployment on Railway (Quick Guide)

### Prerequisites
- GitHub account
- Railway account ([railway.app](https://railway.app))

### Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin master
   ```

2. **Create Railway Project**
   - Go to [Railway](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `string-analyzer` repository

3. **Add PostgreSQL Database**
   - In your Railway project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically create a `DATABASE_URL` variable

4. **Configure Environment Variables**
   - The `DATABASE_URL` is automatically set by Railway
   - Optionally add:
     ```
     ENVIRONMENT=production
     ```

5. **Deploy**
   - Railway will automatically detect your `Procfile` or `railway.json`
   - The app will build and deploy automatically
   - You'll receive a public URL (e.g., `https://string-analyzer-production.up.railway.app`)

6. **Initialize Production Database**
   - After first deployment, run migrations if needed
   - The app will automatically create tables on first run

### Verification

Test your deployed endpoints:
```bash
# Health check
curl https://your-app-name.up.railway.app/docs

# Create a string
curl -X POST https://your-app-name.up.railway.app/api/v1/strings/ \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

## 🔧 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./string_analyzer.db` | No |
| `ENVIRONMENT` | Environment mode | `development` | No |

### Local (.env)
```env
DATABASE_URL=sqlite:///./string_analyzer.db
ENVIRONMENT=development
```

### Production (Railway)
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
ENVIRONMENT=production
```

## 📦 Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **python-dotenv** - Environment variable management
- **psycopg2-binary** - PostgreSQL adapter (for production)

## 🧪 Testing

### Using HTTP Client
See `tests/test_endpoints.http` for example requests.

### Using cURL
```bash
# Create string
curl -X POST http://localhost:8000/api/v1/strings/ \
  -H "Content-Type: application/json" \
  -d '{"value": "Hello World"}'

# Get string
curl http://localhost:8000/api/v1/strings/Hello%20World

# List all strings
curl http://localhost:8000/api/v1/strings/

# Filter palindromes
curl "http://localhost:8000/api/v1/strings/?is_palindrome=true"

# NLP filter
curl "http://localhost:8000/api/v1/strings/filter-by-natural-language?query=palindromic%20strings"

# Delete string
curl -X DELETE http://localhost:8000/api/v1/strings/Hello%20World
```

## 👨‍💻 Author

**Kalanza**
- GitHub: [@Kalanza](https://github.com/Kalanza)
- Repository: [string-analyzer](https://github.com/Kalanza/string-analyzer)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 Notes

- All timestamps are in UTC ISO format
- SHA-256 hashing is used for duplicate detection
- Strings are case-sensitive for storage but palindrome checks are case-insensitive
- The API uses JSON for all request/response bodies
