"""Test upload για Pinecone"""
from pinecone import Pinecone
import hashlib

API_KEY = "pcsk_5cxk9S_U6bg96gFJEfFWm1da2fwmVqRdGd9cEt1UNq7WhznwJneHFwMH1EdQaKKLRkWuVH"
INDEX_NAME = "enercon"

pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)

# Test document - JA Solar panel specs
text = """JA Solar JAM54S30-410/MR
Monocrystalline PERC Half-Cell Module
Power: 410W
Efficiency: 21.3%
Dimensions: 1722 x 1134 x 30mm
Weight: 21.5kg
Cells: 108 half-cells
Voc: 37.09V
Isc: 13.92A
Vmp: 31.12V
Imp: 13.18A
Temperature Coefficient: -0.35%/°C
Warranty: 12 years product, 25 years performance
Applications: Residential, Commercial rooftop installations
"""

# Create embedding
result = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[text],
    parameters={"input_type": "passage"}
)
embedding = result.data[0].values

# Upload
doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
index.upsert(vectors=[{
    "id": doc_id,
    "values": embedding,
    "metadata": {
        "text": text,
        "category": "panel",
        "title": "JA Solar JAM54S30-410/MR"
    }
}])

print(f"Uploaded: JA Solar JAM54S30-410/MR")
print(f"ID: {doc_id}")
