"""
Pinecone Server v3 με AI Assistant + PDF Generator + Email Templates
"""
import asyncio
import websockets
import json
import base64
import os
import sys
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pinecone import Pinecone
import hashlib
from datetime import datetime, timedelta
import anthropic

# PDF extraction & creation
import fitz  # PyMuPDF

# Excel extraction
import pandas as pd

# Google APIs
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# API Keys from environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "enercon")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")

if not PINECONE_API_KEY:
    print("❌ PINECONE_API_KEY not set! Check .env file")
    sys.exit(1)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Claude client
claude_client = None

def init_claude(api_key):
    global claude_client, CLAUDE_API_KEY
    CLAUDE_API_KEY = api_key
    if api_key:
        claude_client = anthropic.Anthropic(api_key=api_key)
        return True
    return False

# Google API setup
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/contacts.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]
gmail_service = None
calendar_service = None
contacts_service = None

def get_google_services():
    global gmail_service, calendar_service, contacts_service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                return None, None, None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    gmail_service = build('gmail', 'v1', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)
    contacts_service = build('people', 'v1', credentials=creds)
    return gmail_service, calendar_service, contacts_service

def get_gmail_service():
    global gmail_service
    if not gmail_service:
        get_google_services()
    return gmail_service

def get_calendar_service():
    global calendar_service
    if not calendar_service:
        get_google_services()
    return calendar_service

def get_contacts_service():
    global contacts_service
    if not contacts_service:
        get_google_services()
    return contacts_service

# ============ AI ASSISTANT ============

def search_rag(query, top_k=5):
    """Search RAG for context"""
    result = pc.inference.embed(model="multilingual-e5-large", inputs=[query], parameters={"input_type": "query"})
    results = index.query(vector=result.data[0].values, top_k=top_k, include_metadata=True)
    return [{"title": m.metadata.get("title", ""), "text": m.metadata.get("text", "")[:1000], "category": m.metadata.get("category", "")} for m in results.matches]

def ask_claude(user_message, context="", system_prompt=""):
    """Ask Claude with RAG context"""
    global claude_client
    if not claude_client:
        return "❌ Claude API δεν έχει ρυθμιστεί. Πήγαινε στις Ρυθμίσεις AI."
    
    # Default system prompt for Enercon assistant
    if not system_prompt:
        system_prompt = """Είσαι ο AI βοηθός του Enercon Knowledge Base, μια εφαρμογή για διαχείριση εγγράφων φωτοβολταϊκών συστημάτων.

Μπορείς να βοηθήσεις με:
- Αναζήτηση προϊόντων (panels, inverters, batteries)
- Δημιουργία προσφορών
- Υπολογισμούς ενέργειας
- Συμβουλές εγκατάστασης

Απάντα πάντα στα Ελληνικά. Να είσαι φιλικός και επαγγελματικός.
Όταν έχεις context από το RAG, χρησιμοποίησέ το για ακριβείς τιμές και πληροφορίες."""

    messages = [{"role": "user", "content": f"{context}\n\nΕρώτηση: {user_message}" if context else user_message}]
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        return f"❌ Σφάλμα Claude: {str(e)}"

def ai_chat(user_message, action=None, settings=None):
    """Main AI chat handler with RAG"""
    settings = settings or {}
    use_rag = settings.get('useRAG', True)
    
    context = ""
    if use_rag:
        # Search RAG for relevant context
        rag_results = search_rag(user_message, top_k=3)
        if rag_results:
            context = "📚 Σχετικές πληροφορίες από τη βάση:\n\n"
            for r in rag_results:
                context += f"**{r['title']}** ({r['category']})\n{r['text'][:500]}...\n\n"
    
    # Custom prompts based on action
    if action == 'quote':
        system = """Είσαι ειδικός στη δημιουργία προσφορών φωτοβολταϊκών.
Με βάση τις πληροφορίες που έχεις, δημιούργησε μια επαγγελματική προσφορά.
Συμπερίλαβε: προϊόντα, ποσότητες, τιμές, σύνολο, εγγύηση.
Χρησιμοποίησε τιμές από το context αν υπάρχουν."""
        return ask_claude(user_message, context, system)
    
    elif action == 'organize':
        system = """Βοήθησε με την οργάνωση και ταξινόμηση εγγράφων.
Πρότεινε κατηγορίες, tags, και τρόπους οργάνωσης."""
        return ask_claude(user_message, context, system)
    
    elif action == 'email':
        system = """Βοήθησε με τη σύνταξη επαγγελματικών emails.
Κράτα τον τόνο επαγγελματικό αλλά φιλικό.
Συμπερίλαβε χαιρετισμό, κύριο μήνυμα, και κλείσιμο."""
        return ask_claude(user_message, context, system)
    
    else:
        return ask_claude(user_message, context)

