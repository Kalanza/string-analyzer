# 🚀 Railway Deployment Guide for String Analyzer API

## ✅ Pre-Deployment Checklist

- [x] All code committed to GitHub
- [x] .gitignore created (excludes .env, venv, __pycache__, etc.)
- [x] .env.example created for reference
- [x] requirements.txt updated with all dependencies
- [x] Procfile created for Railway
- [x] railway.json configuration added
- [x] Database configuration updated to support PostgreSQL
- [x] README.md updated with deployment instructions

## 📋 Step-by-Step Deployment Guide

### Step 1: Create Railway Account

1. Go to [https://railway.app](https://railway.app)
2. Click "Login" or "Start a New Project"
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

### Step 2: Create New Project

1. On Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. You may need to authorize Railway to access your GitHub account
4. Select **"Kalanza/string-analyzer"** repository
5. Railway will automatically detect it's a Python project

### Step 3: Add PostgreSQL Database

1. In your project dashboard, click **"New"** button
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will:
   - Provision a PostgreSQL database
   - Automatically create a `DATABASE_URL` environment variable
   - Link it to your application

### Step 4: Configure Environment Variables (Optional)

Railway automatically sets `DATABASE_URL`, but you can add more:

1. Click on your service (the main app, not the database)
2. Go to **"Variables"** tab
3. Add additional variables if needed:
   ```
   ENVIRONMENT=production
   ```

### Step 5: Deploy

Railway will automatically:
1. Detect your `Procfile` or `railway.json`
2. Install dependencies from `requirements.txt`
3. Run the start command: `uvicorn string-analyzer.app.main:app --host 0.0.0.0 --port $PORT`
4. Assign a public URL

**Monitor the deployment:**
- Click on **"Deployments"** tab to see build logs
- Wait for status to show **"Success"** or **"Active"**
- This usually takes 2-5 minutes

### Step 6: Get Your Public URL

1. In your service settings, go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. You'll get a URL like: `https://string-analyzer-production.up.railway.app`
5. Copy this URL for testing

### Step 7: Test Your Deployment

#### Test the API Documentation
Open in browser:
```
https://your-app-name.up.railway.app/docs
```

#### Test with cURL

**Create a string:**
```bash
curl -X POST https://your-app-name.up.railway.app/api/v1/strings/ \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

**Get a string:**
```bash
curl https://your-app-name.up.railway.app/api/v1/strings/racecar
```

**List all strings:**
```bash
curl https://your-app-name.up.railway.app/api/v1/strings/
```

**Filter palindromes:**
```bash
curl "https://your-app-name.up.railway.app/api/v1/strings/?is_palindrome=true"
```

**NLP filter:**
```bash
curl "https://your-app-name.up.railway.app/api/v1/strings/filter-by-natural-language?query=palindromic%20strings"
```

**Delete a string:**
```bash
curl -X DELETE https://your-app-name.up.railway.app/api/v1/strings/racecar
```

### Step 8: Update README with Live URL

1. Open `README.md`
2. Update the line:
   ```markdown
   **Base URL**: `https://your-actual-app-name.up.railway.app`
   ```
3. Commit and push:
   ```bash
   git add README.md
   git commit -m "docs: update README with live deployment URL"
   git push origin master
   ```

## 🔧 Troubleshooting

### Build Failed

**Check logs:**
1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on the failed deployment
5. Read the build logs

**Common issues:**
- Missing dependencies → Check `requirements.txt`
- Python version → Railway uses Python 3.11 by default
- Import errors → Check your module paths

### Application Crashed

**Check runtime logs:**
1. In Railway dashboard, go to "Logs" tab
2. Look for error messages

**Common issues:**
- Database connection error → Check `DATABASE_URL` is set
- Port binding → Make sure you're using `$PORT` variable
- Import errors → Check file paths and module structure

### Database Not Working

**Verify database connection:**
1. Check that PostgreSQL addon is added
2. Verify `DATABASE_URL` variable exists
3. Check logs for connection errors

**Initialize database:**
The app should create tables automatically on first run, but if not:
- You may need to run migrations manually via Railway CLI

### 404 Errors

**Check your endpoints:**
- Remember the `/api/v1` prefix
- Correct endpoint: `/api/v1/strings/` not `/strings/`

## 🎯 Post-Deployment Tasks

### 1. Set up Custom Domain (Optional)

1. In Railway settings, go to "Domains"
2. Click "Custom Domain"
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update your DNS with the CNAME provided by Railway

### 2. Enable HTTPS (Automatic)

Railway automatically provisions SSL certificates for all domains.

### 3. Monitor Your Application

- Check "Metrics" tab for usage statistics
- Monitor "Logs" for errors
- Set up alerts if needed

### 4. Set up CI/CD

Railway automatically redeploys when you push to your GitHub repository:
```bash
git add .
git commit -m "Update feature"
git push origin master
```
Railway will detect the push and redeploy automatically!

## 💰 Railway Pricing

- **Free tier**: $5 of usage credits per month
- Enough for development and small projects
- Upgrade to "Hobby" plan for $5/month for more resources

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)

## 🎉 Success!

Once deployed, your API is live and accessible worldwide! 

**Your endpoints:**
- 📖 API Docs: `https://your-app.up.railway.app/docs`
- 🔗 Base URL: `https://your-app.up.railway.app/api/v1`

Share your API URL and start testing! 🚀