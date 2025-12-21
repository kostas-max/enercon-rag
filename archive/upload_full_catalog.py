"""
ΠΛΗΡΗΣ Κατάλογος Big Solar 2025 - Όλα τα προϊόντα
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
    print(f"OK: {title}")

print("=== UPLOADING FULL BIG SOLAR CATALOG 2025 ===\n")

# ============ FRONIUS INVERTERS ============
upload_doc("""Fronius Μονοφασικοί Inverters - Τιμοκατάλογος Big Solar 2025

PRIMO GEN24 Series (Single Phase):

PRIMO GEN24 3.0 (3kW):
- 0-100 kWp: 878€ | 100-500 kWp: 869€ | >500 kWp: 860€ | Δίκτυο: 852€

PRIMO GEN24 3.6 (3.6kW):
- 0-100 kWp: 927€ | 100-500 kWp: 918€ | >500 kWp: 908€ | Δίκτυο: 899€

PRIMO GEN24 4.0 (4kW):
- 0-100 kWp: 969€ | 100-500 kWp: 959€ | >500 kWp: 950€ | Δίκτυο: 940€

PRIMO GEN24 4.6 (4.6kW):
- 0-100 kWp: 1,028€ | 100-500 kWp: 1,018€ | >500 kWp: 1,008€ | Δίκτυο: 998€

PRIMO GEN24 5.0 (5kW):
- 0-100 kWp: 1,063€ | 100-500 kWp: 1,052€ | >500 kWp: 1,042€ | Δίκτυο: 1,032€

PRIMO GEN24 6.0 (6kW):
- 0-100 kWp: 1,233€ | 100-500 kWp: 1,221€ | >500 kWp: 1,209€ | Δίκτυο: 1,197€

PRIMO GEN24 8.0 (8kW):
- 0-100 kWp: 1,448€ | 100-500 kWp: 1,433€ | >500 kWp: 1,419€ | Δίκτυο: 1,405€

Προμηθευτής: Big Solar AE
""", "inverter", "Fronius PRIMO GEN24 Μονοφασικοί Inverters")

upload_doc("""Fronius Τριφασικοί Inverters - Τιμοκατάλογος Big Solar 2025

SYMO Series (Three Phase):

SYMO 3.0-3-M (3kW):
- 0-100 kWp: 1,006€ | 100-500 kWp: 996€ | >500 kWp: 986€ | Δίκτυο: 976€

SYMO 3.7-3-M (3.7kW):
- 0-100 kWp: 1,100€ | 100-500 kWp: 1,089€ | >500 kWp: 1,078€ | Δίκτυο: 1,068€

SYMO GEN24 4.0 (4kW):
- 0-100 kWp: 1,232€ | 100-500 kWp: 1,220€ | >500 kWp: 1,207€ | Δίκτυο: 1,195€

SYMO 4.5-3-M (4.5kW):
- 0-100 kWp: 1,160€ | 100-500 kWp: 1,148€ | >500 kWp: 1,137€ | Δίκτυο: 1,125€

SYMO 5.0-3-M (5kW):
- 0-100 kWp: 1,178€ | 100-500 kWp: 1,166€ | >500 kWp: 1,155€ | Δίκτυο: 1,144€

SYMO 6.0-3-M (6kW):
- 0-100 kWp: 1,203€ | 100-500 kWp: 1,191€ | >500 kWp: 1,179€ | Δίκτυο: 1,167€

SYMO GEN24 6.0 (6kW):
- 0-100 kWp: 1,455€ | 100-500 kWp: 1,441€ | >500 kWp: 1,427€ | Δίκτυο: 1,412€

SYMO 7.0-3-M (7kW):
- 0-100 kWp: 1,485€ | 100-500 kWp: 1,471€ | >500 kWp: 1,456€ | Δίκτυο: 1,442€

SYMO 8.2-3-M (8.2kW):
- 0-100 kWp: 1,643€ | 100-500 kWp: 1,627€ | >500 kWp: 1,611€ | Δίκτυο: 1,595€

SYMO GEN24 8.0 (8kW):
- 0-100 kWp: 1,754€ | 100-500 kWp: 1,737€ | >500 kWp: 1,720€ | Δίκτυο: 1,703€

SYMO ADVANCED 10.0-3-M (10kW):
- 0-100 kWp: 1,698€ | 100-500 kWp: 1,681€ | >500 kWp: 1,665€ | Δίκτυο: 1,648€

SYMO GEN24 10.0 (10kW):
- 0-100 kWp: 1,860€ | 100-500 kWp: 1,842€ | >500 kWp: 1,824€ | Δίκτυο: 1,806€

SYMO ADVANCED 12.5-3-M (12.5kW):
- 0-100 kWp: 1,927€ | 100-500 kWp: 1,908€ | >500 kWp: 1,889€ | Δίκτυο: 1,870€

SYMO ADVANCED 15.0-3-M (15kW):
- 0-100 kWp: 1,940€ | 100-500 kWp: 1,921€ | >500 kWp: 1,902€ | Δίκτυο: 1,883€

SYMO ADVANCED 17.5-3-M (17.5kW):
- 0-100 kWp: 1,935€ | 100-500 kWp: 1,916€ | >500 kWp: 1,897€ | Δίκτυο: 1,878€

SYMO ADVANCED 20.0-3-M (20kW):
- 0-100 kWp: 2,025€ | 100-500 kWp: 2,005€ | >500 kWp: 1,985€ | Δίκτυο: 1,965€

ECO 25.0-3-S (25kW):
- 0-100 kWp: 2,212€ | 100-500 kWp: 2,190€ | >500 kWp: 2,169€ | Δίκτυο: 2,147€

ECO 27.0-3-S (27kW):
- 0-100 kWp: 2,272€ | 100-500 kWp: 2,250€ | >500 kWp: 2,227€ | Δίκτυο: 2,205€

VERTO 25.0 SPD I+II (25kW):
- 0-100 kWp: 2,362€ | 100-500 kWp: 2,339€ | >500 kWp: 2,316€ | Δίκτυο: 2,293€

VERTO 27.0 SPD I+II (27kW):
- 0-100 kWp: 2,423€ | 100-500 kWp: 2,399€ | >500 kWp: 2,375€ | Δίκτυο: 2,352€

VERTO 30.0 SPD I+II (30kW):
- 0-100 kWp: 2,572€ | 100-500 kWp: 2,547€ | >500 kWp: 2,521€ | Δίκτυο: 2,496€

VERTO 33.3 SPD I+II (33.3kW):
- 0-100 kWp: 2,762€ | 100-500 kWp: 2,734€ | >500 kWp: 2,707€ | Δίκτυο: 2,680€

