# Dov's Deployment Profile - Wilmington Training App

**This is YOUR proven setup. Use this every time!**

---

## ✅ YOUR WORKING CONFIGURATION

### Project Details
- **Project ID:** `wilmington-half-marathon`
- **Service Name:** `wilmington-training`
- **Live URL:** https://wilmington-training-126906269448.us-east1.run.app/
- **Region:** us-east1

### Code Location
- **GitHub Repo:** https://github.com/DovC/wilmington-training
- **Branch:** main
- **Visibility:** Public ✅
- **Local Path:** `/Users/dov/Documents/wilmington-training`

### Your Proven Deployment Method
**✅ THIS METHOD WORKS FOR YOU:**

```bash
# In Cloud Shell (https://console.cloud.google.com):

cd ~
rm -rf wilmington-training  # Clean start
git clone https://github.com/DovC/wilmington-training.git
cd wilmington-training

# Manual image build (most reliable for your setup)
gcloud builds submit --tag gcr.io/wilmington-half-marathon/wilmington-training

# Deploy pre-built image
gcloud run deploy wilmington-training \
  --image gcr.io/wilmington-half-marathon/wilmington-training \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated \
  --project wilmington-half-marathon
```

**Deployment Time:** 10-15 minutes
**Success Rate:** 100% (as of Nov 25, 2024)

---

## 🎯 YOUR WORKFLOW FOR UPDATES

### Step 1: Update Code (5 minutes)
1. Make changes locally in `/Users/dov/Documents/wilmington-training`
2. Go to https://github.com/DovC/wilmington-training
3. Click file to edit (e.g., `app.py`)
4. Click pencil icon
5. Paste new content
6. Commit changes

**OR** if you get git/gcloud working locally later:
```bash
cd /Users/dov/Documents/wilmington-training
git add .
git commit -m "Updated [feature]"
git push origin main
```

### Step 2: Deploy (10 minutes)
Use the proven method above (Cloud Shell + manual build)

### Step 3: Verify (2 minutes)
1. Visit: https://wilmington-training-126906269448.us-east1.run.app/
2. Hard refresh: Cmd+Shift+R
3. Click "Initialize Training Plan"
4. Test new features

**Total Time: ~20 minutes**

---

## 🛠️ YOUR TOOLS

### What Works for You
- ✅ **Cloud Shell:** Always works, gcloud pre-authenticated
- ✅ **GitHub Web UI:** Easy file editing, no git commands
- ✅ **Manual image build:** Avoids Docker conflicts

### What Had Issues
- ⚠️ **Local gcloud:** "command not found" errors
- ⚠️ **Git authentication:** Token issues
- ⚠️ **Automatic Docker builds:** Python version conflicts

**Recommendation:** Stick with Cloud Shell for deployments

---

## 📁 YOUR PROJECT STRUCTURE

```
wilmington-training/
├── app.py                    # Backend (435 lines)
├── requirements.txt          # Dependencies (4 packages)
├── Dockerfile               # Container config
├── Procfile                 # Startup config
├── .gcloudignore            # Ignore file
└── templates/
    └── index.html           # Frontend (848 lines)
```

**Verify with:**
```bash
cd ~/wilmington-training
ls -la
ls -la templates/
wc -l app.py templates/index.html
```

---

## 🎯 YOUR FEATURE CHECKLIST

### Current Features (Working)
- ✅ 13-week training plan (Dec 1, 2025 - Feb 28, 2026)
- ✅ 2-on/1-off pattern (strict rest days)
- ✅ Day numbering (1-91)
- ✅ Color-coded workouts
- ✅ Log workouts (distance, pace, effort, notes)
- ✅ Edit workouts (modify, revert)
- ✅ 3-column dashboard
- ✅ Target paces reference card
- ✅ Weekly mileage chart (Planned vs Actual)
- ✅ Calendar and List views
- ✅ Mobile responsive
- ✅ Firestore persistence

### Files for Each Feature Type
- **Backend logic:** Edit `app.py`
- **UI/Display:** Edit `templates/index.html`
- **Paces/Plan:** Edit `app.py` (TRAINING_PLAN object)
- **Styling:** Edit `templates/index.html` (Tailwind classes)

---

## 🚨 TROUBLESHOOTING GUIDE

### Problem: App shows 500/503 error
**Solution:**
1. Go to: https://console.cloud.google.com/run
2. Click `wilmington-training`
3. Click LOGS tab
4. Look for Python errors
5. Most common: "ModuleNotFoundError: flask"
6. Fix: Redeploy with manual image build (your proven method)

