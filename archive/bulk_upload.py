"""
Bulk upload για Enercon Pinecone
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

# === JA SOLAR JAM54D40 460W Panel ===
upload_doc("""JA Solar JAM54D40-460/LB
N-type Double Glass Bifacial Module - Black Frame
DEEP BLUE 4.0 Pro Series
Power: 435W - 460W range
Model JAM54D40-460/LB: 460W
Efficiency: 23.0%
Dimensions: 1762mm x 1134mm x 30mm
Weight: 28kg
Cells: 108 half-cells (6x18) Mono n-type
Voc: 39.70V
Isc: 14.64A
Vmp: 33.17V
Imp: 13.87A
Temperature Coefficient Pmax: -0.290%/C
Bifaciality: 80% +/-5%
Hail Resistance: Class 4 (HW4)
Maximum System Voltage: 1500V DC
Operating Temperature: -40C to +85C
Front/Back Glass: 2.8mm/2.0mm
Connector: MC4-EVO2A
Warranty: 25 years product, 30 years linear power
Certificates: IEC 61215, IEC 61730, UL 61215, UL 61730
Applications: Residential, Commercial rooftop, Utility scale
""", "panel", "JA Solar JAM54D40-460/LB N-type Bifacial")

# === Huawei Inverter 10KW ===
upload_doc("""Huawei SUN2000-10KTL-M1
Smart String Inverter 10kW
Three-phase inverter
Power: 10kW
Supplier: Big Solar
Price: 965.48 EUR per unit
Warranty: 10 years Huawei
Applications: Residential, Commercial
Features: Smart string technology, high efficiency
Compatible with: JA Solar panels, Huawei LUNA battery
""", "inverter", "Huawei SUN2000-10KTL-M1 10kW Inverter")

# === SolaX X1-HYBRID 5KW ===
upload_doc("""SolaX X1-HYBRID-5.0D G4
Single Phase Hybrid Inverter 5kW Generation 4
Power: 5kW
Dual MPPT with DC Switch
Supplier: Big Solar
Price: 844.80 EUR (network price)
Price tier 0-100kWp: 870 EUR
Price tier 100-500kWp: 862 EUR
Price tier >500kWp: 853 EUR
Warranty: 10 years SolaX
Compatible batteries: SolaX T58, Triple Power
Features: Hybrid operation, battery charging, grid-tied
""", "inverter", "SolaX X1-HYBRID-5.0D G4 5kW Hybrid Inverter")

# === SolaX T58 Battery ===
upload_doc("""SolaX T58 Master Pack 5.8kWh HV
High Voltage Lithium Battery
Capacity: 5.8kWh
Type: High Voltage (HV) Lithium
Supplier: Big Solar  
Price: 1560.00 EUR per unit
Recycling fee: 173.28 EUR
Warranty: 10 years SolaX
Compatible with: SolaX X1-HYBRID, X3-HYBRID inverters
Stackable: Yes
""", "battery", "SolaX T58 Master Pack 5.8kWh Battery")

# === Fronius Inverters ===
upload_doc("""Fronius Inverter Pricelist Big Solar 2025
Single Phase Inverters (Monofasikoi):
- PRIMO GEN24 3.0: 852-878 EUR
- PRIMO GEN24 3.6: 899-927 EUR
- PRIMO GEN24 4.0: 940-969 EUR
- PRIMO GEN24 4.6: 998-1028 EUR
- PRIMO GEN24 5.0: 1032-1063 EUR
- PRIMO GEN24 6.0: 1197-1233 EUR
- PRIMO GEN24 8.0: 1405-1448 EUR

Three Phase Inverters (Trifasikoi):
- SYMO 3.0-3-M: 976-1006 EUR
- SYMO GEN24 4.0: 1195-1232 EUR
- SYMO GEN24 6.0: 1412-1455 EUR
- SYMO GEN24 8.0: 1703-1754 EUR
- SYMO GEN24 10.0: 1806-1860 EUR
- SYMO ADVANCED 10.0-3-M: 1648-1698 EUR
- SYMO ADVANCED 15.0-3-M: 1883-1940 EUR
- SYMO ADVANCED 20.0-3-M: 1965-2025 EUR

Hybrid Inverters (Ybridikoi):
- PRIMO GEN24 3.0 PLUS: 1235-1272 EUR
- PRIMO GEN24 5.0 PLUS: 1495-1540 EUR
- SYMO GEN24 5.0 PLUS: 1610-1658 EUR
- SYMO GEN24 10.0 PLUS: 2305-2374 EUR
- VERTO PLUS 15 SPD: 2846-2933 EUR
- VERTO PLUS 20.0 SPD: 3240-3338 EUR
""", "pricelist", "Fronius Inverter Prices Big Solar 2025")

# === Solis Inverters ===
upload_doc("""Solis Inverter Pricelist Big Solar 2025
Single Phase (Monofasikoi):
- S6-GR1P0.7K-M: 236-244 EUR
- S6-GR1P3K-M: 374-385 EUR
- S6-GR1P5K: 557-574 EUR
- S6-GR1P6K: 584-602 EUR

Three Phase (Trifasikoi):
- S5-GR3P3K: 412-424 EUR
- S5-GR3P5K: 424-437 EUR
- S5-GR3P10K: 518-533 EUR
- S5-GR3P15K: 595-613 EUR
- S5-GR3P20K: 685-706 EUR
- S5-GC30K: 986-1016 EUR
- S5-GC50K: 1421-1464 EUR
- Solis-100K-5G-PRO: 2458-2533 EUR