TAURO ECO 50-3-P PROJECT: Upon request
TAURO ECO 100-3-P PROJECT: Upon request
ARGENO 125 MVP: Upon request

Προμηθευτής: Big Solar AE
""", "inverter", "Fronius SYMO Τριφασικοί Inverters")

upload_doc("""Fronius Υβριδικοί Inverters - Τιμοκατάλογος Big Solar 2025

ΜΟΝΟΦΑΣΙΚΟΙ ΥΒΡΙΔΙΚΟΙ (PRIMO GEN24 PLUS):

PRIMO GEN24 3.0 PLUS (3kW):
- 0-100 kWp: 1,272€ | 100-500 kWp: 1,260€ | >500 kWp: 1,247€ | Δίκτυο: 1,235€

PRIMO GEN24 3.6 PLUS (3.6kW):
- 0-100 kWp: 1,326€ | 100-500 kWp: 1,313€ | >500 kWp: 1,300€ | Δίκτυο: 1,287€

PRIMO GEN24 4.0 PLUS (4kW):
- 0-100 kWp: 1,363€ | 100-500 kWp: 1,350€ | >500 kWp: 1,337€ | Δίκτυο: 1,323€

PRIMO GEN24 4.6 PLUS (4.6kW):
- 0-100 kWp: 1,472€ | 100-500 kWp: 1,457€ | >500 kWp: 1,443€ | Δίκτυο: 1,429€

PRIMO GEN24 5.0 PLUS (5kW):
- 0-100 kWp: 1,540€ | 100-500 kWp: 1,525€ | >500 kWp: 1,510€ | Δίκτυο: 1,495€

PRIMO GEN24 6.0 PLUS (6kW):
- 0-100 kWp: 1,709€ | 100-500 kWp: 1,693€ | >500 kWp: 1,676€ | Δίκτυο: 1,659€

ΤΡΙΦΑΣΙΚΟΙ ΥΒΡΙΔΙΚΟΙ (SYMO GEN24 PLUS):

SYMO GEN24 3.0 PLUS (3kW):
- 0-100 kWp: 1,476€ | 100-500 kWp: 1,462€ | >500 kWp: 1,447€ | Δίκτυο: 1,433€

SYMO GEN24 4.0 PLUS (4kW):
- 0-100 kWp: 1,575€ | 100-500 kWp: 1,559€ | >500 kWp: 1,544€ | Δίκτυο: 1,529€

SYMO GEN24 5.0 PLUS (5kW):
- 0-100 kWp: 1,658€ | 100-500 kWp: 1,642€ | >500 kWp: 1,626€ | Δίκτυο: 1,610€

SYMO GEN24 6.0 PLUS (6kW):
- 0-100 kWp: 1,974€ | 100-500 kWp: 1,954€ | >500 kWp: 1,935€ | Δίκτυο: 1,916€

SYMO GEN24 8.0 PLUS (8kW):
- 0-100 kWp: 2,273€ | 100-500 kWp: 2,250€ | >500 kWp: 2,228€ | Δίκτυο: 2,206€

SYMO GEN24 10.0 PLUS (10kW):
- 0-100 kWp: 2,374€ | 100-500 kWp: 2,351€ | >500 kWp: 2,328€ | Δίκτυο: 2,305€

VERTO PLUS 15 SPD I+II (15kW):
- 0-100 kWp: 2,933€ | 100-500 kWp: 2,904€ | >500 kWp: 2,875€ | Δίκτυο: 2,846€

VERTO PLUS 17.5 SPD I+II (17.5kW):
- 0-100 kWp: 3,135€ | 100-500 kWp: 3,104€ | >500 kWp: 3,073€ | Δίκτυο: 3,043€

VERTO PLUS 20.0 SPD I+II (20kW):
- 0-100 kWp: 3,338€ | 100-500 kWp: 3,305€ | >500 kWp: 3,272€ | Δίκτυο: 3,240€

VERTO PLUS 25.0 SPD I+II (25kW):
- 0-100 kWp: 3,642€ | 100-500 kWp: 3,606€ | >500 kWp: 3,570€ | Δίκτυο: 3,534€

VERTO PLUS 30.0 SPD I+II (30kW):
- 0-100 kWp: 3,877€ | 100-500 kWp: 3,838€ | >500 kWp: 3,800€ | Δίκτυο: 3,763€

VERTO PLUS 33.3 SPD I+II (33.3kW):
- 0-100 kWp: 4,013€ | 100-500 kWp: 3,973€ | >500 kWp: 3,934€ | Δίκτυο: 3,895€

Προμηθευτής: Big Solar AE
""", "inverter", "Fronius Υβριδικοί Inverters PLUS Series")

upload_doc("""Fronius Μπαταρίες & Παρελκόμενα - Τιμοκατάλογος Big Solar 2025

ΣΥΣΤΗΜΑΤΑ ΑΠΟΘΗΚΕΥΣΗΣ:

RESERVA BATTERY MODULE 3.15 kWh:
- 0-100 kWp: 978€ | 100-500 kWp: 969€ | >500 kWp: 959€ | Δίκτυο: 950€

SBA FR RESERVA BMS:
- 0-100 kWp: 829€ | 100-500 kWp: 821€ | >500 kWp: 813€ | Δίκτυο: 805€

ΠΑΡΕΛΚΟΜΕΝΑ:

DC FR IG DATAMANAGER 2.0 WLAN FOR GALSYMPRIMO: 178€
DC FR IG DATAMANAGER BOX 2.0 WLAN: 280€
DC FR SMART METER TS 100A-1: 85€
DC FR SMART METER 63A-3: 170€
DC FR SMART METER TS 50KA-3: 170€

Προμηθευτής: Big Solar AE
""", "battery", "Fronius Μπαταρίες RESERVA & Παρελκόμενα")

# ============ BYD BATTERIES ============
upload_doc("""BYD Μπαταρίες - Τιμοκατάλογος Big Solar 2025

BYD Energy Storage - Battery Modules:

HVS module 2.56KWH:
- 0-100 kWp: 978.79€ | 100-500 kWp: 969.10€ | >500 kWp: 959.50€ | Δίκτυο: 950.00€

HVM module 2.75 KWH:
- 0-100 kWp: 978.79€ | 100-500 kWp: 969.10€ | >500 kWp: 959.50€ | Δίκτυο: 950.00€

BCU + BASE:
- 0-100 kWp: 481.15€ | 100-500 kWp: 476.39€ | >500 kWp: 471.67€ | Δίκτυο: 467.00€

Max Lite Single Battery Module 7.5kWh:
- 0-100 kWp: 1,653.63€ | 100-500 kWp: 1,637.26€ | >500 kWp: 1,621.05€ | Δίκτυο: 1,605.00€

