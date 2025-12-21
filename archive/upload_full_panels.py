"""
Upload JA Solar & Phono panels με τιμές ανά ποσότητα
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

# === JA SOLAR PANELS ===
upload_doc("""JA Solar Φωτοβολταϊκά Πάνελ - Τιμοκατάλογος Big Solar 2025

ΤΙΜΕΣ ΑΝΑ ΠΟΣΟΤΗΤΑ ΠΑΡΑΓΓΕΛΙΑΣ:
- 0-100 kWp: Βασική τιμή
- 100-500 kWp: Μικρή έκπτωση
- >500 kWp: Μεγαλύτερη έκπτωση  
- Δίκτυο: Καλύτερη τιμή για συνεργάτες

=== JAM54D40 (N-type Bifacial, 1762x1134x30mm) ===
Ισχύς: 450/460W | Απόδοση: 22.5-23%

Τιμές EUR/Wp:
- 0-100 kWp: 0.133 EUR/Wp
- 100-500 kWp: 0.123 EUR/Wp
- >500 kWp: 0.113 EUR/Wp
- Δίκτυο: 0.108 EUR/Wp

Τιμή ανά πάνελ 460W:
- 0-100 kWp: 61.18 EUR
- 100-500 kWp: 56.58 EUR
- >500 kWp: 51.98 EUR
- Δίκτυο: 49.68 EUR

=== JAM72D40 (N-type Bifacial, 2333x1134x30mm) ===
Ισχύς: 600W | Απόδοση: 23%

Τιμές EUR/Wp:
- 0-100 kWp: 0.13€ EUR/Wp
- 100-500 kWp: 0.12€ EUR/Wp
- >500 kWp: 0.11€ EUR/Wp
- Δίκτυο: 0.105€ EUR/Wp

Τιμή ανά πάνελ 600W:
- 0-100 kWp: 78.00 EUR
- 100-500 kWp: 72.00 EUR
- >500 kWp: 66.00 EUR
- Δίκτυο: 63.00 EUR

=== JAM66D45 (N-type Bifacial, 2382x1134x30mm) ===
Ισχύς: 620W | Απόδοση: 22.7%

Τιμές EUR/Wp:
- 0-100 kWp: 0.13€ EUR/Wp
- 100-500 kWp: 0.12€ EUR/Wp
- >500 kWp: 0.11€ EUR/Wp
- Δίκτυο: 0.105€ EUR/Wp

=== JAM66D46 (N-type Bifacial, 2382x1303x33mm) ===
Ισχύς: 710W | Απόδοση: 22.9%

Τιμές EUR/Wp:
- 0-100 kWp: 0.13€ EUR/Wp
- 100-500 kWp: 0.12€ EUR/Wp
- >500 kWp: 0.11€ EUR/Wp
- Δίκτυο: 0.105€ EUR/Wp

Προμηθευτής: Big Solar AE
Τηλ: 210 5509090
""", "pricelist", "JA Solar Panels Τιμοκατάλογος με Εκπτώσεις 2025")

# === PHONO SOLAR PANELS ===
upload_doc("""Phono Solar Φωτοβολταϊκά Πάνελ - Τιμοκατάλογος Big Solar 2025

ΤΙΜΕΣ ΑΝΑ ΠΟΣΟΤΗΤΑ ΠΑΡΑΓΓΕΛΙΑΣ:
- 0-100 kWp: Βασική τιμή
- 100-500 kWp: Μικρή έκπτωση
- >500 kWp: Μεγαλύτερη έκπτωση
- Δίκτυο: Καλύτερη τιμή για συνεργάτες

=== PS450M6GFH-18/VNH (N-type Bifacial, 1722x1134x30mm) ===
Ισχύς: 450W | Απόδοση: 23.04%

Τιμές EUR/Wp:
- 0-100 kWp: 0.125€ EUR/Wp
- 100-500 kWp: 0.115€ EUR/Wp
- >500 kWp: 0.105€ EUR/Wp
- Δίκτυο: 0.14€ EUR/Wp

Τιμή ανά πάνελ 450W:
- 0-100 kWp: 56.25 EUR
- 100-500 kWp: 51.75 EUR
- >500 kWp: 47.25 EUR

=== PS620.M6GFH-22/VNH (N-type Bifacial, 2382x1134x30mm) ===
Ισχύς: 620W | Απόδοση: 22.95%

Τιμές EUR/Wp:
- 0-100 kWp: 0.125€ EUR/Wp
- 100-500 kWp: 0.115€ EUR/Wp
- >500 kWp: 0.105€ EUR/Wp
- Δίκτυο: 0.14€ EUR/Wp

Τιμή ανά πάνελ 620W:
- 0-100 kWp: 77.50 EUR
- 100-500 kWp: 71.30 EUR
- >500 kWp: 65.10 EUR

Προμηθευτής: Big Solar AE
Τηλ: 210 5509090
""", "pricelist", "Phono Solar Panels Τιμοκατάλογος με Εκπτώσεις 2025")

# Γενικός οδηγός τιμών
upload_doc("""Οδηγός Τιμών Φωτοβολταϊκών Πάνελ - Big Solar 2025

ΚΑΤΗΓΟΡΙΕΣ ΤΙΜΩΝ:
1. 0-100 kWp: Μικρές οικιακές εγκαταστάσεις (έως ~200 πάνελ)
2. 100-500 kWp: Μεσαίες εμπορικές (~200-1000 πάνελ)
3. >500 kWp: Μεγάλες εγκαταστάσεις (>1000 πάνελ)
4. Δίκτυο: Τιμές για συνεργάτες/εγκαταστάτες

ΣΥΓΚΡΙΣΗ ΤΙΜΩΝ EUR/Wp:

JA Solar JAM54D40 460W:
- Οικιακό (0-100kWp): 0.133 EUR/Wp = 61.18 EUR/panel
- Εμπορικό (100-500kWp): 0.123 EUR/Wp = 56.58 EUR/panel
- Μεγάλο (>500kWp): 0.113 EUR/Wp = 51.98 EUR/panel

JA Solar JAM72D40 600W:
- Οικιακό: 0.13 EUR/Wp = 78 EUR/panel
- Εμπορικό: 0.12 EUR/Wp = 72 EUR/panel
- Μεγάλο: 0.11 EUR/Wp = 66 EUR/panel

Phono Solar 450W:
- Οικιακό: 0.125 EUR/Wp = 56.25 EUR/panel
- Εμπορικό: 0.115 EUR/Wp = 51.75 EUR/panel
- Μεγάλο: 0.105 EUR/Wp = 47.25 EUR/panel

ΠΑΡΑΔΕΙΓΜΑ ΥΠΟΛΟΓΙΣΜΟΥ:
Για σύστημα 10kWp με JA Solar 460W:
- Χρειάζεσαι: 22 πάνελ (22 x 460W = 10.12kWp)
- Κατηγορία: 0-100kWp
- Κόστος: 22 x 61.18 = 1,345.96 EUR

Για σύστημα 20kWp με JA Solar 460W:
- Χρειάζεσαι: 44 πάνελ (44 x 460W = 20.24kWp)
- Κατηγορία: 0-100kWp
- Κόστος: 44 x 61.18 = 2,691.92 EUR

Προμηθευτής: Big Solar AE
""", "pricelist", "Οδηγός Τιμών Πάνελ - Υπολογισμός Κόστους")

print("\n=== Upload Complete ===")
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")
