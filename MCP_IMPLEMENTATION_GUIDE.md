# Enercon RAG - MCP Server Implementation Guide

## Πλήρης Οδηγός: Από Local Server σε Cloud Deployment

Αυτός ο οδηγός περιγράφει αναλυτικά πώς δημιουργήσαμε ένα **MCP (Model Context Protocol) Server** που επιτρέπει στο Claude AI να έχει πρόσβαση σε ένα custom RAG (Retrieval Augmented Generation) knowledge base.

---

## 📋 Περιεχόμενα

1. [Αρχιτεκτονική Συστήματος](#αρχιτεκτονική-συστήματος)
2. [Προαπαιτούμενα](#προαπαιτούμενα)
3. [MCP Server για Claude Desktop (Local)](#mcp-server-για-claude-desktop-local)
4. [Remote API Server (Cloud)](#remote-api-server-cloud)
5. [Google Cloud Run Deployment](#google-cloud-run-deployment)
6. [Mobile Web App](#mobile-web-app)
7. [Σύνδεση με Claude.ai (Remote MCP)](#σύνδεση-με-claudeai-remote-mcp)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)

---

## 🏗️ Αρχιτεκτονική Συστήματος

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENERCON RAG SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Claude     │     │   Claude.ai  │     │   Mobile     │    │
│  │   Desktop    │     │   (Web/App)  │     │   Browser    │    │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘    │
│         │                    │                    │             │
│         │ stdio              │ SSE/HTTP           │ HTTP        │
│         │                    │                    │             │
│  ┌──────▼───────┐     ┌──────▼────────────────────▼───────┐    │
│  │  mcp_server  │     │         mcp_remote.py             │    │
│  │    .py       │     │      (FastAPI Server)             │    │
│  │   (Local)    │     │    Google Cloud Run               │    │
│  └──────┬───────┘     └──────────────┬────────────────────┘    │
│         │                            │                          │
│         │                            │                          │
│         └────────────┬───────────────┘                          │
│                      │                                          │
│              ┌───────▼───────┐                                  │
│              │   Pinecone    │                                  │
│              │  Vector DB    │                                  │
│              │  (Cloud)      │                                  │
│              └───────────────┘                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Συνοπτικά:

| Component | Τεχνολογία | Χρήση |
|-----------|------------|-------|
| **mcp_server.py** | Python + MCP SDK | Claude Desktop (local, stdio) |
| **mcp_remote.py** | FastAPI + Uvicorn | Cloud API (HTTP/SSE/WebSocket) |
| **Pinecone** | Vector Database | Αποθήκευση embeddings |
| **Cloud Run** | Google Cloud | Hosting του remote server |

---

## 📦 Προαπαιτούμενα

### Software
- Python 3.10+
- pip
- Git
- Google Cloud SDK (για deployment)

### Accounts
- Pinecone account (δωρεάν tier)
- Google Cloud account (για Cloud Run)
- Anthropic account (για Claude)

### API Keys
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=enercon
MCP_API_SECRET=your_secret_key
```

---

## 🖥️ MCP Server για Claude Desktop (Local)

### Τι είναι το MCP;

Το **Model Context Protocol (MCP)** είναι ένα πρωτόκολλο που επιτρέπει σε AI assistants να συνδέονται με εξωτερικές πηγές δεδομένων και εργαλεία.

### Δομή Αρχείου: `mcp_server.py`

```python
"""
MCP Server για Claude Desktop
Επικοινωνία μέσω stdio (standard input/output)
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pinecone import Pinecone
import os

# Pinecone setup
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME", "enercon"))

# Create MCP Server
server = Server("enercon-rag")

# Define Tools
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="rag_search",
            description="Αναζήτηση στο Enercon RAG Knowledge Base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Τι ψάχνεις"},
                    "top_k": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="rag_add",
            description="Προσθήκη πληροφορίας στο RAG",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "title": {"type": "string"},
                    "category": {"type": "string", "default": "note"}
                },
                "required": ["text", "title"]
            }
        ),
        Tool(
            name="rag_stats",
            description="Στατιστικά του RAG",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "rag_search":
        results = do_search(arguments["query"], arguments.get("top_k", 5))
        return [TextContent(type="text", text=format_results(results))]
    
    elif name == "rag_add":
        doc_id = do_add(arguments["text"], arguments["title"], arguments.get("category", "note"))
        return [TextContent(type="text", text=f"✅ Added: {doc_id}")]
    
    elif name == "rag_stats":
        stats = do_stats()
        return [TextContent(type="text", text=format_stats(stats))]

# Helper functions
def do_search(query: str, top_k: int = 5):
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    return index.query(
        vector=result.data[0].values,
        top_k=top_k,
        include_metadata=True
    )

# Run server
async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Ρύθμιση στο Claude Desktop

Αρχείο: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "enercon-rag": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp_server.py"],
      "env": {
        "PINECONE_API_KEY": "your_key",
        "PINECONE_INDEX_NAME": "enercon"
      }
    }
  }
}
```

### Επανεκκίνηση Claude Desktop

Μετά την αλλαγή του config, κλείσε και άνοιξε ξανά το Claude Desktop.

---

## 🌐 Remote API Server (Cloud)

### Γιατί χρειάζεται;

- Claude.ai (web/mobile) δεν έχει πρόσβαση σε local servers
- Χρειάζεται **SSE (Server-Sent Events)** endpoint για MCP
- HTTP API για web apps και integrations

### Δομή Αρχείου: `mcp_remote.py`

```python
"""
Remote MCP Server - FastAPI
Υποστηρίζει: HTTP REST, WebSocket, SSE για Claude.ai
"""
from fastapi import FastAPI, HTTPException, Header, Depends, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from pinecone import Pinecone
import json
import os
import asyncio
import uuid

# Config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "enercon")
API_SECRET = os.getenv("MCP_API_SECRET", "your-secret")

# Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# FastAPI App
app = FastAPI(title="Enercon RAG API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ MODELS ============
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class AddRequest(BaseModel):
    text: str
    title: str
    category: str = "note"

# ============ HELPER FUNCTIONS ============
def do_search(query: str, top_k: int = 5):
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    results = index.query(
        vector=result.data[0].values,
        top_k=top_k,
        include_metadata=True
    )
    return [
        {
            "id": m.id,
            "title": m.metadata.get("title", ""),
            "category": m.metadata.get("category", ""),
            "text": m.metadata.get("text", "")[:500],
            "score": round(m.score, 3)
        }
        for m in results.matches
    ]

def do_add(text: str, title: str, category: str = "note"):
    import hashlib
    doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "passage"}
    )
    index.upsert(vectors=[{
        "id": doc_id,
        "values": result.data[0].values,
        "metadata": {"text": text[:8000], "category": category, "title": title}
    }])
    return doc_id

def do_stats():
    stats = index.describe_index_stats()
    # Get categories by searching
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=["solar inverter panel battery email"],
        parameters={"input_type": "query"}
    )
    results = index.query(vector=result.data[0].values, top_k=100, include_metadata=True)
    categories = {}
    for m in results.matches:
        cat = m.metadata.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "total_vectors": stats.total_vector_count,
        "categories": [{"name": k, "count": v} for k, v in sorted(categories.items())]
    }

# ============ MCP TOOLS DEFINITION ============
MCP_TOOLS = [
    {
        "name": "rag_search",
        "description": "Αναζήτηση στο Enercon RAG",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "rag_add",
        "description": "Προσθήκη στο RAG",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "title": {"type": "string"},
                "category": {"type": "string", "default": "note"}
            },
            "required": ["text", "title"]
        }
    },
    {
        "name": "rag_stats",
        "description": "Στατιστικά RAG",
        "inputSchema": {"type": "object", "properties": {}}
    }
]

# ============ SSE ENDPOINT FOR CLAUDE.AI ============
@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint - Claude.ai connects here"""
    async def event_generator():
        yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"
        while True:
            if await request.is_disconnected():
                break
            yield f"data: {json.dumps({'type': 'ping'})}\n\n"
            await asyncio.sleep(30)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.post("/sse")
async def sse_post(request: Request):
    """Handle MCP messages from Claude.ai"""
    body = await request.json()
    method = body.get("method", "")
    params = body.get("params", {})
    msg_id = body.get("id", str(uuid.uuid4()))
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "enercon-rag", "version": "1.0.0"},
                "capabilities": {"tools": {"listChanged": False}}
            }
        }
    
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": MCP_TOOLS}}
    
    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})
        
        if tool_name == "rag_search":
            results = do_search(args.get("query", ""), args.get("top_k", 5))
            content = "🔍 **Αποτελέσματα:**\n\n"
            for r in results:
                content += f"**{r['title']}** ({r['category']})\n{r['text'][:200]}...\n\n"
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": content}]}}
        
        elif tool_name == "rag_add":
            doc_id = do_add(args.get("text", ""), args.get("title", ""), args.get("category", "note"))
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": f"✅ Added: {doc_id}"}]}}
        
        elif tool_name == "rag_stats":
            stats = do_stats()
            content = f"📊 Total: {stats['total_vectors']} vectors\n"
            for cat in stats['categories']:
                content += f"- {cat['name']}: {cat['count']}\n"
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": content}]}}
    
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Unknown: {method}"}}

# ============ REST API ENDPOINTS ============
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/")
async def root():
    return {"status": "ok", "service": "Enercon RAG MCP", "endpoints": ["/sse", "/rag/search", "/rag/add", "/rag/stats", "/app"]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/rag/search")
async def api_search(req: SearchRequest, api_key: str = Depends(verify_api_key)):
    return do_search(req.query, req.top_k)

@app.post("/rag/add")
async def api_add(req: AddRequest, api_key: str = Depends(verify_api_key)):
    doc_id = do_add(req.text, req.title, req.category)
    return {"success": True, "id": doc_id}

@app.get("/rag/stats")
async def api_stats(api_key: str = Depends(verify_api_key)):
    return do_stats()

# ============ WEB APP ============
@app.get("/app", response_class=HTMLResponse)
async def web_app():
    html_path = os.path.join(os.path.dirname(__file__), "pinecone_app_cloud.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>App not found</h1>"

# ============ RUN ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
```

---

## ☁️ Google Cloud Run Deployment

### Βήμα 1: Εγκατάσταση gcloud CLI

**Windows:**
```powershell
winget install Google.CloudSDK
```

**Mac:**
```bash
brew install google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
```

### Βήμα 2: Αρχικοποίηση

```bash
# Login
gcloud auth login

# Create project
gcloud projects create enercon-rag --name="Enercon RAG"
gcloud config set project enercon-rag

# Enable billing (απαιτείται για Cloud Run)
# Πήγαινε: https://console.cloud.google.com/billing?project=enercon-rag

# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### Βήμα 3: Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-remote.txt .
RUN pip install --no-cache-dir -r requirements-remote.txt

COPY mcp_remote.py .
COPY pinecone_app_cloud.html .

EXPOSE 8080

CMD exec uvicorn mcp_remote:app --host 0.0.0.0 --port ${PORT:-8080}
```

### Βήμα 4: Requirements

**requirements-remote.txt:**
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pinecone>=3.0.0
python-dotenv>=1.0.0
```

### Βήμα 5: Deploy!

```bash
cd C:\Users\USER\Desktop\Enercon-RAG

gcloud run deploy enercon-rag \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "PINECONE_API_KEY=xxx,PINECONE_INDEX_NAME=enercon,MCP_API_SECRET=your-secret"
```

### Αποτέλεσμα

```
Service URL: https://enercon-rag-169291548488.europe-west1.run.app
```

---

## 📱 Mobile Web App

### URL
```
https://enercon-rag-169291548488.europe-west1.run.app/app
```

### Features
- 🔍 Αναζήτηση με quick filters
- 📊 Stats dashboard
- ➕ Προσθήκη εγγράφων
- 📱 Mobile-optimized UI
- 🔄 Real-time σύνδεση με Pinecone

---

## 🔗 Σύνδεση με Claude.ai (Remote MCP)

### Βήμα 1: Πήγαινε στο Claude.ai Settings

Settings → Connectors → Browse connectors

### Βήμα 2: Add Custom MCP Server

- Name: `ENERCON-RAG`
- URL: `https://enercon-rag-169291548488.europe-west1.run.app/sse`

### Βήμα 3: Test

Στο Claude.ai chat:
```
Ψάξε στο Enercon RAG για inverter Huawei
```

---

## 📚 API Reference

### Base URL
```
https://enercon-rag-169291548488.europe-west1.run.app
```

### Authentication
Όλα τα `/rag/*` endpoints χρειάζονται header:
```
X-API-Key: your-secret-key
```

### Endpoints

#### GET /
Status και διαθέσιμα endpoints

#### GET /health
Health check

#### GET /docs
Swagger UI documentation

#### POST /rag/search
Αναζήτηση στο RAG

**Request:**
```json
{
  "query": "inverter huawei",
  "top_k": 5
}
```

**Response:**
```json
[
  {
    "id": "abc123",
    "title": "Huawei SUN2000-10KTL",
    "category": "inverter",
    "text": "Huawei SUN2000-10KTL...",
    "score": 0.89
  }
]
```

#### POST /rag/add
Προσθήκη εγγράφου

**Request:**
```json
{
  "title": "Νέα επαφή",
  "text": "Γιάννης Παπαδόπουλος, τηλ: 6971234567",
  "category": "contact"
}
```

**Response:**
```json
{
  "success": true,
  "id": "xyz789"
}
```

#### GET /rag/stats
Στατιστικά

**Response:**
```json
{
  "total_vectors": 103,
  "categories": [
    {"name": "email", "count": 59},
    {"name": "inverter", "count": 14}
  ]
}
```

#### GET/POST /sse
MCP endpoint για Claude.ai

#### GET /app
Mobile Web UI

---

## 🔧 Troubleshooting

### "gcloud not found"
Κλείσε και ξανάνοιξε το terminal μετά την εγκατάσταση.

### "Container failed to start"
- Έλεγξε τα logs: `gcloud logging read "resource.type=cloud_run_revision" --limit=20`
- Συνήθως είναι θέμα με dependencies ή PORT

### "pinecone-client vs pinecone"
Χρησιμοποίησε `pinecone>=3.0.0` (όχι `pinecone-client`)

### "MCP connection error"
- Βεβαιώσου ότι το URL τελειώνει σε `/sse`
- Έλεγξε ότι το server τρέχει: `curl https://your-url.run.app/health`

### "Invalid API Key"
- REST endpoints: Header `X-API-Key`
- MCP/SSE: Δεν χρειάζεται (public για Claude.ai)

---

## 📁 Αρχεία Project

```
enercon-rag/
├── mcp_server.py           # Local MCP για Claude Desktop
├── mcp_remote.py           # Remote API + MCP για Cloud
├── pinecone_app_v2.html    # Desktop Web UI (localhost)
├── pinecone_app_cloud.html # Mobile Web UI (cloud)
├── pinecone_server_v2.py   # WebSocket server για desktop UI
├── Dockerfile              # Για Cloud Run
├── requirements.txt        # Όλα τα dependencies
├── requirements-remote.txt # Minimal για cloud
├── .env                    # Environment variables (not in git)
├── .env.example            # Template
├── .gitignore
└── README.md
```

---

## 🎉 Συμπέρασμα

Με αυτή την υλοποίηση έχεις:

1. ✅ **Local MCP Server** - Claude Desktop με direct πρόσβαση στο RAG
2. ✅ **Cloud API** - REST endpoints για οποιαδήποτε εφαρμογή
3. ✅ **Remote MCP** - Claude.ai (web/mobile) με SSE
4. ✅ **Mobile Web App** - Standalone UI για κινητό
5. ✅ **Pinecone Integration** - Scalable vector database

Όλα συνδέονται στην ίδια **Pinecone database**, οπότε τα δεδομένα είναι synchronized παντού!

---

## 📞 Links

- **Cloud API:** https://enercon-rag-169291548488.europe-west1.run.app
- **Mobile App:** https://enercon-rag-169291548488.europe-west1.run.app/app
- **Swagger Docs:** https://enercon-rag-169291548488.europe-west1.run.app/docs
- **GitHub:** https://github.com/kostas-max/enercon-rag