# ============ PDF GENERATOR ============

def generate_quote_pdf(quote_data):
    """Generate PDF quote"""
    try:
        # Create PDF
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # A4
        
        # Colors
        orange = (0.95, 0.61, 0.07)
        dark = (0.1, 0.1, 0.18)
        gray = (0.5, 0.5, 0.5)
        
        # Header
        header_rect = fitz.Rect(0, 0, 595, 100)
        page.draw_rect(header_rect, color=dark, fill=dark)
        
        # Logo/Title
        page.insert_text((40, 50), "ENERCON", fontsize=28, color=(1, 1, 1), fontname="helv")
        page.insert_text((40, 70), "Φωτοβολταϊκά Συστήματα", fontsize=12, color=gray, fontname="helv")
        
        # Quote number & date
        page.insert_text((400, 40), f"Προσφορά #{quote_data.get('number', '001')}", fontsize=14, color=(1, 1, 1), fontname="helv")
        page.insert_text((400, 60), f"Ημερομηνία: {quote_data.get('date', datetime.now().strftime('%d/%m/%Y'))}", fontsize=10, color=gray, fontname="helv")
        
        # Customer info
        y = 130
        page.insert_text((40, y), "ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ", fontsize=12, color=dark, fontname="helv")
        y += 20
        page.insert_text((40, y), f"Όνομα: {quote_data.get('customer_name', '')}", fontsize=10, color=dark, fontname="helv")
        y += 15
        page.insert_text((40, y), f"Email: {quote_data.get('customer_email', '')}", fontsize=10, color=dark, fontname="helv")
        y += 15
        page.insert_text((40, y), f"Τηλέφωνο: {quote_data.get('customer_phone', '')}", fontsize=10, color=dark, fontname="helv")
        
        # Products table
        y += 40
        page.insert_text((40, y), "ΠΡΟΪΟΝΤΑ", fontsize=12, color=dark, fontname="helv")
        y += 20
        
        # Table header
        page.draw_rect(fitz.Rect(40, y-5, 555, y+15), color=orange, fill=orange)
        page.insert_text((45, y+10), "Περιγραφή", fontsize=9, color=(1, 1, 1), fontname="helv")
        page.insert_text((300, y+10), "Ποσότητα", fontsize=9, color=(1, 1, 1), fontname="helv")
        page.insert_text((380, y+10), "Τιμή", fontsize=9, color=(1, 1, 1), fontname="helv")
        page.insert_text((470, y+10), "Σύνολο", fontsize=9, color=(1, 1, 1), fontname="helv")
        
        y += 25
        total = 0
        items = quote_data.get('items', [])
        for item in items:
            qty = item.get('qty', 1)
            price = item.get('price', 0)
            subtotal = qty * price
            total += subtotal
            
            page.insert_text((45, y), item.get('name', '')[:40], fontsize=9, color=dark, fontname="helv")
            page.insert_text((310, y), str(qty), fontsize=9, color=dark, fontname="helv")
            page.insert_text((380, y), f"€{price:,.2f}", fontsize=9, color=dark, fontname="helv")
            page.insert_text((470, y), f"€{subtotal:,.2f}", fontsize=9, color=dark, fontname="helv")
            y += 20
            
            # Line
            page.draw_line((40, y-5), (555, y-5), color=gray, width=0.5)
        
        # Total
        y += 20
        page.draw_rect(fitz.Rect(350, y-5, 555, y+25), color=dark, fill=dark)
        page.insert_text((360, y+15), f"ΣΥΝΟΛΟ: €{total:,.2f}", fontsize=14, color=(1, 1, 1), fontname="helv")
        
        # Notes
        if quote_data.get('notes'):
            y += 50
            page.insert_text((40, y), "ΣΗΜΕΙΩΣΕΙΣ", fontsize=12, color=dark, fontname="helv")
            y += 20
            page.insert_text((40, y), quote_data['notes'][:200], fontsize=9, color=gray, fontname="helv")
        
        # Footer
        footer_y = 800
        page.draw_line((40, footer_y), (555, footer_y), color=gray, width=0.5)
        page.insert_text((40, footer_y+15), "Enercon - Φωτοβολταϊκά Συστήματα | info@enercon.gr | +30 210 1234567", fontsize=8, color=gray, fontname="helv")
        page.insert_text((40, footer_y+28), f"Η προσφορά ισχύει για 30 ημέρες", fontsize=8, color=gray, fontname="helv")
        
        # Save
        filename = f"quote_{quote_data.get('number', 'draft')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        doc.save(filepath)
        doc.close()
        
        # Return base64 for download
        with open(filepath, 'rb') as f:
            pdf_data = base64.b64encode(f.read()).decode('utf-8')
        
        return {"success": True, "filename": filename, "data": pdf_data}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ EMAIL TEMPLATES ============