Max Lite cabinet with BDU:
- 0-100 kWp: 6,645.44€ | 100-500 kWp: 6,579.65€ | >500 kWp: 6,514.50€ | Δίκτυο: 6,450.00€

Στις τιμές μπαταριών περιλαμβάνεται η εισφορά εναλλακτικής διαχείρισης.
Προμηθευτής: Big Solar AE
""", "battery", "BYD Μπαταρίες HVS HVM Max Lite")

# ============ SOLIS INVERTERS ============
upload_doc("""Solis Μονοφασικοί Inverters - Τιμοκατάλογος Big Solar 2025

SOLIS SINGLE PHASE INVERTERS:

S6-GR1P0.7K-M (0.7kW):
- 0-100 kWp: 244€ | 100-500 kWp: 241€ | >500 kWp: 239€ | Δίκτυο: 236.44€

S6-GR1P1K-M (1kW):
- 0-100 kWp: 245€ | 100-500 kWp: 243€ | >500 kWp: 240€ | Δίκτυο: 237.79€

S6-GR1P1.5K-M (1.5kW):
- 0-100 kWp: 266€ | 100-500 kWp: 263€ | >500 kWp: 261€ | Δίκτυο: 258.18€

S6-GR1P2K-M (2kW):
- 0-100 kWp: 308€ | 100-500 kWp: 305€ | >500 kWp: 302€ | Δίκτυο: 298.94€

S6-GR1P2.5K-M (2.5kW):
- 0-100 kWp: 350€ | 100-500 kWp: 347€ | >500 kWp: 343€ | Δίκτυο: 339.71€

S6-GR1P3K-M (3kW):
- 0-100 kWp: 385€ | 100-500 kWp: 381€ | >500 kWp: 377€ | Δίκτυο: 373.68€

S6-GR1P3.6K-M (3.6kW):
- 0-100 kWp: 420€ | 100-500 kWp: 416€ | >500 kWp: 412€ | Δίκτυο: 407.65€

S6-GR1P2.5K (2.5kW):
- 0-100 kWp: 448€ | 100-500 kWp: 444€ | >500 kWp: 439€ | Δίκτυο: 434.82€

S6-GR1P3K (3kW):
- 0-100 kWp: 462€ | 100-500 kWp: 457€ | >500 kWp: 453€ | Δίκτυο: 448.41€

S6-GR1P3.6K (3.6kW):
- 0-100 kWp: 511€ | 100-500 kWp: 506€ | >500 kWp: 501€ | Δίκτυο: 495.97€

S6-GR1P4K (4kW):
- 0-100 kWp: 532€ | 100-500 kWp: 527€ | >500 kWp: 522€ | Δίκτυο: 516.35€

S6-GR1P4.6K (4.6kW):
- 0-100 kWp: 560€ | 100-500 kWp: 554€ | >500 kWp: 549€ | Δίκτυο: 543.53€

S6-GR1P5K (5kW):
- 0-100 kWp: 574€ | 100-500 kWp: 568€ | >500 kWp: 563€ | Δίκτυο: 557.12€

S6-GR1P6K (6kW):
- 0-100 kWp: 602€ | 100-500 kWp: 596€ | >500 kWp: 590€ | Δίκτυο: 584.29€

Προμηθευτής: Big Solar AE
""", "inverter", "Solis Μονοφασικοί Inverters S6-GR1P")

upload_doc("""Solis Τριφασικοί Inverters - Τιμοκατάλογος Big Solar 2025

SOLIS THREE PHASE INVERTERS:

S5-GR3P3K (3kW):
- 0-100 kWp: 424€ | 100-500 kWp: 420€ | >500 kWp: 416€ | Δίκτυο: 411.72€

S5-GR3P4K (4kW):
- 0-100 kWp: 428€ | 100-500 kWp: 424€ | >500 kWp: 420€ | Δίκτυο: 415.80€

S5-GR3P5K (5kW):
- 0-100 kWp: 437€ | 100-500 kWp: 432€ | >500 kWp: 428€ | Δίκτυο: 423.95€

S5-GR3P6K (6kW):
- 0-100 kWp: 458€ | 100-500 kWp: 453€ | >500 kWp: 449€ | Δίκτυο: 444.34€

S5-GR3P8K (8kW):
- 0-100 kWp: 496€ | 100-500 kWp: 491€ | >500 kWp: 486€ | Δίκτυο: 481.02€

S5-GR3P9K (9kW):
- 0-100 kWp: 514€ | 100-500 kWp: 509€ | >500 kWp: 504€ | Δίκτυο: 499.06€

S5-GR3P10K (10kW):
- 0-100 kWp: 533€ | 100-500 kWp: 528€ | >500 kWp: 523€ | Δίκτυο: 517.71€

S5-GR3P12K (12kW):
- 0-100 kWp: 580€ | 100-500 kWp: 574€ | >500 kWp: 568€ | Δίκτυο: 562.55€

S5-GR3P15K (15kW):
- 0-100 kWp: 613€ | 100-500 kWp: 607€ | >500 kWp: 601€ | Δίκτυο: 595.16€

S5-GR3P17K (17kW):
- 0-100 kWp: 664€ | 100-500 kWp: 657€ | >500 kWp: 651€ | Δίκτυο: 644.08€

S5-GR3P20K (20kW):
- 0-100 kWp: 706€ | 100-500 kWp: 699€ | >500 kWp: 692€ | Δίκτυο: 684.85€

S5-GC25K (25kW):
- 0-100 kWp: 846€ | 100-500 kWp: 838€ | >500 kWp: 829€ | Δίκτυο: 821.22€

S5-GC30K (30kW):
- 0-100 kWp: 1,016€ | 100-500 kWp: 1,006€ | >500 kWp: 996€ | Δίκτυο: 985.76€

S5-GC33K (33kW):
- 0-100 kWp: 1,107€ | 100-500 kWp: 1,096€ | >500 kWp: 1,085€ | Δίκτυο: 1,074.71€

S5-GC36K (36kW):
- 0-100 kWp: 1,199€ | 100-500 kWp: 1,187€ | >500 kWp: 1,175€ | Δίκτυο: 1,163.65€

S5-GC40K (40kW):
- 0-100 kWp: 1,387€ | 100-500 kWp: 1,374€ | >500 kWp: 1,360€ | Δίκτυο: 1,346.47€

S5-GC50K (50kW):
- 0-100 kWp: 1,464€ | 100-500 kWp: 1,449€ | >500 kWp: 1,435€ | Δίκτυο: 1,420.59€

