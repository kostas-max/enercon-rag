import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index('enercon')

# Search for what we just added
queries = ['Γιάννης Παπαδόπουλος', 'Huawei τιμοκατάλογος 2024']
for q in queries:
    print(f'Search: {q}')
    result = pc.inference.embed(model='multilingual-e5-large', inputs=[q], parameters={'input_type': 'query'})
    results = index.query(vector=result.data[0].values, top_k=1, include_metadata=True)
    for m in results.matches:
        title = m.metadata.get('title', '')
        text = m.metadata.get('text', '')[:200]
        print(f'  Found: {title}')
        print(f'  Score: {m.score:.3f}')
        print(f'  Text: {text}...')
    print()
