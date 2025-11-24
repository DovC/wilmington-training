# 🏃 Wilmington Half Marathon Training Tracker
# wilmington Half training plan

A complete web application for tracking your 13-week half marathon training plan.

## 📦 What's Included

### Files:
- `app.py` - Main Flask application (Python backend)
- `templates/index.html` - Web interface (HTML/CSS/JavaScript)
- `requirements.txt` - Python dependencies
- `Dockerfile` - For containerized deployment
- `.gcloudignore` - Google Cloud deployment config

### Documentation:
- `DEPLOYMENT_GUIDE.md` - Complete Google Cloud deployment instructions
- `QUICK_START.md` - Test the app locally before deploying
- `README.md` - This file

## 🎯 Your Training Plan

- **Race:** Wilmington Half Marathon
- **Date:** Saturday, February 28, 2026
- **Start Date:** Monday, December 1, 2025
- **Goal:** Sub 1:50:00 (8:24/mile pace)
- **Total Weeks:** 13
- **Total Miles:** 429 miles
- **Pattern:** 2 days running, 1 day rest (continuous cycle)
- **Peak Weeks:** 40 miles (Weeks 9 & 10)

### Training Phases:
1. **Weeks 1-4:** Base Building (27-32 miles)
2. **Weeks 5-6:** Early Quality (35-36 miles)
3. **Weeks 7-8:** Transition Quality (38-40 miles)
4. **Weeks 9-10:** Peak Phase (40 miles)
5. **Week 11:** Recovery & Transition (34 miles)
6. **Weeks 12-13:** Taper (26 miles, then race week)

### Training Paces (VDOT 39-40):
- **Easy (E):** 9:45-10:30/mile
- **Marathon (M):** 8:45-9:00/mile
- **Threshold (T):** 8:05-8:15/mile
- **Interval (I):** 7:30-7:40/mile
- **Goal Race Pace:** 8:20-8:25/mile

## ✨ Features

### Tracking Capabilities:
- ✅ View complete 13-week training schedule
- ✅ Mark workouts as completed
- ✅ Log actual miles and pace for each workout
- ✅ Add detailed notes (how you felt, weather, etc.)
- ✅ Progress dashboard with statistics
- ✅ Mobile-friendly responsive design
- ✅ Data persists between sessions

### Dashboard Stats:
- Total workouts completed
- Completion percentage
- Miles completed vs. planned
- Weeks remaining to race

## 🚀 Getting Started

### Option 1: Test Locally (Recommended First)
See `QUICK_START.md` for instructions to run on your computer.

### Option 2: Deploy to Google Cloud
See `DEPLOYMENT_GUIDE.md` for complete deployment instructions.

## 💾 Data Storage

**Current Setup:** 
- Uses temporary file storage (`/tmp/workout_data.json`)
- Data persists during deployment lifetime
- Redeploying resets data

**Future Enhancement:**
- Can upgrade to Google Firestore for permanent storage
- Still within Google Cloud's free tier
- Let me know if you want this upgrade!

## 🔄 Making Updates

To modify your training plan or app features:

1. Chat with me in Claude about desired changes
2. I'll provide updated files
3. Replace old files with new versions
4. Redeploy using the same command:
   ```bash
   gcloud run deploy wilmington-training --source . --platform managed --region us-east1 --allow-unauthenticated
   ```

## 📱 Using the App

### Logging Workouts:
1. Find your workout in the schedule
2. Click **"Mark Complete"** when finished
3. Click **"Add Details"** to record:
   - Actual distance run
   - Actual pace achieved
   - Notes about the workout

### Viewing Progress:
- Dashboard at top shows overall statistics
- Completed workouts highlighted in green
- Rest days shown in yellow
- Scroll through all 13 weeks

## 💰 Cost

**FREE!** The app stays well within Google Cloud's free tier:
- 2 million requests/month (you'll use ~1,000)
- 360,000 GB-seconds memory
- 180,000 vCPU-seconds

Expected monthly cost: **$0.00**

## 🛠️ Technical Stack

- **Backend:** Python 3.11, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Docker, Google Cloud Run
- **Storage:** JSON file (upgradeable to Firestore)

## 📞 Support

Need help or want to make changes? Just message me in Claude! I can:
- Troubleshoot deployment issues
- Modify the training plan
- Add new features
- Change the design
- Upgrade to permanent storage
- Help with any errors

## 📝 Training Plan Notes

Your plan follows **Jack Daniels' training methodology**:
- Maintains 2-on/1-off running pattern throughout
- 50-60% easy running volume
- Quality workouts: Tempo, Intervals, Race Pace
- Progressive long runs building to 16 miles
- Strategic recovery weeks (Week 4, Week 11)
- Proper 2-week taper

## 🎉 Good Luck!

Your training starts December 1st. Stay consistent with the pattern, listen to your body, and you'll crush that sub-1:50 goal!

Questions? Updates needed? Just ask! 💪🏃