EMAIL_TEMPLATES = {
    "quote": {
        "name": "Αποστολή Προσφοράς",
        "subject": "Προσφορά Φωτοβολταϊκού Συστήματος - {customer_name}",
        "body": """Αγαπητέ/ή {customer_name},

Σας αποστέλλουμε τη ζητηθείσα προσφορά για φωτοβολταϊκό σύστημα {system_size}.

Η προσφορά περιλαμβάνει:
{items_list}

Συνολικό κόστος: €{total}

Η προσφορά ισχύει για 30 ημέρες από την ημερομηνία έκδοσης.

Παραμένουμε στη διάθεσή σας για οποιαδήποτε διευκρίνιση.

Με εκτίμηση,
Enercon Team"""
    },
    "followup": {
        "name": "Follow-up Προσφοράς",
        "subject": "Re: Προσφορά Φωτοβολταϊκού - Ενημέρωση",
        "body": """Αγαπητέ/ή {customer_name},

Επανερχόμαστε σχετικά με την προσφορά που σας αποστείλαμε στις {quote_date}.

Θα θέλαμε να μάθουμε αν έχετε τυχόν απορίες ή αν χρειάζεστε πρόσθετες πληροφορίες.

Είμαστε διαθέσιμοι για μια σύντομη τηλεφωνική συνομιλία ή συνάντηση.

Με εκτίμηση,
Enercon Team"""
    },
    "thankyou": {
        "name": "Ευχαριστήριο",
        "subject": "Ευχαριστούμε για την εμπιστοσύνη σας!",
        "body": """Αγαπητέ/ή {customer_name},

Σας ευχαριστούμε θερμά για την επιλογή της Enercon για το φωτοβολταϊκό σας σύστημα.

Η εγκατάσταση έχει προγραμματιστεί για {installation_date}.

Τεχνικός υπεύθυνος: {technician_name}
Τηλέφωνο επικοινωνίας: {technician_phone}

Για οποιαδήποτε απορία, μη διστάσετε να επικοινωνήσετε μαζί μας.

Με εκτίμηση,
Enercon Team"""
    },
    "reminder": {
        "name": "Υπενθύμιση Συντήρησης",
        "subject": "Υπενθύμιση Ετήσιας Συντήρησης",
        "body": """Αγαπητέ/ή {customer_name},

Σας υπενθυμίζουμε ότι πλησιάζει η ημερομηνία ετήσιας συντήρησης του φωτοβολταϊκού σας συστήματος.

Η τακτική συντήρηση εξασφαλίζει:
• Μέγιστη απόδοση
• Παράταση εγγύησης
• Πρόληψη βλαβών

Καλέστε μας στο +30 210 1234567 για να κλείσετε ραντεβού.

Με εκτίμηση,
Enercon Team"""
    }
}

def get_email_templates():
    return EMAIL_TEMPLATES

def fill_email_template(template_id, variables):
    template = EMAIL_TEMPLATES.get(template_id)
    if not template:
        return None
    
    subject = template['subject']
    body = template['body']
    
    for key, value in variables.items():
        subject = subject.replace('{' + key + '}', str(value))
        body = body.replace('{' + key + '}', str(value))
    
    return {"subject": subject, "body": body}

# ============ EMAIL FUNCTIONS ============

