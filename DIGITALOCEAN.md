# 🌊 DigitalOcean Deployment Guide for String Analyzer API

## 📋 Overview

This guide will walk you through deploying your FastAPI String Analyzer application to DigitalOcean App Platform with a managed PostgreSQL database.

## ✅ Pre-Deployment Checklist

- [x] GitHub repository created and code pushed
- [x] `requirements.txt` with all dependencies
- [x] `app.yaml` configuration file created
- [x] `runtime.txt` specifying Python version
- [x] Database configuration supports PostgreSQL
- [x] `.gitignore` excludes sensitive files

## 💰 DigitalOcean Pricing

### Free Trial
- **$200 credit** for 60 days (new accounts)
- Credit card required for verification

### App Platform Pricing
- **Basic Plan**: $5/month (512 MB RAM, 1 vCPU)
- **Professional Plan**: Starting at $12/month

### Database Pricing
- **Development Database**: $7/month (1 GB RAM, 10 GB storage, 1 vCPU)
- **Production Database**: Starting at $15/month

**Total for hobby project**: ~$12/month (or free with credits)

## 🚀 Step-by-Step Deployment

### Step 1: Create DigitalOcean Account

1. Go to [https://www.digitalocean.com](https://www.digitalocean.com)
2. Click **"Sign Up"**
3. Create account with email or GitHub
4. Verify your email address
5. Add payment method (required, but you get $200 credit)

**Pro Tip**: If you're a student, check [GitHub Student Developer Pack](https://education.github.com/pack) for additional DigitalOcean credits!

---

### Step 2: Create New App

1. **Login to DigitalOcean dashboard**

2. Click **"Create"** → **"Apps"**

3. **Choose Source**:
   - Select **"GitHub"**
   - Click **"Authorize DigitalOcean"**
   - Grant access to your repositories

4. **Select Repository**:
   - Choose **"Kalanza/string-analyzer"**
   - Select branch: **"master"**
   - Check **"Autodeploy"** (deploys on every push)

5. Click **"Next"**

---

### Step 3: Configure Resources

#### App Configuration

DigitalOcean will auto-detect your app. Verify these settings:

**Name**: `string-analyzer-web` (auto-detected)

**Type**: Web Service

**Build Command**:
```bash
pip install -r requirements.txt
```

**Run Command**:
```bash
uvicorn string-analyzer.app.main:app --host 0.0.0.0 --port 8080
```

**Port**: `8080` (DigitalOcean default)

**Health Check Path**: `/docs` (optional)

**Instance Size**: 
- Select **"Basic"** ($5/month)
- 512 MB RAM / 1 vCPU

**Instance Count**: `1`

Click **"Next"**

---

### Step 4: Add Database

1. Click **"Add Resource"** → **"Database"**

2. **Database Configuration**:
   - **Engine**: PostgreSQL
   - **Version**: 15 (latest stable)
   - **Name**: `string-analyzer-db`
   - **Plan**: Development Database ($7/month)

3. **Connection**:
   - DigitalOcean automatically creates `DATABASE_URL` environment variable
   - App will be linked to the database

4. Click **"Next"**

---

### Step 5: Environment Variables

DigitalOcean automatically sets:
- `DATABASE_URL` (from PostgreSQL database)
- `PORT` (default 8080)

**Add additional variables** (optional):

| Key | Value | Encrypt |
|-----|-------|---------|
| `ENVIRONMENT` | `production` | No |

Click **"Next"**

---

### Step 6: Review and Deploy

1. **Review Summary**:
   - App Name: string-analyzer
   - Region: New York (or choose closest)
   - Resources: 1 web service + 1 database
   - Estimated cost: ~$12/month

2. Click **"Create Resources"**

3. **Wait for deployment** (3-5 minutes):
   - DigitalOcean will:
     - Clone your repository
     - Install dependencies
     - Build the application
     - Provision database
     - Deploy and start the app

4. **Monitor progress**:
   - Watch the **"Activity"** tab for build logs
   - Status will change: Building → Deploying → Active

---

### Step 7: Get Your App URL

Once deployed:

1. Go to **"Settings"** tab
2. Find **"Live App"** URL
3. Your URL will be like:
   ```
   https://string-analyzer-xxxxx.ondigitalocean.app
   ```

4. Click the URL or copy it

---

### Step 8: Test Your Deployment

#### Test API Documentation
```bash
https://your-app.ondigitalocean.app/docs
```

#### Test Endpoints with cURL

**Create a string:**
```bash
curl -X POST https://your-app.ondigitalocean.app/api/v1/strings/ \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

**Get a string:**
```bash
curl https://your-app.ondigitalocean.app/api/v1/strings/racecar
```

**List all strings:**
```bash
curl https://your-app.ondigitalocean.app/api/v1/strings/
```

**Filter palindromes:**
```bash
curl "https://your-app.ondigitalocean.app/api/v1/strings/?is_palindrome=true"
```

**NLP filter:**
```bash
curl "https://your-app.ondigitalocean.app/api/v1/strings/filter-by-natural-language?query=palindromic%20strings"
```

**Delete a string:**
```bash
curl -X DELETE https://your-app.ondigitalocean.app/api/v1/strings/racecar
```

#### Test with Python
```python
import requests

base_url = "https://your-app.ondigitalocean.app/api/v1"

# Create string
response = requests.post(
    f"{base_url}/strings/",
    json={"value": "hello world"}
)
print(response.json())

# Get string
response = requests.get(f"{base_url}/strings/hello%20world")
print(response.json())
```

---

### Step 9: Update README with Live URL

1. Open your `README.md`
2. Update the Live Demo section:
   ```markdown
   **Base URL**: `https://string-analyzer-xxxxx.ondigitalocean.app`
   ```

3. Commit and push:
   ```bash
   git add README.md
   git commit -m "docs: update with DigitalOcean deployment URL"
   git push origin master
   ```

4. DigitalOcean will auto-deploy the update!

---

## 🔧 Post-Deployment Configuration

### Custom Domain (Optional)

1. Go to **"Settings"** → **"Domains"**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `api.yourdomain.com`)
4. Update your DNS with the CNAME record provided
5. DigitalOcean automatically provisions SSL certificate

**Example DNS Settings:**
```
Type: CNAME
Name: api
Value: string-analyzer-xxxxx.ondigitalocean.app
TTL: 3600
```

---

### Database Management

#### Access Database
1. Go to your app dashboard
2. Click on **"string-analyzer-db"**
3. View **"Connection Details"**:
   - Host
   - Port
   - Username
   - Password
   - Database name

#### Connect with psql (locally)
```bash
psql "postgresql://username:password@host:port/database?sslmode=require"
```

#### View Database Metrics
- Go to database resource
- Check **"Insights"** tab for:
  - CPU usage
  - Memory usage
  - Connection count

---

### Enable Logs

1. Go to **"Runtime Logs"** tab
2. View real-time application logs
3. Filter by:
   - Build logs
   - Deploy logs
   - Runtime logs

**Download logs:**
```bash
# Install doctl (DigitalOcean CLI)
doctl apps logs <app-id>
```

---

### Scaling Your App

#### Vertical Scaling (More Power)
1. Go to **"Settings"**
2. Under **"Resources"** → **"string-analyzer-web"**
3. Click **"Edit Plan"**
4. Choose larger instance:
   - Basic: 512 MB → 1 GB RAM
   - Professional: 1-8 GB RAM

#### Horizontal Scaling (More Instances)
1. In resource settings
2. Increase **"Instance Count"**: 1 → 2+
3. DigitalOcean adds load balancer automatically

---

## 🔍 Monitoring & Maintenance

### View Metrics

**App Performance:**
1. Go to **"Insights"** tab
2. View:
   - Request rate
   - Response time
   - Error rate
   - Memory usage
   - CPU usage

### Set Up Alerts

1. Click **"Alerts"**
2. Configure notifications for:
   - High CPU usage
   - High memory usage
   - App downtime
   - Deploy failures

3. Add email or Slack integration

---

## 🐛 Troubleshooting

### Build Failed

**Check build logs:**
1. Go to **"Activity"** tab
2. Click on failed deployment
3. View **"Build Logs"**

**Common issues:**
- Missing dependencies → Check `requirements.txt`
- Python version mismatch → Check `runtime.txt`
- Import errors → Check module paths

**Fix:**
```bash
# Update files
git add .
git commit -m "fix: resolve build issues"
git push origin master
```

---

### App Crashes on Startup

**Check runtime logs:**
1. Go to **"Runtime Logs"** tab
2. Look for error messages

**Common issues:**
- Database connection failed → Check `DATABASE_URL`
- Port mismatch → Use port 8080
- Missing environment variables

**Test locally first:**
```bash
# Set DATABASE_URL to your DigitalOcean database
export DATABASE_URL="postgresql://..."
uvicorn string-analyzer.app.main:app --host 0.0.0.0 --port 8080
```

---

### Database Connection Issues

**Verify connection:**
1. Check environment variables in Settings
2. Ensure `DATABASE_URL` is set correctly
3. Check database is running (should be green)

**Test connection:**
```python
# Add to your app temporarily
from sqlalchemy import text
from app.db import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database connected!")
except Exception as e:
    print(f"Database error: {e}")
```

---

### 404 Errors

**Check your paths:**
- Endpoints are prefixed with `/api/v1`
- Correct: `https://your-app.ondigitalocean.app/api/v1/strings/`
- Wrong: `https://your-app.ondigitalocean.app/strings/`

---

### Slow Response Times

**Optimize database:**
1. Add indexes to frequently queried fields
2. Use connection pooling
3. Consider upgrading database plan

**Scale up:**
1. Increase app instance size
2. Add more instances
3. Enable caching

---

## 📱 DigitalOcean CLI (doctl)

### Install doctl

**Windows (PowerShell):**
```powershell
# Download from GitHub releases
# https://github.com/digitalocean/doctl/releases
```

**Mac/Linux:**
```bash
# Using Homebrew (Mac)
brew install doctl

# Using snap (Linux)
snap install doctl
```

### Authenticate
```bash
doctl auth init
# Enter your API token from DigitalOcean dashboard
```

### Useful Commands

```bash
# List apps
doctl apps list

# Get app info
doctl apps get <app-id>

# View logs
doctl apps logs <app-id>

# Create deployment
doctl apps create-deployment <app-id>

# List databases
doctl databases list
```

---

## 🔄 CI/CD with GitHub Actions (Optional)

DigitalOcean auto-deploys on push, but you can add tests first:

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to DigitalOcean

on:
  push:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest  # If you have tests

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to DigitalOcean
        run: echo "DigitalOcean auto-deploys on push"
```

---

## 💡 Best Practices

### 1. Use Environment Variables
- Never commit secrets
- Use `.env.example` for documentation
- Set all secrets in DigitalOcean dashboard

### 2. Enable Auto-Deploy
- ✅ Already enabled if you checked the box
- Automatically deploys when you push to master

### 3. Monitor Your App
- Check metrics regularly
- Set up alerts for critical issues
- Review logs for errors

### 4. Keep Dependencies Updated
```bash
pip list --outdated
pip install --upgrade package-name
```

### 5. Use Database Backups
- DigitalOcean automatically backs up databases daily
- You can restore from any backup point

---

## 📊 Cost Optimization

### For Development/Testing
- Use **Basic tier** ($5/month)
- Use **Development database** ($7/month)
- 1 instance
- **Total: ~$12/month**

### For Production
- Use **Professional tier** ($12+/month)
- Use **Production database** ($15+/month)
- 2+ instances for redundancy
- **Total: ~$40+/month**

### Free Tier Alternative
- Use $200 credit (60 days free)
- After credits: pause app when not in use
- Or migrate to Railway/Render free tier

---

## 🎓 Additional Resources

- [DigitalOcean App Platform Docs](https://docs.digitalocean.com/products/app-platform/)
- [DigitalOcean Databases Docs](https://docs.digitalocean.com/products/databases/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [DigitalOcean Community Tutorials](https://www.digitalocean.com/community/tags/fastapi)

---

## 🆘 Getting Help

### DigitalOcean Support
- Community forums
- Live chat (paid plans)
- Support tickets

### App Issues
- Check **Runtime Logs** first
- Review **Activity** tab for deployment history
- Test locally with same Python version

---

## ✅ Success Checklist

After deployment, verify:

- [ ] App is running (status: Active)
- [ ] Database is connected (green status)
- [ ] `/docs` endpoint works
- [ ] Can create strings via API
- [ ] Can retrieve strings via API
- [ ] Can filter strings
- [ ] Can delete strings
- [ ] Logs show no errors
- [ ] README updated with live URL
- [ ] Custom domain configured (optional)

---

## 🎉 Congratulations!

Your String Analyzer API is now live on DigitalOcean!

**Your endpoints:**
- 📖 API Docs: `https://your-app.ondigitalocean.app/docs`
- 🔗 Base URL: `https://your-app.ondigitalocean.app/api/v1`

Share your API and start building! 🚀

---

## 🔄 Next Steps

1. **Test all endpoints** thoroughly
2. **Update README** with live URL
3. **Add custom domain** (optional)
4. **Set up monitoring** and alerts
5. **Share your project** on GitHub!

**Need help?** Check the troubleshooting section or DigitalOcean docs!