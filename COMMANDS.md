# Command Cheat Sheet - Copy/Paste These Commands

## Initial Setup (One Time Only)

### 1. Install Google Cloud CLI
**Mac:**
```bash
brew install google-cloud-sdk
```

**Windows:** Download from https://cloud.google.com/sdk/docs/install

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2. Login to Google Cloud
```bash
gcloud auth login
```

### 3. Create Project
```bash
gcloud projects create wilmington-half-marathon --name="Wilmington Half Marathon"
gcloud config set project wilmington-half-marathon
```

### 4. Enable Services
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Deploy Your App

### Navigate to your app folder:
```bash
cd ~/wilmington-training
```

### Deploy (first time and updates):
```bash
gcloud run deploy wilmington-training \
  --source . \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated \
  --memory 512Mi
```

**That's it!** You'll get a URL when it's done.

## Useful Commands

### Check if app is running:
```bash
gcloud run services describe wilmington-training --region us-east1
```

### View logs:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=wilmington-training" --limit 50
```

### Delete the app:
```bash
gcloud run services delete wilmington-training --region us-east1
```

### Update after making changes:
```bash
# Just run the same deploy command again
gcloud run deploy wilmington-training --source . --platform managed --region us-east1 --allow-unauthenticated
```

## Test Locally First

### Install dependencies:
```bash
pip install flask gunicorn
```

### Run locally:
```bash
python app.py
```

### Open in browser:
```
http://localhost:8080
```

### Stop local server:
Press `Ctrl+C`

## Need Help?

Just ask me in Claude! Copy any error messages you see and I'll help you fix them.