def parse_email_address(raw):
    if not raw:
        return "Άγνωστος"
    match = re.match(r'^"?([^"<]+)"?\s*<?([^>]*)>?', raw)
    if match:
        name = match.group(1).strip()
        email = match.group(2).strip()
        return name if name and name != email else (email or name)
    return raw.strip()

def fetch_emails(query, max_results=50):
    service = get_gmail_service()
    if not service:
        return []
    
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []
        
        for msg in messages:
            try:
                msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                headers = {h['name'].lower(): h['value'] for h in msg_data['payload'].get('headers', [])}
                
                sender_raw = headers.get('from') or headers.get('sender') or ''
                sender = parse_email_address(sender_raw)
                
                attachments = 0
                def count_attachments(parts):
                    count = 0
                    for part in parts:
                        if part.get('filename'):
                            count += 1
                        if 'parts' in part:
                            count += count_attachments(part['parts'])
                    return count
                
                if 'parts' in msg_data['payload']:
                    attachments = count_attachments(msg_data['payload']['parts'])
                
                labels = msg_data.get('labelIds', [])
                category = 'other'
                categoryLabel = 'Άλλο'
                if 'SENT' in labels:
                    category = 'sent'
                    categoryLabel = 'Απεσταλμένα'
                    to_raw = headers.get('to', '')
                    if to_raw:
                        sender = "→ " + parse_email_address(to_raw)
                elif 'CATEGORY_PERSONAL' in labels:
                    category = 'primary'
                    categoryLabel = 'Κύρια'
                elif 'CATEGORY_UPDATES' in labels:
                    category = 'updates'
                    categoryLabel = 'Ενημερώσεις'
                
                date_str = headers.get('date', '')
                try:
                    date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})', date_str)
                    date_parsed = date_match.group(1) if date_match else date_str[:20]
                except:
                    date_parsed = date_str[:20]
                
                # Extract body text
                def extract_body(payload):
                    if 'body' in payload and payload['body'].get('data'):
                        try:
                            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
                        except:
                            pass
                    if 'parts' in payload:
                        for part in payload['parts']:
                            if part.get('mimeType') == 'text/plain' and part['body'].get('data'):
                                try:
                                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                                except:
                                    pass
                            elif part.get('mimeType', '').startswith('multipart/'):
                                result = extract_body(part)
                                if result:
                                    return result
                    return ''
                
                body = extract_body(msg_data['payload']) or msg_data.get('snippet', '')
                body = re.sub(r'\n\s*\n', '\n\n', body).strip()[:5000]
                
                emails.append({
                    'id': msg['id'],
                    'subject': headers.get('subject', '(χωρίς θέμα)'),
                    'from': sender,
                    'date': date_parsed,
                    'snippet': msg_data.get('snippet', ''),
                    'body': body,
                    'attachments': attachments,
                    'category': category,
                    'categoryLabel': categoryLabel
                })
            except Exception as e:
                print(f"Error processing email: {e}")
        
        return emails
    except Exception as e:
        print(f"Gmail error: {e}")
        return []

def get_email_full_content(email_id):
    service = get_gmail_service()
    if not service:
        return None
    
    try:
        msg = service.users().messages().get(userId='me', id=email_id, format='full').execute()
        headers = {h['name'].lower(): h['value'] for h in msg['payload'].get('headers', [])}
        
        def extract_body(payload):
            if 'body' in payload and payload['body'].get('data'):
                try:
                    return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
                except:
                    pass
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain' and part['body'].get('data'):
                        try:
                            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        except:
                            pass
                    elif part.get('mimeType', '').startswith('multipart/'):
                        result = extract_body(part)
                        if result:
                            return result
            return ''
        
        body = extract_body(msg['payload']) or msg.get('snippet', '')
        body = re.sub(r'\n\s*\n', '\n\n', body).strip()
        
        return {
            'subject': headers.get('subject', ''),
            'from': parse_email_address(headers.get('from', '')),
            'to': parse_email_address(headers.get('to', '')),
            'date': headers.get('date', ''),
            'body': body[:10000]
        }
    except Exception as e:
        print(f"Error getting email: {e}")
        return None