S5-GC60K (60kW):
- 0-100 kWp: 1,845€ | 100-500 kWp: 1,827€ | >500 kWp: 1,809€ | Δίκτυο: 1,791.18€

Solis-80K-5G-PRO (80kW):
- 0-100 kWp: 2,164€ | 100-500 kWp: 2,142€ | >500 kWp: 2,121€ | Δίκτυο: 2,100.00€

Solis-100K-5G-PRO (100kW):
- 0-100 kWp: 2,533€ | 100-500 kWp: 2,508€ | >500 kWp: 2,483€ | Δίκτυο: 2,458.24€

Solis-110K-5G-PRO (110kW):
- 0-100 kWp: 2,609€ | 100-500 kWp: 2,583€ | >500 kWp: 2,558€ | Δίκτυο: 2,532.35€

S6-GC125K: Upon request

Solis-215K-EHV-5G-PLUS (215kW):
- 0-100 kWp: 6,364€ | 100-500 kWp: 6,301€ | >500 kWp: 6,238€ | Δίκτυο: 6,176.47€

Solis-255K-EHV-5G-PLUS (255kW):
- 0-100 kWp: 6,364€ | 100-500 kWp: 6,301€ | >500 kWp: 6,238€ | Δίκτυο: 6,176.47€

S6-GU350K-EHV-M12 (350kW):
- 0-100 kWp: 8,782€ | 100-500 kWp: 8,695€ | >500 kWp: 8,609€ | Δίκτυο: 8,523.53€

S6-GU350K-EHV-M16 (350kW):
- 0-100 kWp: 8,909€ | 100-500 kWp: 8,821€ | >500 kWp: 8,734€ | Δίκτυο: 8,647.06€

Προμηθευτής: Big Solar AE
""", "inverter", "Solis Τριφασικοί Inverters S5-GR3P S5-GC")

upload_doc("""Solis Υβριδικοί Inverters Low Voltage - Τιμοκατάλογος Big Solar 2025

SOLIS THREE PHASE HYBRID - LOW VOLTAGE:

S6-EH3P8K02-NV-YD-L (8kW):
- 0-100 kWp: 1,537€ | 100-500 kWp: 1,522€ | >500 kWp: 1,507€ | Δίκτυο: 1,491.94€

S6-EH3P10K02-NV-YD-L (10kW):
- 0-100 kWp: 1,599€ | 100-500 kWp: 1,583€ | >500 kWp: 1,567€ | Δίκτυο: 1,551.62€

S6-EH3P12K02-NV-YD-L (12kW):
- 0-100 kWp: 1,660€ | 100-500 kWp: 1,644€ | >500 kWp: 1,627€ | Δίκτυο: 1,611.29€

S6-EH3P15K02-NV-YD-L (15kW):
- 0-100 kWp: 1,906€ | 100-500 kWp: 1,887€ | >500 kWp: 1,869€ | Δίκτυο: 1,850.00€

Προμηθευτής: Big Solar AE
""", "inverter", "Solis Υβριδικοί Low Voltage")

upload_doc("""Solis Υβριδικοί Inverters High Voltage - Τιμοκατάλογος Big Solar 2025

SOLIS THREE PHASE HYBRID - HIGH VOLTAGE:

S6-EH3P5K-H-EU (5kW):
- 0-100 kWp: 984€ | 100-500 kWp: 974€ | >500 kWp: 964€ | Δίκτυο: 954.88€

S6-EH3P6K-H-EU (6kW):
- 0-100 kWp: 995€ | 100-500 kWp: 985€ | >500 kWp: 976€ | Δίκτυο: 966.00€

S6-EH3P8K-H-EU (8kW):
- 0-100 kWp: 1,036€ | 100-500 kWp: 1,026€ | >500 kWp: 1,016€ | Δίκτυο: 1,005.53€

S6-EH3P10K-H-EU (10kW):
- 0-100 kWp: 1,070€ | 100-500 kWp: 1,060€ | >500 kWp: 1,049€ | Δίκτυο: 1,038.88€

S6-EH3P12K-H (12kW):
- 0-100 kWp: 1,457€ | 100-500 kWp: 1,443€ | >500 kWp: 1,429€ | Δίκτυο: 1,414.41€

S6-EH3P15K-H (15kW):
- 0-100 kWp: 1,540€ | 100-500 kWp: 1,525€ | >500 kWp: 1,510€ | Δίκτυο: 1,494.71€

S6-EH3P20K-H (20kW):
- 0-100 kWp: 1,915€ | 100-500 kWp: 1,896€ | >500 kWp: 1,878€ | Δίκτυο: 1,859.12€

S6-EH3P30K-H (30kW):
- 0-100 kWp: 3,462€ | 100-500 kWp: 3,428€ | >500 kWp: 3,394€ | Δίκτυο: 3,360.00€

S6-EH3P40K-H (40kW):
- 0-100 kWp: 4,009€ | 100-500 kWp: 3,969€ | >500 kWp: 3,930€ | Δίκτυο: 3,891.18€

S6-EH3P50K-H (50kW):
- 0-100 kWp: 4,455€ | 100-500 kWp: 4,410€ | >500 kWp: 4,367€ | Δίκτυο: 4,323.53€

ΠΑΡΕΛΚΟΜΕΝΑ MONITORING:

S2-WL-ST:
- 0-100 kWp: 44.55€ | 100-500 kWp: 44.10€ | >500 kWp: 43.67€ | Δίκτυο: 43.24€

S3-GPRS-ST:
- 0-100 kWp: 12.73€ | 100-500 kWp: 12.60€ | >500 kWp: 12.48€ | Δίκτυο: 12.35€

S3-WIFI-ST:
- 0-100 kWp: 12.73€ | 100-500 kWp: 12.60€ | >500 kWp: 12.48€ | Δίκτυο: 12.35€

ΠΑΡΕΛΚΟΜΕΝΑ ΜΕΤΡΗΤΕΣ:

Meter-1P-Acrel (Built-In CT):
- 0-100 kWp: 50.91€ | 100-500 kWp: 50.40€ | >500 kWp: 49.91€ | Δίκτυο: 49.41€

Meter-1P-Acrel (External CT):
- 0-100 kWp: 76.36€ | 100-500 kWp: 75.61€ | >500 kWp: 74.86€ | Δίκτυο: 74.12€

Meter-3P-Acrel (Built-in CT):
- 0-100 kWp: 76.36€ | 100-500 kWp: 75.61€ | >500 kWp: 74.86€ | Δίκτυο: 74.12€

Meter-3P-Acrel (External CT):
- 0-100 kWp: 114.55€ | 100-500 kWp: 113.41€ | >500 kWp: 112.29€ | Δίκτυο: 111.18€

