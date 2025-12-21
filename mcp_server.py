"""
Enercon RAG - MCP Server
Model Context Protocol server για Claude Desktop integration
"""
import asyncio
import json
import sys
from typing import Any
import hashlib

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Pinecone
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "enercon")

if not PINECONE_API_KEY:
    print("Error: PINECONE_API_KEY not set", file=sys.stderr)
    sys.exit(1)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Create MCP Server
app = Server("enercon-rag")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="rag_search",
            description="Αναζήτηση στο Enercon RAG Knowledge Base. Βρίσκει έγγραφα, emails, επαφές, τιμές φωτοβολταϊκών.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Τι ψάχνεις (π.χ. 'inverter Huawei τιμή', 'επαφή Γιάννης', 'email Big Solar')"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Πόσα αποτελέσματα (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="rag_add",
            description="Προσθήκη νέας πληροφορίας στο Enercon RAG (επαφή, σημείωση, τιμή, κλπ)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Το περιεχόμενο (π.χ. 'Επαφή: Γιάννης, Τηλ: 6971234567')"
                    },
                    "title": {
                        "type": "string",
                        "description": "Τίτλος για εύκολη αναγνώριση"
                    },
                    "category": {
                        "type": "string",
                        "description": "Κατηγορία: contact, note, pricelist, inverter, panel, battery, email, quote",
                        "default": "note"
                    }
                },
                "required": ["text", "title"]
            }
        ),
        Tool(
            name="rag_stats",
            description="Στατιστικά του Enercon RAG - πόσα έγγραφα, κατηγορίες κλπ",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a tool"""
    
    if name == "rag_search":
        query = arguments.get("query", "")
        top_k = arguments.get("top_k", 5)
        
        # Embed and search
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
        
        # Format results
        output = f"🔍 Αποτελέσματα για: {query}\n\n"
        for i, m in enumerate(results.matches, 1):
            title = m.metadata.get("title", "")
            category = m.metadata.get("category", "")
            text = m.metadata.get("text", "")[:300]
            score = m.score
            output += f"{i}. **{title}** [{category}] (score: {score:.2f})\n"
            output += f"   {text}...\n\n"
        
        if not results.matches:
            output += "Δεν βρέθηκαν αποτελέσματα."
        
        return [TextContent(type="text", text=output)]
    
    elif name == "rag_add":
        text = arguments.get("text", "")
        title = arguments.get("title", "")
        category = arguments.get("category", "note")
        
        # Create embedding and upsert
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
        
        return [TextContent(
            type="text",
            text=f"✅ Προστέθηκε στο RAG!\n\n**Τίτλος:** {title}\n**Κατηγορία:** {category}\n**ID:** {doc_id}"
        )]
    
    elif name == "rag_stats":
        stats = index.describe_index_stats()
        
        # Get category breakdown
        result = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=["solar inverter panel battery email contact"],
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
        
        output = f"📊 **Enercon RAG Stats**\n\n"
        output += f"**Total vectors:** {stats.total_vector_count}\n\n"
        output += "**Ανά κατηγορία:**\n"
        for cat, count in sorted(categories.items()):
            output += f"- {cat}: {count}\n"
        
        return [TextContent(type="text", text=output)]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
