"""
Enercon RAG - Remote MCP Server (Production Ready)
FastAPI + Uvicorn | HTTP + WebSocket + SSE for Claude.ai
"""
from fastapi import FastAPI, HTTPException, Header, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import hashlib
import json
import os
import asyncio
import uuid
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

# CORS - Allow all for MCP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ MODELS ============
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AddRequest(BaseModel):
    text: str
    title: str
    category: Optional[str] = "note"

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

# ============ MCP TOOLS DEFINITION ============
MCP_TOOLS = [
    {
        "name": "rag_search",
        "description": "Αναζήτηση στο Enercon RAG Knowledge Base. Βρίσκει έγγραφα, emails, επαφές, τιμές φωτοβολταϊκών.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Τι ψάχνεις (π.χ. 'inverter Huawei τιμή', 'επαφή Γιάννης', 'email Big Solar')"},
                "top_k": {"type": "integer", "description": "Πόσα αποτελέσματα (default: 5)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "rag_add",
        "description": "Προσθήκη νέας πληροφορίας στο Enercon RAG (επαφή, σημείωση, τιμή, κλπ)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Το περιεχόμενο (π.χ. 'Επαφή: Γιάννης, Τηλ: 6971234567')"},
                "title": {"type": "string", "description": "Τίτλος για εύκολη αναγνώριση"},
                "category": {"type": "string", "description": "Κατηγορία: contact, note, pricelist, inverter, panel, battery, email, quote", "default": "note"}
            },
            "required": ["text", "title"]
        }
    },
    {
        "name": "rag_stats",
        "description": "Στατιστικά του Enercon RAG - πόσα έγγραφα, κατηγορίες κλπ",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

# ============ SSE/MCP ENDPOINT FOR CLAUDE.AI ============
@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for MCP - Claude.ai connects here"""
    async def event_generator():
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"
        
        # Keep connection alive
        while True:
            if await request.is_disconnected():
                break
            yield f"data: {json.dumps({'type': 'ping'})}\n\n"
            await asyncio.sleep(30)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/sse")
async def sse_post(request: Request):
    """Handle MCP messages from Claude.ai"""
    body = await request.json()
    method = body.get("method", "")
    params = body.get("params", {})
    msg_id = body.get("id", str(uuid.uuid4()))
    
    # Handle MCP methods
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
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": MCP_TOOLS}
        }
    
    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})
        
        try:
            if tool_name == "rag_search":
                results = do_search(args.get("query", ""), args.get("top_k", 5))
                content = "🔍 **Αποτελέσματα αναζήτησης:**\n\n"
                for r in results:
                    content += f"**{r['title']}** ({r['category']}) - Score: {r['score']}\n{r['text'][:200]}...\n\n"
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": content}]}
                }
            
            elif tool_name == "rag_add":
                doc_id = do_add(args.get("text", ""), args.get("title", ""), args.get("category", "note"))
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": f"✅ Προστέθηκε: {args.get('title')} (ID: {doc_id})"}]}
                }
            
            elif tool_name == "rag_stats":
                stats = do_stats()
                content = f"📊 **Enercon RAG Stats**\n\nTotal: {stats['total_vectors']} vectors\n\n"
                for cat in stats['categories']:
                    content += f"- {cat['name']}: {cat['count']}\n"
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": content}]}
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": str(e)}
            }
    
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"}
    }

# ============ HTTP ENDPOINTS ============
@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Enercon RAG MCP",
        "version": "1.0.0",
        "mcp_endpoint": "/sse",
        "web_ui": "/app",
        "endpoints": {
            "mcp_sse": "GET/POST /sse",
            "web_app": "GET /app",
            "search": "POST /rag/search",
            "add": "POST /rag/add",
            "stats": "GET /rag/stats",
            "websocket": "WS /ws"
        }
    }

# Mobile Web App
@app.get("/app", response_class=HTMLResponse)
async def web_app():
    """Mobile-friendly Web UI"""
    html_path = os.path.join(os.path.dirname(__file__), "pinecone_app_cloud.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Web App not found</h1>"

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "pinecone", "index": INDEX_NAME}

# Auth dependency
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.post("/rag/search")
async def rag_search(req: SearchRequest, api_key: str = Depends(verify_api_key)):
    try:
        return do_search(req.query, req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/add")
async def rag_add(req: AddRequest, api_key: str = Depends(verify_api_key)):
    try:
        doc_id = do_add(req.text, req.title, req.category)
        return {"success": True, "id": doc_id, "title": req.title, "category": req.category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rag/stats")
async def rag_stats(api_key: str = Depends(verify_api_key)):
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
            
            if api_key != API_SECRET:
                await websocket.send_json({"error": "Invalid API Key"})
                continue
            
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

# ============ RUN ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