Meter-3P-RHI-Eastron:
- 0-100 kWp: 101.82€ | 100-500 kWp: 100.81€ | >500 kWp: 99.81€ | Δίκτυο: 98.82€

ΠΑΡΕΛΚΟΜΕΝΑ EPM:

Solis-EPM1-5G:
- 0-100 kWp: 254.54€ | 100-500 kWp: 252.02€ | >500 kWp: 249.53€ | Δίκτυο: 247.06€

Solis-EPM3-5G:
- 0-100 kWp: 254.54€ | 100-500 kWp: 252.02€ | >500 kWp: 249.53€ | Δίκτυο: 247.06€

Solis-EPM3-5G-PRO:
- 0-100 kWp: 356.36€ | 100-500 kWp: 352.83€ | >500 kWp: 349.34€ | Δίκτυο: 345.88€

Προμηθευτής: Big Solar AE
""", "inverter", "Solis Υβριδικοί High Voltage & Παρελκόμενα")

# ============ SOLAX INVERTERS ============
upload_doc("""SolaX Μονοφασικοί Υβριδικοί Inverters - Τιμοκατάλογος Big Solar 2025

SOLAX X1-HYBRID Series (Generation 4):

X1-HYBRID-3.0D (3kW):
- 0-100 kWp: 784€ | 100-500 kWp: 777€ | >500 kWp: 769€ | Δίκτυο: 761.40€

X1-HYBRID-3.7D (3.7kW):
- 0-100 kWp: 832€ | 100-500 kWp: 824€ | >500 kWp: 816€ | Δίκτυο: 807.84€

X1-HYBRID-5.0D (5kW) - BEST SELLER:
- 0-100 kWp: 870€ | 100-500 kWp: 862€ | >500 kWp: 853€ | Δίκτυο: 844.80€

X1-HYBRID-6.0D (6kW):
- 0-100 kWp: 903€ | 100-500 kWp: 894€ | >500 kWp: 885€ | Δίκτυο: 876.00€

X1-HYBRID-7.5D (7.5kW):
- 0-100 kWp: 966€ | 100-500 kWp: 956€ | >500 kWp: 947€ | Δίκτυο: 937.20€

Generation 3:

X1-Hybrid-3.0-D-E (3kW):
- 0-100 kWp: 668€ | 100-500 kWp: 661€ | >500 kWp: 654€ | Δίκτυο: 648.00€

X1-Hybrid-5.0-D-E (5kW):
- 0-100 kWp: 739€ | 100-500 kWp: 732€ | >500 kWp: 725€ | Δίκτυο: 717.60€

X1-VAST Series (με DC Switch Pocket WiFi+LAN CT Screen SPD II):

X1-VAST-6K (6kW):
- 0-100 kWp: 1,209€ | 100-500 kWp: 1,197€ | >500 kWp: 1,185€ | Δίκτυο: 1,173.60€

X1-VAST-8K (8kW):
- 0-100 kWp: 1,261€ | 100-500 kWp: 1,249€ | >500 kWp: 1,236€ | Δίκτυο: 1,224.00€

X1-VAST-10K (10kW):
- 0-100 kWp: 1,311€ | 100-500 kWp: 1,298€ | >500 kWp: 1,285€ | Δίκτυο: 1,272.00€

Προμηθευτής: Big Solar AE
""", "inverter", "SolaX X1-HYBRID Μονοφασικοί Υβριδικοί")

upload_doc("""SolaX Τριφασικοί Υβριδικοί Inverters - Τιμοκατάλογος Big Solar 2025

SOLAX X3-HYBRID Series (Generation 4):

X3-HYBRID-5.0-D (5kW):
- 0-100 kWp: 1,163€ | 100-500 kWp: 1,152€ | >500 kWp: 1,140€ | Δίκτυο: 1,129.20€

X3-HYBRID-6.0-D (6kW):
- 0-100 kWp: 1,222€ | 100-500 kWp: 1,209€ | >500 kWp: 1,197€ | Δίκτυο: 1,185.60€

X3-HYBRID-8.0-D (8kW):
- 0-100 kWp: 1,283€ | 100-500 kWp: 1,271€ | >500 kWp: 1,258€ | Δίκτυο: 1,245.60€

X3-HYBRID-10.0-D (10kW):
- 0-100 kWp: 1,406€ | 100-500 kWp: 1,392€ | >500 kWp: 1,378€ | Δίκτυο: 1,364.40€

X3-HYBRID-12.0-D (12kW):
- 0-100 kWp: 1,507€ | 100-500 kWp: 1,492€ | >500 kWp: 1,477€ | Δίκτυο: 1,462.80€

X3-HYBRID-15.0-D (15kW):
- 0-100 kWp: 1,618€ | 100-500 kWp: 1,602€ | >500 kWp: 1,587€ | Δίκτυο: 1,570.80€

X3-ULTRA Series (με DC Switch Pocket WiFi+Lan CT SPD II):

X3-ULT-15K (15kW):
- 0-100 kWp: 2,302€ | 100-500 kWp: 2,279€ | >500 kWp: 2,257€ | Δίκτυο: 2,234.40€

X3-ULT-20K (20kW):
- 0-100 kWp: 2,417€ | 100-500 kWp: 2,393€ | >500 kWp: 2,369€ | Δίκτυο: 2,346.00€

X3-ULT-25K (25kW):
- 0-100 kWp: 2,520€ | 100-500 kWp: 2,495€ | >500 kWp: 2,470€ | Δίκτυο: 2,445.60€

X3-ULT-30K (30kW):
- 0-100 kWp: 2,643€ | 100-500 kWp: 2,617€ | >500 kWp: 2,591€ | Δίκτυο: 2,565.60€

Προμηθευτής: Big Solar AE
""", "inverter", "SolaX X3-HYBRID & X3-ULTRA Τριφασικοί")

upload_doc("""SolaX Μονοφασικοί Micro/Mini/Boost Inverters - Τιμοκατάλογος Big Solar 2025

X1-MINI Series (Generation 4 με LCD):

X1-MINI-0.7K-G4 (700W):
- 0-100 kWp: 232€ | 100-500 kWp: 230€ | >500 kWp: 228€ | Δίκτυο: 225.60€

X1-MINI-1.1K-G4 (1.1kW):
- 0-100 kWp: 240€ | 100-500 kWp: 237€ | >500 kWp: 235€ | Δίκτυο: 232.80€

X1-MINI-1.5K-G4 (1.5kW):
- 0-100 kWp: 251€ | 100-500 kWp: 248€ | >500 kWp: 246€ | Δίκτυο: 243.60€

X1-MINI-2.0K-G4 (2kW):
- 0-100 kWp: 255€ | 100-500 kWp: 252€ | >500 kWp: 250€ | Δίκτυο: 247.20€

