#!/bin/bash

# Wilmington Training App - Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Configuration
PROJECT_NAME="wilmington-half-marathon"
SERVICE_NAME="wilmington-training"
REGION="us-east1"
REPO_URL="https://github.com/DovC/wilmington-training.git"

echo "📦 Cleaning up old code..."
cd ~
rm -rf wilmington-training

echo "📥 Cloning latest code from GitHub..."
git clone $REPO_URL
cd wilmington-training

echo "🏗️  Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_NAME/$SERVICE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_NAME/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --project $PROJECT_NAME

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app is live at: https://$SERVICE_NAME-126906269448.us-east1.run.app/"
