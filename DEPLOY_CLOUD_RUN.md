# Enercon RAG - Google Cloud Run Deployment Guide

## Prerequisites

1. Google Cloud Account (έχεις ήδη)
2. gcloud CLI installed
3. Docker (προαιρετικό για local testing)

## Quick Deploy (5 λεπτά)

### 1. Login στο Google Cloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Deploy με ένα command!
```bash
gcloud run deploy enercon-rag \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "PINECONE_API_KEY=your_key,PINECONE_INDEX_NAME=enercon,MCP_API_SECRET=your_secret"
```

### 4. Παίρνεις URL!
```
Service URL: https://enercon-rag-xxxxx-ew.a.run.app
```

## Test
```bash
curl https://enercon-rag-xxxxx-ew.a.run.app/health
```

## Κόστος
- **Free tier:** 2 million requests/month
- **CPU:** 180,000 vCPU-seconds/month free
- **Memory:** 360,000 GB-seconds/month free

Για την χρήση σου (development/testing) = **ΔΩΡΕΑΝ**

## Security Tips
1. Άλλαξε το MCP_API_SECRET σε κάτι δυνατό
2. Μπορείς να βάλεις authentication στο Cloud Run
3. Χρησιμοποίησε Secret Manager για τα keys