X1-MINI-2.5K-G4 (2.5kW):
- 0-100 kWp: 321€ | 100-500 kWp: 318€ | >500 kWp: 315€ | Δίκτυο: 312.00€

X1-MINI-3.0K-G4 (3kW):
- 0-100 kWp: 352€ | 100-500 kWp: 349€ | >500 kWp: 345€ | Δίκτυο: 342.00€

X1-MINI-3.3K-G4 (3.3kW):
- 0-100 kWp: 371€ | 100-500 kWp: 367€ | >500 kWp: 364€ | Δίκτυο: 360.00€

X1-BOOST Series (Generation 4 με LCD screen):

X1-BOOST-2.5K-G4 (2.5kW):
- 0-100 kWp: 396€ | 100-500 kWp: 392€ | >500 kWp: 388€ | Δίκτυο: 384.00€

X1-BOOST-3.0K-G4 (3kW):
- 0-100 kWp: 412€ | 100-500 kWp: 408€ | >500 kWp: 404€ | Δίκτυο: 399.60€

X1-BOOST-3.3K-G4 (3.3kW):
- 0-100 kWp: 430€ | 100-500 kWp: 426€ | >500 kWp: 422€ | Δίκτυο: 417.60€

X1-BOOST-3.6K-G4 (3.6kW):
- 0-100 kWp: 454€ | 100-500 kWp: 449€ | >500 kWp: 445€ | Δίκτυο: 440.40€

X1-BOOST-4.2K-G4 (4.2kW):
- 0-100 kWp: 496€ | 100-500 kWp: 491€ | >500 kWp: 486€ | Δίκτυο: 481.20€

X1-BOOST-5K-G4 (5kW):
- 0-100 kWp: 519€ | 100-500 kWp: 514€ | >500 kWp: 509€ | Δίκτυο: 504.00€

X1-BOOST-6K-G4 (6kW):
- 0-100 kWp: 538€ | 100-500 kWp: 532€ | >500 kWp: 527€ | Δίκτυο: 522.00€

Προμηθευτής: Big Solar AE
""", "inverter", "SolaX X1-MINI & X1-BOOST Μικροί Inverters")

upload_doc("""SolaX Τριφασικοί MIC/PRO/MEGA/FORTH Inverters - Τιμοκατάλογος Big Solar 2025

X3-MIC G2 Series (Three Phases Dual MPPT):

X3-MIC-4.0K-G2 (4kW):
- 0-100 kWp: 638€ | 100-500 kWp: 632€ | >500 kWp: 625€ | Δίκτυο: 619.20€

X3-MIC-5.0K-G2 (5kW):
- 0-100 kWp: 648€ | 100-500 kWp: 641€ | >500 kWp: 635€ | Δίκτυο: 628.80€

X3-MIC-6.0K-G2 (6kW):
- 0-100 kWp: 682€ | 100-500 kWp: 676€ | >500 kWp: 669€ | Δίκτυο: 662.40€

X3-MIC-8.0K-G2 (8kW):
- 0-100 kWp: 732€ | 100-500 kWp: 725€ | >500 kWp: 718€ | Δίκτυο: 710.40€

X3-MIC-10.0K-G2 (10kW):
- 0-100 kWp: 780€ | 100-500 kWp: 772€ | >500 kWp: 765€ | Δίκτυο: 757.20€

X3-MIC-12.0K-G2 (12kW):
- 0-100 kWp: 820€ | 100-500 kWp: 812€ | >500 kWp: 804€ | Δίκτυο: 795.60€

X3-MIC-15.0K-G2 (15kW):
- 0-100 kWp: 861€ | 100-500 kWp: 852€ | >500 kWp: 844€ | Δίκτυο: 835.20€

X3-PRO G2 Series (με 4 input strings):

X3-PRO-8K-G2 (8kW):
- 0-100 kWp: 936€ | 100-500 kWp: 927€ | >500 kWp: 917€ | Δίκτυο: 908.40€

X3-PRO-10K-G2 (10kW):
- 0-100 kWp: 968€ | 100-500 kWp: 958€ | >500 kWp: 949€ | Δίκτυο: 939.60€

X3-PRO-12K-G2 (12kW):
- 0-100 kWp: 977€ | 100-500 kWp: 967€ | >500 kWp: 957€ | Δίκτυο: 948.00€

X3-PRO-15K-G2 (15kW):
- 0-100 kWp: 1,022€ | 100-500 kWp: 1,012€ | >500 kWp: 1,002€ | Δίκτυο: 992.40€

X3-PRO-17K-G2 (17kW):
- 0-100 kWp: 1,055€ | 100-500 kWp: 1,044€ | >500 kWp: 1,034€ | Δίκτυο: 1,023.60€

X3-PRO-20K-G2 (20kW):
- 0-100 kWp: 1,092€ | 100-500 kWp: 1,081€ | >500 kWp: 1,070€ | Δίκτυο: 1,059.60€

X3-PRO-25K-G2(3D) (25kW με 6 input strings):
- 0-100 kWp: 1,136€ | 100-500 kWp: 1,125€ | >500 kWp: 1,114€ | Δίκτυο: 1,102.80€

X3-PRO-30K-G2(3D) (30kW με 6 input strings):
- 0-100 kWp: 1,233€ | 100-500 kWp: 1,220€ | >500 kWp: 1,208€ | Δίκτυο: 1,196.40€

X1 MEGA & X3 FORTH Series (Industrial & Utility):

X3-MGA-40K (40kW με LCD AFCI):
- 0-100 kWp: 1,669€ | 100-500 kWp: 1,653€ | >500 kWp: 1,636€ | Δίκτυο: 1,620.00€

X3-MGA-50K (50kW με LCD AFCI):
- 0-100 kWp: 1,731€ | 100-500 kWp: 1,714€ | >500 kWp: 1,697€ | Δίκτυο: 1,680.00€

X3-MGA-60K (60kW με LCD AFCI):
- 0-100 kWp: 1,855€ | 100-500 kWp: 1,836€ | >500 kWp: 1,818€ | Δίκτυο: 1,800.00€

X3-FTH-80K (80kW με LCD AFCI):
- 0-100 kWp: 2,701€ | 100-500 kWp: 2,675€ | >500 kWp: 2,648€ | Δίκτυο: 2,622.00€

X3-FTH-100K (100kW με LCD AFCI):
- 0-100 kWp: 2,819€ | 100-500 kWp: 2,791€ | >500 kWp: 2,763€ | Δίκτυο: 2,736.00€