def sync_email_to_rag(email_data):
    content = get_email_full_content(email_data['id'])
    if not content:
        return None
    
    text = f"""📧 Email από: {content['from']}
📅 Ημερομηνία: {content['date']}
📋 Θέμα: {content['subject']}

{content['body']}"""
    
    doc_id = f"email_{hashlib.md5(email_data['id'].encode()).hexdigest()[:12]}"
    result = pc.inference.embed(model="multilingual-e5-large", inputs=[text[:8000]], parameters={"input_type": "passage"})
    
    index.upsert(vectors=[{
        "id": doc_id,
        "values": result.data[0].values,
        "metadata": {"text": text[:8000], "category": "email", "title": f"Email: {content['subject'][:60]}", "from": content['from'], "date": content['date']}
    }])
    
    return doc_id

def sync_note_to_rag(title, content):
    text = f"""📝 Σημείωση: {title}
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}

{content}"""
    
    doc_id = f"note_{hashlib.md5(content.encode()).hexdigest()[:12]}"
    result = pc.inference.embed(model="multilingual-e5-large", inputs=[text[:8000]], parameters={"input_type": "passage"})
    
    index.upsert(vectors=[{
        "id": doc_id,
        "values": result.data[0].values,
        "metadata": {"text": text[:8000], "category": "note", "title": f"Σημείωση: {title[:50]}"}
    }])
    return doc_id

def fetch_calendar_events():
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        now = datetime.utcnow()
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',
            timeMax=(now + timedelta(days=30)).isoformat() + 'Z',
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except Exception as e:
        print(f"Calendar error: {e}")
        return []

def fetch_contacts():
    service = get_contacts_service()
    if not service:
        return []
    
    try:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=200,
            personFields='names,emailAddresses,phoneNumbers,organizations'
        ).execute()
        
        connections = results.get('connections', [])
        contacts = []
        
        for person in connections:
            names = person.get('names', [])
            emails = person.get('emailAddresses', [])
            phones = person.get('phoneNumbers', [])
            orgs = person.get('organizations', [])
            
            name = names[0].get('displayName', '') if names else ''
            if not name:
                continue
            
            contact = {
                'id': person.get('resourceName', ''),
                'name': name,
                'emails': [e.get('value', '') for e in emails],
                'phones': [p.get('value', '') for p in phones],
                'organization': orgs[0].get('name', '') if orgs else ''
            }
            contacts.append(contact)
        
        contacts.sort(key=lambda x: x['name'].lower())
        return contacts
    except Exception as e:
        print(f"Contacts error: {e}")
        return []

# ============ DOCUMENT FUNCTIONS ============

def generate_smart_title(text, filename, part_num=None, total_parts=None):
    brands = ['Fronius', 'SolaX', 'Solis', 'Huawei', 'BYD', 'JA Solar', 'Phono', 'Dyness', 'Sungrow', 'GoodWe']
    categories = {
        'inverter': ['inverter', 'hybrid', 'GEN24', 'SYMO', 'SUN2000'],
        'battery': ['battery', 'μπαταρ', 'HVS', 'HVM', 'LUNA'],
        'panel': ['panel', 'πάνελ', 'JAM', 'bifacial', 'mono', 'Wp'],
        'pricelist': ['τιμοκατάλογος', 'pricelist', 'τιμές', '€']
    }
    
    found_brand = next((b for b in brands if b.lower() in text.lower()), None)
    found_category = 'general'
    for cat, keywords in categories.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            found_category = cat
            break
    
    title_parts = [found_brand] if found_brand else [filename.rsplit('.', 1)[0]]
    cat_names = {'inverter': 'Inverters', 'battery': 'Μπαταρίες', 'panel': 'Panels', 'pricelist': 'Τιμοκατάλογος'}
    if cat_names.get(found_category):
        title_parts.append(cat_names[found_category])
    
    title = ' '.join(title_parts)
    if total_parts and total_parts > 1:
        title = f"{title} ({part_num}/{total_parts})"
    return title, found_category

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "".join(page.get_text() + "\n" for page in doc)
    doc.close()
    return text.strip()

