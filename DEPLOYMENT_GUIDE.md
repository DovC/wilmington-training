# Wilmington Half Marathon Training Tracker - Deployment Guide

## 📋 What You're Getting

A complete web application that tracks your 13-week training plan with:
- ✅ Full training schedule (December 1, 2025 - February 28, 2026)
- ✅ Workout logging (mark complete, add notes)
- ✅ Progress tracking dashboard
- ✅ Mobile-friendly design
- ✅ Data persistence (your logged workouts are saved)

## 🚀 Step-by-Step Deployment to Google Cloud

### Prerequisites
1. A Google Cloud account (free tier is sufficient)
2. Terminal access on your computer

### Step 1: Install Google Cloud CLI

**On Mac:**
```bash
brew install google-cloud-sdk
```

**On Windows:**
Download and install from: https://cloud.google.com/sdk/docs/install

**On Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Step 2: Authenticate with Google Cloud

Open Terminal and run:
```bash
gcloud auth login
```

This will open a browser window. Log in with your Google account.

### Step 3: Create a New Google Cloud Project

```bash
gcloud projects create wilmington-half-marathon --name="Wilmington Half Marathon"
gcloud config set project wilmington-half-marathon
```

### Step 4: Enable Required Services

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 5: Navigate to Your App Directory

You'll need to download the app files to your computer first. Save all files to a folder called `wilmington-training`.

Then in Terminal:
```bash
cd ~/wilmington-training
```

### Step 6: Deploy to Google Cloud Run

This single command builds and deploys your app:

```bash
gcloud run deploy wilmington-training \
  --source . \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated \
  --memory 512Mi
```

This will take 2-3 minutes. When complete, you'll see a URL like:
`https://wilmington-training-xxxxxxxxx-ue.a.run.app`

**That's your app! Save this URL.**

## 📱 Accessing Your App

Just open the URL in any browser:
- On your phone
- On your computer  
- Share with others if you want

## 💾 Important: Data Persistence

**Current Setup:** Uses temporary storage (`/tmp/workout_data.json`)
- Your data persists during the deployment
- Redeploying will reset the data

**For Permanent Storage:** We can upgrade to use Google Firestore (still free tier). Let me know if you want this!

## 💰 Costs

**100% FREE** if you stay within these limits:
- 2 million requests per month (you'll use maybe 1,000)
- 360,000 GB-seconds of memory (you'll use a tiny fraction)
- 180,000 vCPU-seconds (again, tiny usage)

Your app will cost: **$0.00/month**

## 🔄 Updating Your App

When you want to make changes (like adjusting workouts), just:

1. Tell me what you want to change in Claude
2. I'll give you updated files
3. Replace the old files with new ones
4. Run the same deploy command:
   ```bash
   gcloud run deploy wilmington-training --source . --platform managed --region us-east1 --allow-unauthenticated
   ```

## 🎯 Using Your Training Tracker

### Logging a Workout:
1. Find the workout in your schedule
2. Click "Mark Complete" when done
3. Click "Add Details" to log:
   - Actual miles run
   - Actual pace
   - Notes (how you felt, weather, etc.)

### Viewing Progress:
- Top dashboard shows your stats
- Completed workouts turn green
- Track your mileage accumulation

## 🛠️ Troubleshooting

**App URL not working?**
```bash
gcloud run services describe wilmington-training --region us-east1
```

**Need to delete and redeploy?**
```bash
gcloud run services delete wilmington-training --region us-east1
# Then deploy again
```

**Check deployment logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=wilmington-training" --limit 50
```

## 📞 Need Help?

Just message me in Claude! I can:
- Help troubleshoot any errors
- Modify the training plan
- Add new features
- Upgrade to permanent storage
- Change the design

## 🎉 Your Training Plan Summary

**Start Date:** Monday, December 1, 2025
**Race Date:** Saturday, February 28, 2026
**Goal:** Sub 1:50:00 (8:24/mile pace)
**Pattern:** 2 days running, 1 day rest (continuous)
**Peak Mileage:** 40 miles (Weeks 9 & 10)
**Total Miles:** 428 miles over 13 weeks

Good luck with your training! 🏃💪
