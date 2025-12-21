import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index('enercon')

# Stats
stats = index.describe_index_stats()
print('=== PINECONE MEMORY STATS ===')
print(f'Total vectors: {stats.total_vector_count}')
print()

# List all unique categories and titles
result = pc.inference.embed(model='multilingual-e5-large', inputs=['solar inverter panel battery email'], parameters={'input_type': 'query'})
results = index.query(vector=result.data[0].values, top_k=50, include_metadata=True)

categories = {}
for m in results.matches:
    cat = m.metadata.get("category", "unknown")
    if cat not in categories:
        categories[cat] = []
    categories[cat].append({
        'title': m.metadata.get("title", "")[:60],
        'score': m.score
    })

print('=== CONTENT BY CATEGORY ===')
for cat, items in sorted(categories.items()):
    print(f'\n📁 {cat.upper()} ({len(items)} items):')
    for item in items[:5]:
        print(f'   - {item["title"]}')
    if len(items) > 5:
        print(f'   ... και {len(items)-5} ακόμα')
