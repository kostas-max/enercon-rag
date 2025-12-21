"""
Pinecone Tool για Enercon
Εργαλείο για upload και search στο Pinecone
"""

from pinecone import Pinecone
import sys
import json
import hashlib

# Config
API_KEY = "pcsk_5cxk9S_U6bg96gFJEfFWm1da2fwmVqRdGd9cEt1UNq7WhznwJneHFwMH1EdQaKKLRkWuVH"
INDEX_NAME = "enercon"

# Embedding μέσω Pinecone Inference API
def get_client():
    return Pinecone(api_key=API_KEY)

def get_embedding(pc, text):
    """Δημιουργία embedding για κείμενο"""
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "passage"}
    )
    return result.data[0].values

def get_query_embedding(pc, text):
    """Δημιουργία embedding για query"""
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "query"}
    )
    return result.data[0].values

def stats():
    """Εμφάνιση στατιστικών του index"""
    pc = get_client()
    index = pc.Index(INDEX_NAME)
    stats = index.describe_index_stats()
    print(f"Index: {INDEX_NAME}")
    print(f"Total vectors: {stats.total_vector_count}")
    print(f"Dimensions: {stats.dimension}")

def upload(text, category="general", title=""):
    """Upload ένα document στο Pinecone"""
    pc = get_client()
    index = pc.Index(INDEX_NAME)
    
    # Δημιουργία unique ID
    doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
    
    # Δημιουργία embedding
    embedding = get_embedding(pc, text)
    
    # Upload
    index.upsert(vectors=[{
        "id": doc_id,
        "values": embedding,
        "metadata": {
            "text": text,
            "category": category,
            "title": title
        }
    }])
    
    print(f"Uploaded: {title or doc_id}")
    print(f"Category: {category}")
    print(f"ID: {doc_id}")

def search(query, top_k=5):
    """Semantic search στο Pinecone"""
    pc = get_client()
    index = pc.Index(INDEX_NAME)
    
    # Δημιουργία query embedding
    query_embedding = get_query_embedding(pc, query)
    
    # Search
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    print(f"Search: '{query}'")
    print(f"Results: {len(results.matches)}")
    print("-" * 50)
    
    for i, match in enumerate(results.matches, 1):
        score = match.score
        metadata = match.metadata or {}
        title = metadata.get("title", "No title")
        category = metadata.get("category", "")
        text = metadata.get("text", "")[:200]
        
        print(f"\n{i}. {title} (score: {score:.3f})")
        if category:
            print(f"   Category: {category}")
        print(f"   {text}...")

def list_all():
    """Λίστα όλων των documents"""
    pc = get_client()
    index = pc.Index(INDEX_NAME)
    
    # Fetch με dummy query για να πάρουμε όλα
    stats_info = index.describe_index_stats()
    print(f"Total documents: {stats_info.total_vector_count}")

def delete(doc_id):
    """Διαγραφή document"""
    pc = get_client()
    index = pc.Index(INDEX_NAME)
    index.delete(ids=[doc_id])
    print(f"Deleted: {doc_id}")

def delete_all():
    """Διαγραφή όλων"""
    pc = get_client()
    index = pc.Index(INDEX_NAME)
    index.delete(delete_all=True)
    print("Deleted all vectors")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Pinecone Tool για Enercon
========================

Commands:
  stats              - Στατιστικά index
  upload             - Upload document (interactive)
  search <query>     - Αναζήτηση
  list               - Λίστα documents
  delete <id>        - Διαγραφή document
  delete_all         - Διαγραφή όλων

Examples:
  python pinecone_tool.py stats
  python pinecone_tool.py search "JA Solar 410W specs"
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "stats":
        stats()
    elif cmd == "upload":
        # Interactive mode
        print("=== Upload Document ===")
        title = input("Title: ")
        category = input("Category (panel/inverter/pump/general): ")
        print("Text (τελείωσε με κενή γραμμή):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)
        upload(text, category, title)
    elif cmd == "search":
        query = " ".join(sys.argv[2:])
        search(query)
    elif cmd == "list":
        list_all()
    elif cmd == "delete":
        doc_id = sys.argv[2]
        delete(doc_id)
    elif cmd == "delete_all":
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            delete_all()
    else:
        print(f"Unknown command: {cmd}")
