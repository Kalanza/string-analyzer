# 🚀 Deploying String Analyzer API to Heroku

This guide will walk you through deploying your FastAPI application to Heroku with detailed explanations for each step.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Understanding the Deployment Process](#understanding-the-deployment-process)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Post-Deployment](#post-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

1. **Heroku Account** (Free)
   - Sign up at [heroku.com](https://signup.heroku.com/)
   - Free tier includes:
     - 550-1000 dyno hours/month
     - 10,000 rows PostgreSQL database (free tier)

2. **Heroku CLI Installed**
   - Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
   - Verify installation: `heroku --version`

3. **Git Installed**
   - Download from [git-scm.com](https://git-scm.com/downloads)
   - Verify: `git --version`

4. **Your Project Ready**
   - All code committed to Git
   - Required files present (we've already created them)

---

## Understanding the Deployment Process

### What Happens During Deployment?

1. **Code Upload**: Your code is pushed to Heroku's Git repository
2. **Buildpack Detection**: Heroku detects Python and installs dependencies
3. **Procfile Execution**: Heroku reads `Procfile` to know how to start your app
4. **Database Setup**: PostgreSQL database is created and connected
5. **App Launch**: Your FastAPI app starts running on Heroku's servers

### Key Files Explained

- **`Procfile`**: Tells Heroku how to run your app
  - `web:` - Defines the web process type
  - `uvicorn` - ASGI server that runs FastAPI
  - `--host 0.0.0.0` - Binds to all network interfaces
  - `--port $PORT` - Uses Heroku's dynamic port assignment

- **`requirements.txt`**: Lists all Python dependencies to install

- **`runtime.txt`**: Specifies Python version (3.11.0)

---

## Step-by-Step Deployment

### Step 1: Install and Login to Heroku CLI

**What this does**: Authenticates your terminal with your Heroku account

```powershell
# Install Heroku CLI if not already installed
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login
```

**Expected Result**: 
- Opens browser for authentication
- After login, terminal shows: "Logged in as your-email@example.com"

---

### Step 2: Initialize Git Repository (If Not Already Done)

**What this does**: Prepares your code for version control and deployment

```powershell
# Navigate to project root
cd "c:\Users\USER\Desktop\HNG projects\string-analyzer"

# Initialize git (skip if already done)
git init

# Check current status
git status
```

**Expected Result**: Shows untracked or modified files

---

### Step 3: Commit Your Code

**What this does**: Saves all your code changes to Git history

```powershell
# Add all files to staging
git add .

# Commit with descriptive message
git commit -m "Prepare for Heroku deployment"
```

**Expected Result**: 
```
[master abc1234] Prepare for Heroku deployment
 X files changed, Y insertions(+)
```

---

### Step 4: Create Heroku Application

**What this does**: Creates a new app container on Heroku servers

```powershell
# Create app with auto-generated name
heroku create

# OR create with custom name (must be unique globally)
heroku create your-string-analyzer-api
```

**Expected Result**:
```
Creating app... done, ⬢ your-string-analyzer-api
https://your-string-analyzer-api.herokuapp.com/ | https://git.heroku.com/your-string-analyzer-api.git
```

**Understanding the Output**:
- First URL: Your live app URL
- Second URL: Heroku's Git repository for deployment

---

### Step 5: Add PostgreSQL Database

**What this does**: Provisions a PostgreSQL database and sets DATABASE_URL automatically

```powershell
# Add Heroku Postgres (free tier)
heroku addons:create heroku-postgresql:mini
```

**Alternative for Older Accounts**:
```powershell
heroku addons:create heroku-postgresql:essential-0
```

**Expected Result**:
```
Creating heroku-postgresql:mini on ⬢ your-string-analyzer-api... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-xxxxx-xxxxx as DATABASE_URL
```

**What Happened**:
- PostgreSQL database created
- `DATABASE_URL` environment variable automatically set
- Your app can now connect to the database

---

### Step 6: Verify Configuration

**What this does**: Ensures all environment variables are set correctly

```powershell
# Check config variables
heroku config

# Should show:
# DATABASE_URL: postgres://user:pass@host:port/dbname
```

**Optional**: Add custom environment variables

```powershell
# Set environment to production
heroku config:set ENVIRONMENT=production
```

---

### Step 7: Deploy to Heroku

**What this does**: Uploads your code and starts the deployment process

```powershell
# Push code to Heroku
git push heroku master
```

**OR** if you're on a different branch:
```powershell
git push heroku main:master
```

**Expected Output** (This takes 1-3 minutes):
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
remote: -----> Building on the Heroku-22 stack
remote: -----> Using buildpack: heroku/python
remote: -----> Python app detected
remote: -----> Using Python version specified in runtime.txt
remote: -----> Installing python-3.11.0
remote: -----> Installing pip 23.x, setuptools 68.x and wheel 0.x
remote: -----> Installing SQLite3
remote: -----> Installing requirements with pip
remote:        Collecting fastapi>=0.104.0
remote:        Collecting uvicorn[standard]>=0.24.0
remote:        ...
remote:        Successfully installed fastapi-0.104.0 ...
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote: -----> Compressing...
remote: -----> Launching...
remote:        Released v5
remote:        https://your-string-analyzer-api.herokuapp.com/ deployed to Heroku
```

**Understanding the Build Process**:
1. **Buildpack Detection**: Heroku identifies Python project
2. **Python Installation**: Installs Python 3.11.0
3. **Dependency Installation**: Installs all packages from requirements.txt
4. **Process Configuration**: Reads Procfile
5. **Deployment**: App goes live

---

### Step 8: Scale the Web Dyno

**What this does**: Ensures at least one web process is running

```powershell
# Start one web dyno (free tier)
heroku ps:scale web=1
```

**Expected Result**:
```
Scaling dynos... done, now running web at 1:Free
```

---

### Step 9: Open Your Application

**What this does**: Opens your deployed app in the default browser

```powershell
# Open app in browser
heroku open
```

**OR** visit manually:
```
https://your-string-analyzer-api.herokuapp.com/docs
```

---

## Post-Deployment

### Verify Your Deployment

1. **Check API Documentation**
   ```
   https://your-app-name.herokuapp.com/docs
   ```
   Should show Swagger UI with all endpoints

2. **Test Endpoints**
   ```powershell
   # Health check
   curl https://your-app-name.herokuapp.com/api/v1/strings/
   
   # Create a string
   curl -X POST https://your-app-name.herokuapp.com/api/v1/strings/ `
     -H "Content-Type: application/json" `
     -d '{\"value\": \"racecar\"}'
   ```

3. **Check Application Logs**
   ```powershell
   # View real-time logs
   heroku logs --tail
   
   # View last 100 lines
   heroku logs -n 100
   ```

### Monitor Your Application

```powershell
# Check dyno status
heroku ps

# Check app info
heroku info

# Open dashboard
heroku dashboard
```

---

## Important Commands Reference

### Deployment Commands
```powershell
# Deploy changes
git add .
git commit -m "Update message"
git push heroku master

# Force deploy
git push heroku master --force
```

### Database Commands
```powershell
# Access database console
heroku pg:psql

# View database info
heroku pg:info

# Reset database (CAUTION: Deletes all data)
heroku pg:reset DATABASE_URL --confirm your-app-name
```

### Application Management
```powershell
# Restart app
heroku restart

# View config
heroku config

# Set environment variable
heroku config:set KEY=VALUE

# Unset environment variable
heroku config:unset KEY
```

### Logs and Debugging
```powershell
# Live logs
heroku logs --tail

# Search logs
heroku logs --tail | findstr "ERROR"

# View specific number of lines
heroku logs -n 500
```

---

## Troubleshooting

### Issue 1: Application Error (H10)

**Symptoms**: "Application Error" page when visiting your URL

**Causes**:
- No web dyno running
- Port binding issue
- Crash on startup

**Solutions**:
```powershell
# Check dyno status
heroku ps

# Scale web dyno
heroku ps:scale web=1

# Check logs
heroku logs --tail
```

### Issue 2: Module Not Found

**Symptoms**: Logs show `ModuleNotFoundError`

**Causes**:
- Missing package in requirements.txt
- Wrong import path

**Solutions**:
```powershell
# Verify requirements.txt includes all packages
# Redeploy
git add requirements.txt
git commit -m "Update dependencies"
git push heroku master
```

### Issue 3: Database Connection Error

**Symptoms**: "could not connect to database"

**Causes**:
- DATABASE_URL not set
- Database not provisioned

**Solutions**:
```powershell
# Check config
heroku config

# If DATABASE_URL missing, add database
heroku addons:create heroku-postgresql:mini

# Restart app
heroku restart
```

### Issue 4: Build Failed

**Symptoms**: Deployment stops with build error

**Causes**:
- Syntax error in code
- Incompatible dependencies
- Wrong Python version

**Solutions**:
```powershell
# Check build logs carefully
heroku logs --tail

# Test locally first
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn string-analyzer.app.main:app --reload
```

### Issue 5: Slug Size Too Large

**Symptoms**: "Compiled slug size exceeds the limit"

**Causes**:
- Too many dependencies
- Large files in repository

**Solutions**:
```powershell
# Create .slugignore file
echo tests/ > .slugignore
echo *.pyc >> .slugignore
echo __pycache__/ >> .slugignore

# Commit and redeploy
git add .slugignore
git commit -m "Add slugignore"
git push heroku master
```

---

## Cost Considerations

### Free Tier Limits
- **Dyno Hours**: 550 hours/month (1000 with credit card)
- **Database**: 10,000 rows max
- **Bandwidth**: Limited but sufficient for small apps
- **Sleep**: App sleeps after 30 minutes of inactivity
- **Wake Time**: ~10 seconds from sleep

### Keeping App Awake (Optional)
Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your app every 25 minutes.

---

## Next Steps

1. **Update README**: Add your Heroku URL to README.md
2. **Set Up CI/CD**: Configure automatic deployments from GitHub
3. **Monitor**: Set up alerts and monitoring
4. **Optimize**: Enable caching and optimize database queries
5. **Scale**: Upgrade dyno/database as needed

---

## Additional Resources

- [Heroku Python Documentation](https://devcenter.heroku.com/categories/python-support)
- [Heroku PostgreSQL](https://devcenter.heroku.com/articles/heroku-postgresql)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/heroku/)
- [Heroku CLI Commands](https://devcenter.heroku.com/articles/heroku-cli-commands)

---

## Summary Checklist

- [ ] Heroku CLI installed and logged in
- [ ] Code committed to Git
- [ ] Heroku app created
- [ ] PostgreSQL database added
- [ ] Code deployed (`git push heroku master`)
- [ ] Web dyno scaled (`heroku ps:scale web=1`)
- [ ] App tested and working
- [ ] Logs monitored for errors
- [ ] Documentation updated with live URL

**Congratulations! Your String Analyzer API is now live on Heroku! 🎉**