X3-FTH-110K (110kW με LCD AFCI):
- 0-100 kWp: 2,878€ | 100-500 kWp: 2,850€ | >500 kWp: 2,822€ | Δίκτυο: 2,793.60€

X3-FTH-120K (120kW με LCD AFCI):
- 0-100 kWp: 2,996€ | 100-500 kWp: 2,966€ | >500 kWp: 2,937€ | Δίκτυο: 2,907.60€

X3-FTH-125K (125kW με LCD AFCI):
- 0-100 kWp: 3,054€ | 100-500 kWp: 3,024€ | >500 kWp: 2,994€ | Δίκτυο: 2,964.00€

X3-GRAND Utility Series (με DC switch APS SPD2):

X3-GRD-300K-HV (300kW): Upon request
X3-GRD-320K-HV (320kW): Upon request
X3-GRD-333K-HV (333kW): Upon request
X3-GRD-350K-HV (350kW): Upon request

Προμηθευτής: Big Solar AE
""", "inverter", "SolaX X3-MIC X3-PRO X3-MGA X3-FTH Commercial")

# ============ SOLAX BATTERIES ============
upload_doc("""SolaX Μπαταρίες Triple Power & T58 - Τιμοκατάλογος Big Solar 2025

Στις τιμές μπαταριών ΔΕΝ περιλαμβάνεται η εισφορά εναλλακτικής διαχείρισης.

TRIPLE POWER SERIES:

T-BAT H5.8 V2.1 (5.8kWh High Voltage με BMS):
- 0-100 kWp: 1,607€ | 100-500 kWp: 1,591€ | >500 kWp: 1,576€ | Δίκτυο: 1,560.00€

HV11550 V2.1 (5.8kWh High Voltage χωρίς BMS):
- 0-100 kWp: 1,422€ | 100-500 kWp: 1,408€ | >500 kWp: 1,394€ | Δίκτυο: 1,380.00€

T-BAT-SYS-HV-S2.5 (2.5kWh Stackable High Voltage):
- 0-100 kWp: 717€ | 100-500 kWp: 710€ | >500 kWp: 703€ | Δίκτυο: 696.00€

T-BAT-SYS-HV-S3.6 (3.6kWh Stackable High Voltage):
- 0-100 kWp: 893€ | 100-500 kWp: 884€ | >500 kWp: 875€ | Δίκτυο: 866.40€

TP-HS25 (Series box for parallel use with base):
- 0-100 kWp: 321€ | 100-500 kWp: 318€ | >500 kWp: 315€ | Δίκτυο: 312.00€

T-BMS-MCS0800 (BMS for HS25/HS36 battery):
- 0-100 kWp: 494€ | 100-500 kWp: 490€ | >500 kWp: 485€ | Δίκτυο: 480.00€

T58 SERIES:

TBMS-S51-8 (BMS for 5.1kWH stackable LFP με battery bottom):
- 0-100 kWp: 680€ | 100-500 kWp: 673€ | >500 kWp: 667€ | Δίκτυο: 660.00€

TSYS-HS51 (5.1kWh 100Ah module):
- 0-100 kWp: 1,174€ | 100-500 kWp: 1,163€ | >500 kWp: 1,151€ | Δίκτυο: 1,140.00€

Series box(TB-HS51) (connection box for 2 rows):
- 0-100 kWp: 408€ | 100-500 kWp: 404€ | >500 kWp: 400€ | Δίκτυο: 396.00€

TCBox-70:
- 0-100 kWp: 198€ | 100-500 kWp: 196€ | >500 kWp: 194€ | Δίκτυο: 192.00€

TB-HR140 (14kWh rack type LFP Battery IP20):
- 0-100 kWp: 2,287€ | 100-500 kWp: 2,264€ | >500 kWp: 2,242€ | Δίκτυο: 2,220.00€

TBMS-R15 (BMS for 14kWH Rack Battery):
- 0-100 kWp: 1,236€ | 100-500 kWp: 1,224€ | >500 kWp: 1,212€ | Δίκτυο: 1,200.00€

HR140 Battery Rack (για 1BMS + up to 7/8 batteries):
- 0-100 kWp: 804€ | 100-500 kWp: 796€ | >500 kWp: 788€ | Δίκτυο: 780.00€

EMS 1000 PRO BOX-16:
- 0-100 kWp: 1,360€ | 100-500 kWp: 1,346€ | >500 kWp: 1,333€ | Δίκτυο: 1,320.00€

Προμηθευτής: Big Solar AE
""", "battery", "SolaX Μπαταρίες Triple Power T58 Series")

upload_doc("""SolaX Παρελκόμενα Μπαταριών - Τιμοκατάλογος Big Solar 2025

ΠΑΡΕΛΚΟΜΕΝΑ:

T-BAT-Charger (no-logo Europe standard):
- 0-100 kWp: 940€ | 100-500 kWp: 930€ | >500 kWp: 921€ | Δίκτυο: 912.00€

X1-EPS Box (Single phase EPS box for hybrid):
- 0-100 kWp: 198€ | 100-500 kWp: 196€ | >500 kWp: 194€ | Δίκτυο: 192.00€

X3-EPS Box (Three phase EPS box for hybrid):
- 0-100 kWp: 321€ | 100-500 kWp: 318€ | >500 kWp: 315€ | Δίκτυο: 312.00€

Adaptor box G2 (for Heatpump integration):
- 0-100 kWp: 56€ | 100-500 kWp: 55€ | >500 kWp: 55€ | Δίκτυο: 54.00€

Adapter Box G3 (for Heatpump integration):
- 0-100 kWp: 74€ | 100-500 kWp: 73€ | >500 kWp: 73€ | Δίκτυο: 72.00€

ΚΑΛΩΔΙΑ T58:

2m comm line for T58: 6€
2m power line A for T58: 9€ (Δίκτυο: 8.40€)
2m power line B for T58: 9€ (Δίκτυο: 8.40€)
5m comm line for T58: 16€ (Δίκτυο: 15.60€)
5m power line A for T58: 20€ (Δίκτυο: 19.20€)
5m power line B for T58: 20€ (Δίκτυο: 19.20€)

DC PLUGS:

DEVALAN DC-Plug male (1100VDC 40A): 2€ (Δίκτυο: 2.40€)
PHOENIX DC-Plug (40A/1100VDC Male): 2€ (Δίκτυο: 2.40€)
DC-Plug male+female for on-grid με PV Panel: 5€ (Δίκτυο: 4.80€)
AC-Plug for Mini, Boost: 12€

METERS & MONITORING:

M1-40 (Single phase meter 1P2W 100A/40mA CT):
- 0-100 kWp: 62€ | 100-500 kWp: 61€ | >500 kWp: 61€ | Δίκτυο: 60.00€

