# Enercon RAG - Google Cloud Run Deployment Guide

## 📋 Prerequisites

1. Google Cloud Account
2. gcloud CLI installed
3. Billing enabled (για free tier αρκεί)

---

## 🔧 Install gcloud CLI

### Windows
```powershell
winget install Google.CloudSDK
```

### Mac
```bash
brew install google-cloud-sdk
```

### Linux
```bash
curl https://sdk.cloud.google.com | bash
```

Μετά την εγκατάσταση, **κλείσε και ξανάνοιξε το terminal**.

---

## 🚀 Quick Deploy (5 λεπτά)

### 1. Login
```bash
gcloud auth login
```
Θα ανοίξει browser για authentication.

### 2. Δημιούργησε Project (αν δεν έχεις)
```bash
gcloud projects create enercon-rag-project --name="Enercon RAG"
gcloud config set project enercon-rag-project
```

### 3. Enable APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 4. Deploy!
```bash
cd C:\Users\USER\Desktop\Enercon-RAG

gcloud run deploy enercon-rag \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "PINECONE_API_KEY=your_key_here,PINECONE_INDEX_NAME=enercon,MCP_API_SECRET=your_secret_here"
```

### 5. Done! 🎉
Θα πάρεις URL:
```
Service URL: https://enercon-rag-xxxxx-ew.a.run.app
```

---

## 🧪 Test

```bash
# Health check
curl https://enercon-rag-xxxxx-ew.a.run.app/health

# Search (με API key)
curl -X POST https://enercon-rag-xxxxx-ew.a.run.app/rag/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secret_here" \
  -d '{"query": "inverter", "top_k": 3}'
```

---

## 💰 Κόστος (Free Tier)

| Resource | Free/Month |
|----------|------------|
| Requests | 2 million |
| CPU | 180,000 vCPU-seconds |
| Memory | 360,000 GB-seconds |
| Networking | 1 GB outbound |

**Για development/testing = ΔΩΡΕΑΝ** ✅

---

## 🔐 Security Best Practices

1. **Άλλαξε το MCP_API_SECRET** σε κάτι δυνατό (32+ χαρακτήρες)

2. **Χρησιμοποίησε Secret Manager** (προαιρετικά):
```bash
gcloud secrets create pinecone-key --data-file=- <<< "your_key"
```

3. **Ενεργοποίησε authentication** (για production):
```bash
gcloud run deploy enercon-rag \
  --source . \
  --no-allow-unauthenticated
```

---

## 🔄 Update Deployment

Μετά από αλλαγές στον κώδικα:
```bash
gcloud run deploy enercon-rag --source .
```

---

## 📊 Monitoring

```bash
# Logs
gcloud run logs read enercon-rag

# Live logs
gcloud run logs tail enercon-rag
```

---

## 🗑️ Delete (αν θέλεις να σταματήσεις)

```bash
gcloud run services delete enercon-rag --region europe-west1
```

---

## ❓ Troubleshooting

### "gcloud not found"
Κλείσε και ξανάνοιξε το terminal μετά την εγκατάσταση.

### "Permission denied"
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### "Billing not enabled"
Πήγαινε στο https://console.cloud.google.com/billing και ενεργοποίησε billing.

### Build fails
Έλεγξε ότι υπάρχουν τα αρχεία:
- `Dockerfile`
- `mcp_remote.py`
- `requirements-remote.txt`
