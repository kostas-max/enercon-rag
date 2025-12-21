# Enercon RAG - Knowledge Base για Φωτοβολταϊκά

AI-powered knowledge base για διαχείριση εγγράφων, emails και επαφών φωτοβολταϊκών συστημάτων.

## 🚀 Features

- 🔍 **Semantic Search** - Αναζήτηση με AI (RAG)
- 📄 **Document Upload** - PDF, Excel, TXT
- 📧 **Gmail Sync** - Συγχρονισμός emails
- 📅 **Google Calendar** - Events
- 👥 **Google Contacts** - Επαφές
- 📝 **Notes** - Σημειώσεις
- 🤖 **AI Assistant** - Claude integration
- 📊 **PDF Generator** - Δημιουργία προσφορών
- 🔌 **MCP Server** - Model Context Protocol για Claude Desktop
- 🌐 **Remote API** - FastAPI server για Claude.ai (Cloud)

---

## 📦 Installation

### 1. Clone
```bash
git clone https://github.com/kostas-max/enercon-rag.git
cd enercon-rag
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
```bash
cp .env.example .env
# Επεξεργάσου το .env με τα API keys σου
```

### 4. Run
```bash
python pinecone_server_v2.py
```
Άνοιξε το `pinecone_app_v2.html` στον browser.

---

## 🔌 MCP Server - Claude Desktop

Το Enercon RAG λειτουργεί ως **MCP Server** για Claude Desktop.

### Setup
Το αρχείο `claude_desktop_config.json` (συνήθως στο `%APPDATA%\Claude\`):
```json
{
  "mcpServers": {
    "enercon-rag": {
      "command": "python",
      "args": ["C:\\path\\to\\enercon-rag\\mcp_server.py"],
      "env": {
        "PINECONE_API_KEY": "your_key",
        "PINECONE_INDEX_NAME": "enercon"
      }
    }
  }
}
```

### Tools διαθέσιμα:
- `rag_search` - Αναζήτηση στη βάση
- `rag_add` - Προσθήκη πληροφοριών
- `rag_stats` - Στατιστικά

---

## 🌐 Remote API - Claude.ai (Cloud)

FastAPI server για σύνδεση με Claude.ai μέσω HTTP/WebSocket.

### Local Testing
```bash
python mcp_remote.py
# Τρέχει στο http://localhost:8008
```

### Endpoints
| Method | Endpoint | Περιγραφή |
|--------|----------|-----------|
| GET | `/` | Status |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| POST | `/rag/search` | Αναζήτηση |
| POST | `/rag/add` | Προσθήκη |
| GET | `/rag/stats` | Στατιστικά |
| WS | `/ws` | WebSocket |

### Authentication
Όλα τα endpoints (εκτός `/`, `/health`, `/docs`) χρειάζονται header:
```
X-API-Key: your_secret_key
```

---

## ☁️ Deploy στο Cloud

### Google Cloud Run
Δες [DEPLOY_CLOUD_RUN.md](DEPLOY_CLOUD_RUN.md)

```bash
gcloud run deploy enercon-rag \
  --source . \
  --region europe-west1 \
  --set-env-vars "PINECONE_API_KEY=xxx,MCP_API_SECRET=xxx"
```

### Άλλες επιλογές
- **Railway** - `railway up`
- **Render** - Connect GitHub repo
- **Heroku** - `git push heroku main`

---

## 🗄️ Multi-Database Support (Planned)

| Database | Use Case | Status |
|----------|----------|--------|
| Pinecone | Main RAG | ✅ Ready |
| PostgreSQL + pgvector | Code/Projects | 🔜 Coming |
| Redis | Cache/Fast access | 🔜 Coming |
| Qdrant | Alternative vectors | 🔜 Coming |

---

## 📁 File Structure

```
enercon-rag/
├── pinecone_server_v2.py   # WebSocket server για Web UI
├── pinecone_app_v2.html    # Frontend UI
├── mcp_server.py           # MCP Server για Claude Desktop
├── mcp_remote.py           # FastAPI server για Cloud
├── Dockerfile              # Για Cloud Run
├── add_to_rag.py           # Helper: προσθήκη στο RAG
├── check_memory.py         # Helper: έλεγχος μνήμης
├── search_test.py          # Helper: test αναζήτηση
├── .env.example            # Template για env variables
├── requirements.txt        # Python dependencies
├── requirements-remote.txt # Dependencies για remote server
├── DEPLOY_CLOUD_RUN.md     # Οδηγίες deployment
└── README.md
```

---

## 🔑 API Keys Required

| Service | Που το παίρνεις | Required |
|---------|-----------------|----------|
| Pinecone | [pinecone.io](https://pinecone.io) | ✅ Yes |
| Claude | [console.anthropic.com](https://console.anthropic.com) | Optional |
| Google OAuth | [console.cloud.google.com](https://console.cloud.google.com) | For Gmail/Calendar |

---

## 📝 License

MIT

## 👨‍💻 Author

Made with ❤️ by [kostas-max](https://github.com/kostas-max)