Hybrid Three Phase:
- S6-EH3P5K-H-EU: 955-984 EUR
- S6-EH3P10K-H-EU: 1039-1070 EUR
- S6-EH3P20K-H: 1859-1915 EUR
- S6-EH3P50K-H: 4324-4455 EUR
""", "pricelist", "Solis Inverter Prices Big Solar 2025")

# === SolaX Full Pricelist ===
upload_doc("""SolaX Inverter Pricelist Big Solar 2025
Hybrid Single Phase (Monofasikoi):
- X1-HYBRID-3.0D: 761-784 EUR
- X1-HYBRID-5.0D: 845-870 EUR (Popular choice)
- X1-HYBRID-6.0D: 876-903 EUR
- X1-HYBRID-7.5D: 937-966 EUR

Hybrid Three Phase (Trifasikoi):
- X3-HYBRID-5.0-D: 1129-1163 EUR
- X3-HYBRID-8.0-D: 1246-1283 EUR
- X3-HYBRID-10.0-D: 1364-1406 EUR
- X3-HYBRID-15.0-D: 1571-1618 EUR

X3-Ultra Series:
- X3-ULT-15K: 2234-2302 EUR
- X3-ULT-20K: 2346-2417 EUR
- X3-ULT-25K: 2446-2520 EUR
- X3-ULT-30K: 2566-2643 EUR

Micro/Mini Inverters:
- X1-MINI-0.7K-G4: 226-232 EUR
- X1-MINI-2.0K-G4: 247-255 EUR
- X1-MINI-3.3K-G4: 360-371 EUR

Commercial/Industrial:
- X3-MGA-40K: 1620-1669 EUR
- X3-MGA-60K: 1800-1855 EUR
- X3-FTH-100K: 2736-2819 EUR
- X3-FTH-125K: 2964-3054 EUR
""", "pricelist", "SolaX Inverter Prices Big Solar 2025")

# === BYD Batteries ===
upload_doc("""BYD Battery Pricelist Big Solar 2025
Battery Modules:
- HVS module 2.56KWH: 950-979 EUR
- HVM module 2.75KWH: 950-979 EUR
- BCU + BASE: 467-481 EUR
- Max Lite Single Battery Module 7.5kWh: 1605-1654 EUR
- Max Lite cabinet with BDU: 6450-6645 EUR

High quality lithium battery storage
Compatible with: Fronius, SMA, Kostal inverters
Warranty: 10 years
""", "pricelist", "BYD Battery Prices Big Solar 2025")

# === SolaX Batteries ===
upload_doc("""SolaX Battery Pricelist Big Solar 2025
Triple Power Series:
- T-BAT H5.8 V2.1 (5.8kWh with BMS): 1560-1607 EUR
- HV11550 V2.1 (5.8kWh without BMS): 1380-1422 EUR
- T-BAT-SYS-HV-S2.5 (2.5kWh stackable): 696-717 EUR
- T-BAT-SYS-HV-S3.6 (3.6kWh stackable): 866-893 EUR

T58 Series:
- TBMS-S51-8: 660-680 EUR
- TSYS-HS51 5.1kWh 100Ah: 1140-1174 EUR
- TB-HR140 14kWh rack battery: 2220-2287 EUR

Accessories:
- T-BAT-Charger: 912-940 EUR
- X1-EPS Box: 192-198 EUR
- X3-EPS Box: 312-321 EUR
""", "pricelist", "SolaX Battery Prices Big Solar 2025")

# === Quote Example 20kW ===
upload_doc("""Quote Example: ARIKIDIS 20kW System
Customer: ARIKIDIS KONSTANTINOS
Location: Kavala, Greece
Date: 28/11/2025
Supplier: Big Solar AE

Equipment:
- 44x JA Solar N-TYPE BIFACIAL 460W panels = 20.24kWp total
  Price: 51.98 EUR/panel = 2287.12 EUR (0.113 EUR/W)
- 2x Huawei SUN2000-10KTL-M1 10kW inverters
  Price: 965.48 EUR/unit = 1930.96 EUR

Net Total: 4223.26 EUR
VAT 24%: 1013.58 EUR
Grand Total: 5236.84 EUR

Warranties:
- Panels: Manufacturer warranty (25 years)
- Inverters: 10 years Huawei

Delivery: 5 days via carrier
Payment: Upon agreement
""", "quote", "Quote 20kW System ARIKIDIS - Big Solar")

# === Quote Example 5kW Hybrid ===
upload_doc("""Quote Example: ARIKIDIS 5kW Hybrid System with Battery
Customer: ARIKIDIS KONSTANTINOS  
Location: Kavala, Greece
Date: 11/12/2025
Supplier: Big Solar AE

Equipment:
- 1x SolaX X1-HYBRID G4 5kW inverter: 844.80 EUR
- 1x SolaX Pocket WiFi V3.0-P: 12.00 EUR
- 1x SolaX Smart Meter DDSU666: 60.00 EUR
- 1x SolaX T58 Master Pack 5.8kWh battery: 1560.00 EUR
- Battery recycling fee: 173.28 EUR

Net Total: 2653.76 EUR
VAT 24%: 636.90 EUR
Grand Total: 3290.66 EUR

Warranties:
- Inverter: 10 years SolaX
- Battery: 10 years SolaX
- Accessories: Manufacturer warranty

Delivery: 5 days via carrier
""", "quote", "Quote 5kW Hybrid System with Battery - Big Solar")

print("\n=== Upload Complete ===")
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")
