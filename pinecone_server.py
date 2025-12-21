"""
Pinecone Server με File Upload Support
"""
import asyncio
import websockets
import json
import base64
import os
import tempfile
from pinecone import Pinecone
import hashlib

# PDF extraction
import fitz  # PyMuPDF

# Excel extraction
import openpyxl
import pandas as pd

API_KEY = "pcsk_5cxk9S_U6bg96gFJEfFWm1da2fwmVqRdGd9cEt1UNq7WhznwJneHFwMH1EdQaKKLRkWuVH"
INDEX_NAME = "enercon"

pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)

def generate_smart_title(text, filename, part_num=None, total_parts=None):
    """Generate smart title from content"""
    import re
    
    # Try to find product names, brands, models
    brands = ['Fronius', 'SolaX', 'Solis', 'Huawei', 'BYD', 'JA Solar', 'Phono', 'HEXING', 'Dyness', 'Sungrow', 'GoodWe']
    categories = {
        'inverter': ['inverter', 'hybrid', 'GEN24', 'SYMO', 'PRIMO', 'SUN2000', 'X1-', 'X3-', 'S5-', 'S6-'],
        'battery': ['battery', 'μπαταρ', 'HVS', 'HVM', 'LUNA', 'Triple Power', 'T58', 'RESERVA', 'kWh storage'],
        'panel': ['panel', 'πάνελ', 'JAM', 'bifacial', 'mono', 'solar module', 'Wp'],
        'pricelist': ['τιμοκατάλογος', 'pricelist', 'τιμές', 'price', 'EUR', '€'],
        'quote': ['προσφορά', 'quote', 'quotation', 'σύστημα', 'εγκατάσταση']
    }
    
    # Find brand in text
    found_brand = None
    for brand in brands:
        if brand.lower() in text.lower():
            found_brand = brand
            break
    
    # Find category
    found_category = 'general'
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                found_category = cat
                break
        if found_category != 'general':
            break
    
    # Try to extract model numbers
    model_pattern = r'[A-Z]{1,3}[\d-]+[A-Z]*[\d]*[KkWw]*'
    models = re.findall(model_pattern, text[:500])
    found_model = models[0] if models else None
    
    # Build title
    title_parts = []
    if found_brand:
        title_parts.append(found_brand)
    if found_model and found_model not in str(found_brand):
        title_parts.append(found_model)
    
    # Add category description
    cat_names = {
        'inverter': 'Inverters',
        'battery': 'Μπαταρίες',
        'panel': 'Panels',
        'pricelist': 'Τιμοκατάλογος',
        'quote': 'Προσφορά',
        'general': ''
    }
    if cat_names.get(found_category):
        title_parts.append(cat_names[found_category])
    
    # If nothing found, use filename
    if not title_parts:
        title_parts.append(filename.rsplit('.', 1)[0])
    
    title = ' '.join(title_parts)
    
    # Add part number if multiple parts
    if total_parts and total_parts > 1:
        title = f"{title} (Part {part_num}/{total_parts})"
    
    return title, found_category
    """Extract text from PDF bytes"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text.strip()

def extract_text_from_excel(excel_bytes):
    """Extract text from Excel bytes - each row becomes searchable"""
    import io
    df = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None)
    
    all_text = []
    for sheet_name, sheet_df in df.items():
        all_text.append(f"=== Sheet: {sheet_name} ===")
        # Get headers
        headers = list(sheet_df.columns)
        
        # Convert each row to readable text
        for idx, row in sheet_df.iterrows():
            row_text = []
            for col in headers:
                val = row[col]
                if pd.notna(val):
                    row_text.append(f"{col}: {val}")
            if row_text:
                all_text.append(" | ".join(row_text))
    
    return "\n".join(all_text)

def chunk_by_sentences(text, max_sentences=25):
    """Split text by sentences, max 25-30 sentences per chunk"""
    import re
    # Split by sentence endings
    sentences = re.split(r'(?<=[.!?;])\s+', text)
    
    chunks = []
    current_chunk = []
    
    for sentence in sentences:
        current_chunk.append(sentence)
        if len(current_chunk) >= max_sentences:
            chunks.append(' '.join(current_chunk))
            # Keep last 3 sentences for overlap
            current_chunk = current_chunk[-3:]
    
    # Add remaining
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks if len(chunks) > 1 else [text]

def chunk_text(text, chunk_size=2000, overlap=200):
    """Split text into overlapping chunks by characters"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks

def smart_chunk(text, max_sentences=25, max_chars=3000):
    """Auto-detect best chunking method"""
    # Count sentences
    import re
    sentences = re.split(r'(?<=[.!?;])\s+', text)
    
    if len(sentences) > max_sentences:
        # Use sentence-based chunking
        return chunk_by_sentences(text, max_sentences)
    elif len(text) > max_chars:
        # Use character-based chunking
        return chunk_text(text, max_chars, 300)
    else:
        # No chunking needed
        return [text]

def search(query, top_k=5):
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    query_embedding = result.data[0].values
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    matches = []
    for match in results.matches:
        matches.append({
            "id": match.id,
            "score": round(match.score, 3),
            "title": match.metadata.get("title", "No title"),
            "category": match.metadata.get("category", ""),
            "text": match.metadata.get("text", "")[:500]
        })
    return matches