def extract_text_from_excel(excel_bytes):
    import io
    df = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None)
    all_text = []
    for sheet_name, sheet_df in df.items():
        all_text.append(f"=== Φύλλο: {sheet_name} ===\n")
        # Get column names
        cols = list(sheet_df.columns)
        all_text.append(f"Στήλες: {', '.join(str(c) for c in cols)}\n")
        
        for idx, row in sheet_df.iterrows():
            # Create a readable entry for each row
            entry_parts = []
            for col in cols:
                val = row[col]
                if pd.notna(val):
                    val_str = str(val).strip()
                    if val_str:
                        entry_parts.append(f"{col}: {val_str}")
            if entry_parts:
                # Each row as a separate block for better search
                all_text.append("---\n" + "\n".join(entry_parts) + "\n")
    
    return "\n".join(all_text)

def smart_chunk(text, max_chars=3000):
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    # Try to split on record separators first (---)
    if '---' in text:
        records = text.split('---')
        current_chunk = ""
        for record in records:
            record = record.strip()
            if not record:
                continue
            if len(current_chunk) + len(record) + 5 <= max_chars:
                current_chunk += "\n---\n" + record if current_chunk else record
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = record
        if current_chunk:
            chunks.append(current_chunk)
        return chunks if chunks else [text]
    
    # Fallback to original chunking
    start = 0
    while start < len(text):
        end = start + max_chars
        if text[start:end].strip():
            chunks.append(text[start:end].strip())
        start = end - 300
    return chunks

# Create uploads directory
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

def search(query, top_k=15):
    result = pc.inference.embed(model="multilingual-e5-large", inputs=[query], parameters={"input_type": "query"})
    results = index.query(vector=result.data[0].values, top_k=top_k, include_metadata=True)
    return [{"id": m.id, "score": round(m.score, 3), "title": m.metadata.get("title", ""), "category": m.metadata.get("category", ""), "text": m.metadata.get("text", "")[:500], "filepath": m.metadata.get("filepath", "")} for m in results.matches]

