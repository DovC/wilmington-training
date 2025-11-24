# Quick Start - Test Locally First

Before deploying to Google Cloud, you can test the app on your computer!

## Step 1: Install Python Requirements

Open Terminal, navigate to the app folder, and run:

```bash
pip install flask gunicorn
```

## Step 2: Run the App Locally

```bash
python app.py
```

You should see:
```
* Running on http://0.0.0.0:8080
```

## Step 3: Open in Browser

Go to: http://localhost:8080

You should see your training tracker! Try:
- Clicking "Mark Complete" on a workout
- Adding notes to a workout
- Watching the stats update

## Step 4: Stop the Server

Press `Ctrl+C` in Terminal

## Ready to Deploy?

Once you've tested locally and it looks good, follow the DEPLOYMENT_GUIDE.md to deploy to Google Cloud!