### Problem: Changes don't appear
**Solution:**
1. Verify changes are on GitHub
2. Hard refresh browser: Cmd+Shift+R
3. Check deployment timestamp in Cloud Console
4. If old deployment, redeploy

### Problem: "Error loading training plan"
**Solution:**
1. Check Firestore: https://console.cloud.google.com/firestore
2. Database should exist in `us-east1`
3. If missing, create Native mode database
4. Click "Initialize Training Plan" button

### Problem: Chart not showing
**Solution:**
1. Click F12 → Console tab
2. Look for JavaScript errors
3. Most common: trainingPlan is null
4. Verify `/api/get_plan` endpoint works
5. Visit: https://wilmington-training-126906269448.us-east1.run.app/api/get_plan
6. Should return JSON data

---

## 📊 YOUR DEPLOYMENT HISTORY

### Successful Deployments

**Nov 25, 2024 - 2:35 PM EST**
- **Method:** Cloud Shell + Manual image build
- **Changes:** Added dashboard chart, edit feature, API endpoint
- **Result:** ✅ SUCCESS
- **Time:** 15 minutes (after troubleshooting)

**Nov 11, 2024**
- **Method:** Initial deployment
- **Result:** ✅ SUCCESS
- **URL:** https://wilmington-training-126906269448.us-east1.run.app/

### Failed Attempts (Don't Repeat!)
- ❌ Local gcloud (authentication issues)
- ❌ Automatic Docker build (Python version conflicts)
- ❌ Direct Cloud Run deploy (Flask not installed)

---

## 💡 LESSONS LEARNED

### What Works
1. ✅ Always use Cloud Shell (bypasses local issues)
2. ✅ Manual image build first (avoids conflicts)
3. ✅ Keep GitHub repo public (simplifies access)
4. ✅ Update via GitHub web UI (no git commands)
5. ✅ Test endpoints individually (/api/get_plan, /api/get_stats)

### What to Avoid
1. ❌ Fighting with local gcloud for >10 minutes
2. ❌ Trying to fix Docker automatic builds
3. ❌ Starting from scratch when something works
4. ❌ Forgetting to hard refresh after deployment

---

## 🎓 YOUR NEXT DEPLOYMENT

**When you want to update the app:**

1. **Open this file first!**
2. **Use the proven method** (Cloud Shell + manual build)
3. **Update your code** on GitHub web UI
4. **Run the commands** from "YOUR WORKING CONFIGURATION"
5. **Time estimate:** 20 minutes total

**Before asking for help, provide:**
- "I'm using my proven method from DEPLOYMENT_PROFILE.md"
- "Last successful deployment: [date]"
- Screenshot of any errors
- What you've changed

---

## 🔗 QUICK LINKS

**Your Dashboards:**
- App: https://wilmington-training-126906269448.us-east1.run.app/
- Cloud Run: https://console.cloud.google.com/run?project=wilmington-half-marathon
- Cloud Build: https://console.cloud.google.com/cloud-build/builds?project=wilmington-half-marathon
- Firestore: https://console.cloud.google.com/firestore?project=wilmington-half-marathon
- GitHub: https://github.com/DovC/wilmington-training
- Cloud Shell: https://console.cloud.google.com (click >_ icon)

**Your Endpoints (for testing):**
- Main app: https://wilmington-training-126906269448.us-east1.run.app/
- Stats API: https://wilmington-training-126906269448.us-east1.run.app/api/get_stats
- Plan API: https://wilmington-training-126906269448.us-east1.run.app/api/get_plan

---

## 📞 WHEN TO ASK FOR HELP

**Opening message template:**

> I'm deploying my Wilmington training app updates.
> 
> **Current setup:**
> - Project ID: wilmington-half-marathon
> - Live URL: https://wilmington-training-126906269448.us-east1.run.app/
> - GitHub: https://github.com/DovC/wilmington-training
> - Last deployed: [date] using Cloud Shell + manual build
> 
> **What I updated:** [files changed]
> 
> **Issue:** [describe problem or just say "ready to deploy"]
> 
> **Tried:** [what you've done so far]

**This gives me everything I need to help you in 5 minutes!**

---

*Keep this file updated after each successful deployment!*
*Add notes about what works/doesn't work for your setup*

**Last Updated:** November 25, 2024
**Working Status:** ✅ All systems operational