M3-40 (Three phase meter 3P4W/3P3W 100A/40mA CT):
- 0-100 kWp: 93€ | 100-500 kWp: 92€ | >500 kWp: 91€ | Δίκτυο: 90.00€

M3-40-Dual (Three phase dual current collection 2 sets 100A/40mA CT):
- 0-100 kWp: 117€ | 100-500 kWp: 116€ | >500 kWp: 115€ | Δίκτυο: 114.00€

DDSU666 (Chint Single Phase meter):
- 0-100 kWp: 62€ | 100-500 kWp: 61€ | >500 kWp: 61€ | Δίκτυο: 60.00€

DDSU666-D-CT (Chint Single Phase με CT):
- 0-100 kWp: 74€ | 100-500 kWp: 73€ | >500 kWp: 73€ | Δίκτυο: 72.00€

DTSU666-D (Chint Three Phase meter):
- 0-100 kWp: 87€ | 100-500 kWp: 86€ | >500 kWp: 85€ | Δίκτυο: 84.00€

DTSU666-D-CT (Chint Three Phase με CT):
- 0-100 kWp: 124€ | 100-500 kWp: 122€ | >500 kWp: 121€ | Δίκτυο: 120.00€

Wi-BR (for single/three-phase meters 85~277Vac):
- 0-100 kWp: 87€ | 100-500 kWp: 86€ | >500 kWp: 85€ | Δίκτυο: 84.00€

Chint 600A CT (LCTA97C4-600A/5A):
- 0-100 kWp: 27€ | Δίκτυο: 26.40€

Chint 1500A CT:
- 0-100 kWp: 56€ | 100-500 kWp: 55€ | >500 kWp: 55€ | Δίκτυο: 54.00€

CT for MINI: 9€ (Δίκτυο: 8.40€)

X PID BOX (anti-PID 1100V):
- 0-100 kWp: 185€ | 100-500 kWp: 184€ | >500 kWp: 182€ | Δίκτυο: 180.00€

Anti-combiner box PVR-24S (12 MPPT output):
- 0-100 kWp: 791€ | 100-500 kWp: 783€ | >500 kWp: 776€ | Δίκτυο: 768.00€

Datahub1000 (monitoring for multi inverters):
- 0-100 kWp: 341€ | 100-500 kWp: 338€ | >500 kWp: 335€ | Δίκτυο: 331.20€

WIFI DONGLES:

Pocket Wifi 3.0: 12€
Pocket Wifi V3.0 - P(10s) (S3 antenna 10sec refresh): 22€ (Δίκτυο: 21.60€)
Pocket Lan 3.0: 12€
Pocket WiFi+Lan: 35€ (Δίκτυο: 33.60€)
Pocket WiFi+Lan V2.0: 35€ (Δίκτυο: 33.60€)
Pocket 4G V3: 31€ (Δίκτυο: 30.00€)
Pocket WiFi + 4GM: 35€ (Δίκτυο: 33.60€)

Προμηθευτής: Big Solar AE
""", "accessories", "SolaX Παρελκόμενα Meters WiFi Cables")

# ============ HEXING METERS ============
upload_doc("""Μετρητές Ενέργειας HEXING - Τιμοκατάλογος Big Solar 2025

HEXING Energy Meters:

HXE310 τριφασικός μετρητής ενέργειας: 220€

HXE110 μονοφασικός μετρητής ενέργειας: 170€

Πλαστικό κιβώτιο τριφασικού μετρητή: 40€

Πλαστικό κιβώτιο μονοφασικού μετρητή: 32€

Προμηθευτής: Big Solar AE
""", "accessories", "HEXING Μετρητές Ενέργειας")

# ============ BESS SYSTEMS ============
upload_doc("""Battery Energy Storage Systems (BESS) - Big Solar 2025

HUAWEI LUNA:

SB HU LUNA2000-107-1S11:
- Li-Ion Energy Storage System
- Hybrid Cooling
- Rated Capacity: 107 kWh
- Price: Upon Request

SB HU LUNA2000-215-2S10:
- Li-Ion Energy Storage System
- Hybrid Cooling
- Rated Capacity: 215 kWh
- Price: Upon Request

SUNGROW PowerStack:

SB SUNG ST225kWh-110kW-2h:
- Liquid Cooled C&I ESS 225kWh LFP
- IP55 | C5 Anti-corrosion
- Price: Upon Request

SBA SUNG EMS300CP:
- Energy Management System for C&I
- Power Plant (Mandatory)
- IP66 Protection
- Price: Upon Request

GOODWE:

GW112.6-BAT-AC-G10:
- BAT Series Air Cooling
- LFP IP55 60/112.6kWh
- Price: Upon Request

GW125/261-ESA-LCN-G10:
- ESA Series Liquid Cooling
- LFP IP54 125kW/261kWh
- Compatible: GW40K-ET-10 & GW50K-ET-10
- Price: Upon Request

GW40K-ET-10 (40KW 3ph Hyb 3 MPPT): Upon Request
GW50K-ET-10 (50kW 3ph Hyb 4 MPPT): Upon Request

DYNESS:

DH100F-S00L01C100 All-in-one:
- PV+ESS no MPPT for initial setting
- System capacity: 100kWh
- Price: Upon Request

DH100F-S02L01C100:
- PV+ESS 2 MPPT (35kW*2)
- System capacity: 100kWh
- Price: Upon Request

SOLAX:

TRENE-P125B261L:
- 125kW PCS (Power Conversion System)
- 261kWh battery cabinet
- Liquid Cooling Cabinet
- Price: Upon Request

AELIO-B100:
- 100kWh battery cabinet
- με EMS No DC Switch
- No Screen No Dongle No Meter/CT
- No AFCI Air Cooled
- Price: Upon Request

WHES (Weiheng Energy Storage):

WH-PowerCore-50KW-100 kWh:
- 4 MPPTs & 200% PV Oversizing
- 280 Ah with 8000 Cycles
- Price: Upon Request

WH-PowerCore-100 kW-233KWh:
- All-In-One CATL Battery Modules
- Liquid Cooling
- Price: Upon Request

WH-PowerCore-250KW-500 kWh:
- Modular AC/DC Design
- CATL 306 Ah Battery Pack Liquid Cooling
- Price: Upon Request

Προμηθευτής: Big Solar AE
Για τιμές BESS επικοινωνήστε: 210 5509090
""", "battery", "BESS Συστήματα Αποθήκευσης Μεγάλης Κλίμακας")

print("\n" + "="*50)
print("UPLOAD COMPLETE!")
print("="*50)
stats = index.describe_index_stats()
print(f"Total documents in Pinecone: {stats.total_vector_count}")
