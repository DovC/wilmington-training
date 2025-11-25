# 🚀 Deployment Quick Reference Card

**Print this and keep it handy!**

---

## ⚡ THE 5 MAGIC QUESTIONS

Before starting ANY deployment, answer these:

1. **Do you have an existing deployment?** YES / NO
   - If YES → URL: _______________________

2. **What deployment method worked last time?**
   - [ ] Cloud Shell
   - [ ] Local Terminal  
   - [ ] GitHub auto-deploy
   - [ ] Don't remember/First time

3. **Where is your code?**
   - GitHub URL: _______________________
   - Public or Private? _______________________

4. **What tools work for you RIGHT NOW?**
   - [ ] Cloud Shell (always works)
   - [ ] gcloud locally (type: `gcloud --version`)
   - [ ] GitHub web interface

5. **What are you updating?**
   - [ ] app.py
   - [ ] templates/index.html
   - [ ] Other: _______________________

---

## 🎯 FASTEST PATH DECISION

**Choose your scenario:**

### ✅ I have a working deployment + GitHub is public
```bash
# In Cloud Shell:
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
gcloud run deploy SERVICE_NAME \
  --source . \
  --region us-east1 \
  --allow-unauthenticated
```
**Time: 10 minutes**

---

### ✅ I have a working deployment + gcloud works locally
```bash
# In your Terminal:
cd /path/to/your/project
git pull origin main  # Get latest changes
gcloud run deploy SERVICE_NAME \
  --source . \
  --region us-east1 \
  --allow-unauthenticated
```
**Time: 5 minutes**

---

### ✅ First time deployment
```bash
# In Cloud Shell:
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Build image manually (avoids issues)
gcloud builds submit --tag gcr.io/PROJECT_ID/APP_NAME

# Deploy image
gcloud run deploy APP_NAME \
  --image gcr.io/PROJECT_ID/APP_NAME \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
```
**Time: 20 minutes**

---

### ✅ Docker build keeps failing
```bash
# Always use manual image build:
cd ~/your-project
gcloud builds submit --tag gcr.io/PROJECT_ID/APP_NAME
gcloud run deploy APP_NAME \
  --image gcr.io/PROJECT_ID/APP_NAME \
  --region us-east1 \
  --allow-unauthenticated
```
**Time: 15 minutes**

---

### ✅ gcloud not working / authentication issues
**→ Use Cloud Shell instead!**
1. Go to: console.cloud.google.com
2. Click terminal icon (>_) in top-right
3. gcloud is pre-installed and authenticated
4. Use commands above

**Time: +0 minutes (no local setup needed)**

---

## 🛑 TROUBLESHOOTING QUICK FIXES

| Problem | Quick Fix | Time |
|---------|-----------|------|
| "gcloud: command not found" | Use Cloud Shell | 0 min |
| "Authentication failed" | Use Cloud Shell | 0 min |
| GitHub is private | Make public OR use token | 2 min |
| Docker build fails | Manual image build (see above) | 5 min |
| "ModuleNotFoundError: flask" | Manual image build (see above) | 5 min |
| 500/503 errors | Check logs in Cloud Console | 2 min |
| Can't find files | `ls -la` to verify structure | 1 min |

---

## 📁 REQUIRED FILES CHECKLIST

Your project must have these files:

```
your-project/
├── app.py              ✓ Python backend
├── requirements.txt    ✓ Dependencies
├── Dockerfile         ✓ Container config
└── templates/
    └── index.html     ✓ Frontend
```

**Verify with:** `ls -la && ls -la templates/`

---

## ✅ REQUIRED FILE CONTENTS

### requirements.txt
```
Flask==3.0.0
Flask-CORS==4.0.0
google-cloud-firestore==2.13.1
gunicorn==21.2.0
```

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

---

## 🔍 POST-DEPLOYMENT CHECKS

After deploying, verify:

1. **Service is running:**
   - Go to: console.cloud.google.com/run
   - Service shows green checkmark
   
2. **App loads:**
   - Visit your URL
   - Page loads without errors
   
3. **Check logs if broken:**
   - Click service → LOGS tab
   - Look for red errors
   - Common: "ModuleNotFoundError" → Rebuild image

---

## 💾 YOUR PROJECT INFO (Fill this out!)

**Keep this updated for quick reference:**

- **Project ID:** _______________________
- **Service Name:** _______________________
- **Live URL:** _______________________
- **GitHub Repo:** _______________________
- **Deployment Method That Works:** _______________________

**Last Successful Deployment:**
- **Date:** _______________________
- **Command Used:** 
  ```
  
  
  ```

---

## ⚡ EMERGENCY: App is Down!

1. Go to: console.cloud.google.com/run
2. Click your service name
3. Click LOGS tab
4. Screenshot any red errors
5. Use Cloud Shell + manual image build (safest method)

---

## 📞 WHEN TO ASK FOR HELP

**Before asking, provide:**
- ✅ Filled deployment checklist
- ✅ Your project ID
- ✅ Live URL (if exists)
- ✅ GitHub repo URL
- ✅ Screenshots of errors
- ✅ What you've already tried

**Magic phrase:**
> "I have an existing deployment at [URL]. I deployed it before using [method]. 
> I want to update [files]. My project ID is [ID]. Can you help me use the same method?"

**This saves 2+ hours!**

---

## 🎓 LESSONS LEARNED

**Do:**
- ✅ Use Cloud Shell when local gcloud fails
- ✅ Manual image build if Docker errors
- ✅ Keep GitHub repo public (or use token)
- ✅ Save commands that work
- ✅ Check logs first when errors occur

**Don't:**
- ❌ Fight with local gcloud authentication
- ❌ Ignore existing working deployments
- ❌ Start from scratch if something already works
- ❌ Struggle for >10 min without changing approach

---

*Print this card and keep it by your desk!*
*Update it when you find better methods!*