def upload_file(file_data, filename, category):
    file_bytes = base64.b64decode(file_data)
    ext = filename.lower().split('.')[-1]
    
    if ext == 'pdf':
        text = extract_text_from_pdf(file_bytes)
    elif ext in ['xlsx', 'xls']:
        text = extract_text_from_excel(file_bytes)
    elif ext in ['txt', 'csv']:
        text = file_bytes.decode('utf-8', errors='ignore')
    else:
        return None, "Unsupported"
    
    if not text.strip():
        return None, "No text"
    
    # Save original file to uploads folder
    safe_filename = re.sub(r'[^\w\-\.]', '_', filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_filename = f"{timestamp}_{safe_filename}"
    filepath = os.path.join(UPLOADS_DIR, saved_filename)
    with open(filepath, 'wb') as f:
        f.write(file_bytes)
    
    chunks = smart_chunk(text)
    uploaded = []
    for i, chunk in enumerate(chunks):
        smart_title, detected_cat = generate_smart_title(chunk, filename, i+1 if len(chunks)>1 else None, len(chunks) if len(chunks)>1 else None)
        final_cat = detected_cat if category == 'general' else category
        doc_id = hashlib.md5(chunk.encode()).hexdigest()[:16]
        result = pc.inference.embed(model="multilingual-e5-large", inputs=[chunk], parameters={"input_type": "passage"})
        index.upsert(vectors=[{"id": doc_id, "values": result.data[0].values, "metadata": {"text": chunk[:8000], "category": final_cat, "title": smart_title, "filepath": saved_filename, "original_filename": filename}}])
        uploaded.append({"id": doc_id, "title": smart_title, "filepath": saved_filename})
    return uploaded, None

def get_file(filename):
    """Get file from uploads folder"""
    filepath = os.path.join(UPLOADS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

def get_stats():
    stats = index.describe_index_stats()
    return {"total_vectors": stats.total_vector_count}

def delete_doc(doc_id):
    index.delete(ids=[doc_id])

def list_docs(limit=50):
    result = pc.inference.embed(model="multilingual-e5-large", inputs=["solar inverter panel battery email note"], parameters={"input_type": "query"})
    results = index.query(vector=result.data[0].values, top_k=limit, include_metadata=True)
    return [{"id": m.id, "title": m.metadata.get("title", ""), "category": m.metadata.get("category", "")} for m in results.matches]

# ============ WEBSOCKET HANDLER ============

async def handler(websocket):
    print("✅ Client connected")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")
                
                if action == "search":
                    await websocket.send(json.dumps({"action": "search_results", "results": search(data.get("query", ""), data.get("top_k", 15))}))
                
                elif action == "upload_file":
                    uploaded, error = upload_file(data.get("file_data", ""), data.get("filename", ""), data.get("category", "general"))
                    if error:
                        await websocket.send(json.dumps({"action": "error", "message": error}))
                    else:
                        await websocket.send(json.dumps({"action": "file_upload_success", "files": uploaded, "count": len(uploaded)}))
                
                elif action == "fetch_emails":
                    emails = fetch_emails(data.get("query", ""), data.get("max_results", 50))
                    await websocket.send(json.dumps({"action": "emails_loaded", "emails": emails}))
                
                elif action == "sync_emails":
                    emails = data.get("emails", [])
                    synced = 0
                    for email in emails:
                        try:
                            if sync_email_to_rag(email):
                                synced += 1
                                await websocket.send(json.dumps({"action": "email_sync_success", "subject": email.get('subject', '')[:50]}))
                        except Exception as e:
                            print(f"Sync error: {e}")
                    await websocket.send(json.dumps({"action": "email_sync_complete", "count": synced}))
                
                elif action == "sync_note":
                    sync_note_to_rag(data.get("title", ""), data.get("content", ""))
                    await websocket.send(json.dumps({"action": "note_synced"}))
                
                elif action == "fetch_calendar":
                    await websocket.send(json.dumps({"action": "calendar_events", "events": fetch_calendar_events()}))
                
                elif action == "fetch_contacts":
                    await websocket.send(json.dumps({"action": "contacts_loaded", "contacts": fetch_contacts()}))
                
                elif action == "stats":
                    await websocket.send(json.dumps({"action": "stats", "data": get_stats()}))
                
                elif action == "get_file":
                    filename = data.get("filename", "")
                    file_data = get_file(filename)
                    if file_data:
                        await websocket.send(json.dumps({"action": "file_data", "filename": filename, "data": file_data}))
                    else:
                        await websocket.send(json.dumps({"action": "error", "message": "File not found"}))
                
                elif action == "list":
                    await websocket.send(json.dumps({"action": "list_results", "docs": list_docs()}))
                
                elif action == "delete":
                    delete_doc(data.get("doc_id"))
                    await websocket.send(json.dumps({"action": "delete_success"}))
                
                # AI Actions
                elif action == "ai_chat":
                    response = ai_chat(data.get("message", ""), data.get("ai_action"), data.get("settings", {}))
                    await websocket.send(json.dumps({"action": "ai_response", "response": response}))
                
                elif action == "set_claude_key":
                    success = init_claude(data.get("api_key", ""))
                    await websocket.send(json.dumps({"action": "claude_key_set", "success": success}))
                
                # PDF
                elif action == "generate_pdf":
                    result = generate_quote_pdf(data.get("quote_data", {}))
                    await websocket.send(json.dumps({"action": "pdf_generated", **result}))
                
                # Email Templates
                elif action == "get_email_templates":
                    await websocket.send(json.dumps({"action": "email_templates", "templates": get_email_templates()}))
                
                elif action == "fill_template":
                    filled = fill_email_template(data.get("template_id", ""), data.get("variables", {}))
                    await websocket.send(json.dumps({"action": "template_filled", "result": filled}))
                    
            except Exception as e:
                print(f"Error: {e}")
                await websocket.send(json.dumps({"action": "error", "message": str(e)}))
    except websockets.exceptions.ConnectionClosed:
        print("❌ Client disconnected")

async def main():
    print("="*50)
    print("🚀 Enercon Knowledge Base Server v3")
    print("📡 WebSocket: ws://localhost:8765")
    print("="*50)
    
    try:
        gmail, calendar, contacts = get_google_services()
        if gmail: print("✅ Gmail API")
        if calendar: print("✅ Calendar API")
        if contacts: print("✅ Contacts API")
        if not gmail: print("⚠️ Google APIs not configured")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    
    # Load Claude key from env
    claude_key = os.environ.get('CLAUDE_API_KEY', '')
    if claude_key:
        init_claude(claude_key)
        print("✅ Claude API")
    else:
        print("⚠️ Claude API not configured (set CLAUDE_API_KEY or configure in app)")
    
    async with websockets.serve(handler, "localhost", 8765, max_size=50*1024*1024):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
