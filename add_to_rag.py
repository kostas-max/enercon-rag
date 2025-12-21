import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pinecone import Pinecone
from dotenv import load_dotenv
import os
import hashlib

load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index('enercon')

def add_to_rag(text, title, category='general'):
    """Add content to RAG"""
    doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
    result = pc.inference.embed(model='multilingual-e5-large', inputs=[text], parameters={'input_type': 'passage'})
    index.upsert(vectors=[{
        "id": doc_id,
        "values": result.data[0].values,
        "metadata": {
            "text": text[:8000],
            "category": category,
            "title": title
        }
    }])
    print(f'✅ Added: {title} ({category}) - ID: {doc_id}')
    return doc_id

# === ΠΡΟΣΘΕΣΕ ΕΔΩ ΤΙΣ ΠΛΗΡΟΦΟΡΙΕΣ ===

# Παράδειγμα 1: Επαφή
add_to_rag(
    text="""
    Επαφή: Γιάννης Παπαδόπουλος
    Εταιρεία: Solar Tech AE
    Τηλέφωνο: 6971234567
    Email: giannis@solartech.gr
    Διεύθυνση: Λεωφ. Κηφισίας 100, Αθήνα
    Σημειώσεις: Προμηθευτής panels, καλές τιμές σε μεγάλες ποσότητες
    """,
    title="Επαφή: Γιάννης Παπαδόπουλος - Solar Tech",
    category="contact"
)

# Παράδειγμα 2: Σημείωση
add_to_rag(
    text="""
    Σημείωση: Νέος τιμοκατάλογος Huawei
    Ημερομηνία: Δεκέμβριος 2024
    Οι τιμές αυξήθηκαν 5% σε όλα τα inverters.
    Νέο μοντέλο SUN2000-12KTL διαθέσιμο από Ιανουάριο.
    """,
    title="Σημείωση: Νέος τιμοκατάλογος Huawei Δεκ 2024",
    category="note"
)

print('\n✅ Done! Οι πληροφορίες προστέθηκαν στο RAG.')