def upload_text(text, category, title):
    """Upload text document with auto-chunking if > 25 sentences"""
    chunks = smart_chunk(text, max_sentences=25, max_chars=3000)
    
    uploaded_ids = []
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            chunk_title = f"{title} (Part {i+1}/{len(chunks)})"
        else:
            chunk_title = title
            
        doc_id = hashlib.md5(chunk.encode()).hexdigest()[:16]
        result = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[chunk],
            parameters={"input_type": "passage"}
        )
        embedding = result.data[0].values
        index.upsert(vectors=[{
            "id": doc_id,
            "values": embedding,
            "metadata": {"text": chunk[:8000], "category": category, "title": chunk_title}
        }])
        uploaded_ids.append(doc_id)
    
    return uploaded_ids[0] if len(uploaded_ids) == 1 else uploaded_ids

def upload_file(file_data, filename, category):
    """Upload file (PDF, TXT, Excel) with auto-chunking"""
    # Decode base64
    file_bytes = base64.b64decode(file_data)
    
    # Extract text based on file type
    ext = filename.lower().split('.')[-1]
    
    if ext == 'pdf':
        text = extract_text_from_pdf(file_bytes)
    elif ext in ['xlsx', 'xls']:
        text = extract_text_from_excel(file_bytes)
    elif ext in ['txt', 'csv']:
        text = file_bytes.decode('utf-8', errors='ignore')
    else:
        return None, "Unsupported file type (use PDF, Excel, TXT, CSV)"
    
    if not text.strip():
        return None, "No text extracted from file"
    
    # Smart chunk - auto detects best method
    chunks = smart_chunk(text, max_sentences=25, max_chars=3000)
    
    uploaded = []
    for i, chunk in enumerate(chunks):
        # Generate smart title from content
        smart_title, detected_cat = generate_smart_title(
            chunk, 
            filename, 
            part_num=i+1 if len(chunks) > 1 else None,
            total_parts=len(chunks) if len(chunks) > 1 else None
        )
        
        # Use detected category if user selected 'general'
        final_category = detected_cat if category == 'general' else category
        
        doc_id = hashlib.md5(chunk.encode()).hexdigest()[:16]
        result = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[chunk],
            parameters={"input_type": "passage"}
        )
        embedding = result.data[0].values
        index.upsert(vectors=[{
            "id": doc_id,
            "values": embedding,
            "metadata": {"text": chunk[:8000], "category": final_category, "title": smart_title}
        }])
        uploaded.append({"id": doc_id, "title": smart_title})
    
    return uploaded, None

def get_stats():
    stats = index.describe_index_stats()
    return {
        "total_vectors": stats.total_vector_count,
        "dimension": stats.dimension
    }

def delete_doc(doc_id):
    index.delete(ids=[doc_id])
    return True

def list_docs(limit=50):
    """List all documents (sample)"""
    # Pinecone doesn't have direct list, so we do a broad search
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=["product equipment solar inverter panel battery price"],
        parameters={"input_type": "query"}
    )
    results = index.query(
        vector=result.data[0].values,
        top_k=limit,
        include_metadata=True
    )
    docs = []
    for match in results.matches:
        docs.append({
            "id": match.id,
            "title": match.metadata.get("title", "No title"),
            "category": match.metadata.get("category", "")
        })
    return docs

async def handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")
                
                if action == "search":
                    query = data.get("query", "")
                    top_k = data.get("top_k", 5)
                    results = search(query, top_k)
                    await websocket.send(json.dumps({
                        "action": "search_results",
                        "query": query,
                        "results": results
                    }))
                
                elif action == "upload":
                    text = data.get("text", "")
                    category = data.get("category", "general")
                    title = data.get("title", "")
                    doc_id = upload_text(text, category, title)
                    await websocket.send(json.dumps({
                        "action": "upload_success",
                        "doc_id": doc_id,
                        "title": title
                    }))
                
                elif action == "upload_file":
                    file_data = data.get("file_data", "")
                    filename = data.get("filename", "unknown")
                    category = data.get("category", "general")
                    
                    uploaded, error = upload_file(file_data, filename, category)
                    
                    if error:
                        await websocket.send(json.dumps({
                            "action": "error",
                            "message": error
                        }))
                    else:
                        await websocket.send(json.dumps({
                            "action": "file_upload_success",
                            "files": uploaded,
                            "count": len(uploaded)
                        }))
                
                elif action == "stats":
                    stats = get_stats()
                    await websocket.send(json.dumps({
                        "action": "stats",
                        "data": stats
                    }))
                
                elif action == "list":
                    docs = list_docs()
                    await websocket.send(json.dumps({
                        "action": "list_results",
                        "docs": docs
                    }))
                
                elif action == "delete":
                    doc_id = data.get("doc_id")
                    delete_doc(doc_id)
                    await websocket.send(json.dumps({
                        "action": "delete_success",
                        "doc_id": doc_id
                    }))
                    
            except Exception as e:
                print(f"Error: {e}")
                await websocket.send(json.dumps({
                    "action": "error",
                    "message": str(e)
                }))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    print("="*50)
    print("Pinecone Server with File Upload")
    print("WebSocket: ws://localhost:8765")
    print("="*50)
    async with websockets.serve(handler, "localhost", 8765, max_size=50*1024*1024):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
