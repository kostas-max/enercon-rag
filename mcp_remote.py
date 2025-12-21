"""
Enercon RAG - Remote MCP Server (Production Ready)
FastAPI + Uvicorn | HTTP + WebSocket | Port 8008
"""
from fastapi import FastAPI, HTTPException, Header, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import hashlib
import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "enercon")
API_SECRET = os.getenv("MCP_API_SECRET", "enercon-secret-2024")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not set!")

# Pinecone setup
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# FastAPI app
app = FastAPI(
    title="Enercon RAG API",
    description="Remote MCP Server για Claude.ai integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ AUTH ============
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# ============ MODELS ============
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AddRequest(BaseModel):
    text: str
    title: str
    category: Optional[str] = "note"

class SearchResult(BaseModel):
    id: str
    title: str
    category: str
    text: str
    score: float

class AddResponse(BaseModel):
    success: bool
    id: str
    title: str
    category: str

class StatsCategory(BaseModel):
    name: str
    count: int

class StatsResponse(BaseModel):
    total_vectors: int
    categories: List[StatsCategory]

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
    doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "passage"}
    )
    index.upsert(vectors=[{
        "id": doc_id,
        "values": result.data[0].values,
        "metadata": {
            "text": text[:8000],
            "category": category,
            "title": title
        }
    }])
    return doc_id

def do_stats():
    stats = index.describe_index_stats()
    
    # Get categories
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=["solar inverter panel battery email contact note"],
        parameters={"input_type": "query"}
    )
    results = index.query(
        vector=result.data[0].values,
        top_k=100,
        include_metadata=True
    )
    
    categories = {}
    for m in results.matches:
        cat = m.metadata.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_vectors": stats.total_vector_count,
        "categories": [{"name": k, "count": v} for k, v in sorted(categories.items())]
    }

# ============ HTTP ENDPOINTS ============
@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Enercon RAG MCP",
        "version": "1.0.0",
        "endpoints": {
            "search": "POST /rag/search",
            "add": "POST /rag/add",
            "stats": "GET /rag/stats",
            "websocket": "WS /ws"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "pinecone", "index": INDEX_NAME}

@app.post("/rag/search", response_model=List[SearchResult])
async def rag_search(req: SearchRequest, api_key: str = Depends(verify_api_key)):
    """🔍 Αναζήτηση στο RAG Knowledge Base"""
    try:
        return do_search(req.query, req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/add", response_model=AddResponse)
async def rag_add(req: AddRequest, api_key: str = Depends(verify_api_key)):
    """✍️ Προσθήκη νέας πληροφορίας στο RAG"""
    try:
        doc_id = do_add(req.text, req.title, req.category)
        return AddResponse(
            success=True,
            id=doc_id,
            title=req.title,
            category=req.category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rag/stats", response_model=StatsResponse)
async def rag_stats(api_key: str = Depends(verify_api_key)):
    """📊 Στατιστικά του RAG"""
    try:
        return do_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ WEBSOCKET ============
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            action = msg.get("action")
            api_key = msg.get("api_key", "")
            
            # Verify API key
            if api_key != API_SECRET:
                await websocket.send_json({"error": "Invalid API Key"})
                continue
            
            # Handle actions
            if action == "search":
                results = do_search(msg.get("query", ""), msg.get("top_k", 5))
                await websocket.send_json({"action": "search_results", "results": results})
            
            elif action == "add":
                doc_id = do_add(msg.get("text", ""), msg.get("title", ""), msg.get("category", "note"))
                await websocket.send_json({"action": "add_success", "id": doc_id})
            
            elif action == "stats":
                stats = do_stats()
                await websocket.send_json({"action": "stats", "data": stats})
            
            else:
                await websocket.send_json({"error": f"Unknown action: {action}"})
                
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")

# ============ RUN ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
