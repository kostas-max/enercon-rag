"""
Upload JA Solar panels από Big Solar pricelist
"""
from pinecone import Pinecone
import hashlib

API_KEY = "pcsk_5cxk9S_U6bg96gFJEfFWm1da2fwmVqRdGd9cEt1UNq7WhznwJneHFwMH1EdQaKKLRkWuVH"
INDEX_NAME = "enercon"

pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)

def upload_doc(text, category, title):
    doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
    result = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={"input_type": "passage"}
    )
    embedding = result.data[0].values
    index.upsert(vectors=[{
        "id": doc_id,
        "values": embedding,
        "metadata": {"text": text, "category": category, "title": title}
    }])
    print(f"Uploaded: {title}")

# JA Solar Panel Pricelist
upload_doc("""JA Solar Φωτοβολταϊκά Πάνελ - Τιμοκατάλογος Big Solar 2025

JA SOLAR N-TYPE BIFACIAL DOUBLE GLASS 460W
Κωδικός: 0650/00330
Hail Resistance Class 4
Διαστάσεις: 1762x1134x30mm
Voc: 39.7V
Τιμή: 51.98 EUR/τεμάχιο
Τιμή ανά Watt: 0.113 EUR/W

JA Solar JAM54D40 Series (N-type Bifacial Double Glass):
- JAM54D40-435/LB: 435W
- JAM54D40-440/LB: 440W  
- JAM54D40-445/LB: 445W
- JAM54D40-450/LB: 450W
- JAM54D40-455/LB: 455W
- JAM54D40-460/LB: 460W (most popular)

Τεχνικά Χαρακτηριστικά JAM54D40-460/LB:
- Power: 460W
- Efficiency: 23.0%
- Voc: 39.70V
- Isc: 14.64A
- Vmp: 33.17V
- Imp: 13.87A
- Cells: 108 half-cells (6x18) Mono n-type
- Weight: 28kg
- Dimensions: 1762 x 1134 x 30mm
- Glass: Front 2.8mm / Back 2.0mm
- Bifaciality: 80% +/-5%
- Temperature Coefficient: -0.290%/°C
- Hail Resistance: Class 4 (HW4)
- Max System Voltage: 1500V DC
- Warranty: 25 years product, 30 years linear power

Εφαρμογές: Οικιακές εγκαταστάσεις, Εμπορικές στέγες, Utility scale
Προμηθευτής: Big Solar AE
""", "pricelist", "JA Solar Panels Τιμοκατάλογος Big Solar 2025")

# Huawei Inverters
upload_doc("""Huawei Inverters - Τιμοκατάλογος Big Solar 2025

HUAWEI SUN2000 Series - Smart String Inverters

Τριφασικοί Inverters:
- SUN2000-3KTL-M1: 3kW
- SUN2000-4KTL-M1: 4kW  
- SUN2000-5KTL-M1: 5kW
- SUN2000-6KTL-M1: 6kW
- SUN2000-8KTL-M1: 8kW
- SUN2000-10KTL-M1: 10kW - Τιμή: 965.48 EUR
- SUN2000-12KTL-M1: 12kW
- SUN2000-15KTL-M1: 15kW
- SUN2000-17KTL-M1: 17kW
- SUN2000-20KTL-M1: 20kW

Χαρακτηριστικά:
- Smart String Technology
- High efficiency >98%
- Multiple MPPT
- IP65 protection
- WiFi/4G monitoring
- Compatible με LUNA2000 batteries

Εγγύηση: 10 έτη Huawei
Προμηθευτής: Big Solar AE
""", "pricelist", "Huawei Inverters Τιμοκατάλογος Big Solar 2025")

print("\n=== Upload Complete ===")
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")
