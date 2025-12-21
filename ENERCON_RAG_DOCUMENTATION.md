# Enercon Knowledge Base - Project Documentation

## 📋 Overview
AI-powered knowledge base για διαχείριση εγγράφων φωτοβολταϊκών συστημάτων με RAG (Retrieval Augmented Generation), Gmail sync, Google Calendar, Contacts και Claude AI integration.

---

## 📁 Project Location
```
C:\Users\USER\Desktop\Enercon-RAG\
```

## 📦 Αρχεία Project

| Αρχείο | Περιγραφή |
|--------|-----------|
| `pinecone_app_v2.html` | Frontend UI (HTML/JS/CSS) |
| `pinecone_server_v2.py` | Backend WebSocket Server |
| `credentials.json` | Google OAuth credentials |
| `token.pickle` | Google auth token (auto-generated) |

---

## 🔧 Tech Stack

- **Backend**: Python 3, WebSocket (asyncio)
- **Vector DB**: Pinecone (index: `enercon`)
- **Embeddings**: `multilingual-e5-large`
- **AI**: Claude API (Anthropic)
- **PDF**: PyMuPDF (fitz)
- **Google APIs**: Gmail, Calendar, Contacts (People API)

---

## 🔑 API Keys & Credentials

### Pinecone
```
API_KEY: pcsk_5cxk9S_U6bg96gFJEfFWm1da2fwmVqRdGd9cEt1UNq7WhznwJneHFwMH1EdQaKKLRkWuVH
INDEX: enercon
```

### Google OAuth
- **Client ID**: `1095141208661-aj7gt5s90qd1lrdo7nn3d0nr15jcep0b.apps.googleusercontent.com`
- **Type**: Desktop App
- **Scopes**:
  - `gmail.readonly`
  - `gmail.send`
  - `calendar.readonly`
  - `contacts.readonly`

### Claude API
- Ρυθμίζεται από το UI (Settings → Claude AI)
- Ή με environment variable: `CLAUDE_API_KEY`

---

## 🚀 Εκκίνηση

### 1. Εγκατάσταση Dependencies
```bash
pip install pinecone-client websockets pandas PyMuPDF anthropic google-auth google-auth-oauthlib google-api-python-client
```

### 2. Start Server
```bash
cd C:\Users\USER\Desktop\Enercon-RAG
python pinecone_server_v2.py
```

### 3. Άνοιγμα UI
Άνοιξε το `pinecone_app_v2.html` σε browser

---

## 🎯 Features

### 1. Αναζήτηση (RAG)
- Semantic search σε όλα τα έγγραφα
- Multilingual support (EL/EN)
- Score-based ranking

### 2. Upload Εγγράφων
- PDF, Excel, TXT, CSV
- Auto-categorization (panel, inverter, battery, pricelist)
- Smart chunking (3000 chars)
- Brand detection (Fronius, SolaX, Huawei, BYD, etc.)

### 3. Email Sync
- Φόρτωση από Gmail
- Filters: κατηγορία, ημέρες, συνημμένα
- Sync επιλεγμένων στο RAG
- Auto-sync κάθε 10 λεπτά

### 4. Επαφές
- Google Contacts integration
- Τηλέφωνα & emails (clickable)
- Αναζήτηση

### 5. Σημειώσεις
- CRUD operations
- Sync στο RAG
- localStorage persistence

### 6. Ημερολόγιο
- Month view
- Google Calendar sync
- Local events
- Διαγραφή events

### 7. AI Assistant ✨
- **Chat**: Συνομιλία με Claude + RAG context
- **Προσφορά**: Quote builder με PDF export
- **Templates**: Email πρότυπα
- **Prompts**: Customizable AI prompts

### 8. PDF Generator
- Επαγγελματική προσφορά
- Στοιχεία πελάτη
- Πίνακας προϊόντων
- Auto-calculate σύνολο
- Download PDF

### 9. Email Templates
| Template | Χρήση |
|----------|-------|
| `quote` | Αποστολή προσφοράς |
| `followup` | Υπενθύμιση προσφοράς |
| `thankyou` | Ευχαριστήριο μετά αγορά |
| `reminder` | Υπενθύμιση συντήρησης |

---

## 🌐 WebSocket API

**Endpoint**: `ws://localhost:8765`

### Actions

| Action | Description | Params |
|--------|-------------|--------|
| `search` | Αναζήτηση RAG | `query`, `top_k` |
| `upload_file` | Upload αρχείου | `file_data`, `filename`, `category` |
| `fetch_emails` | Φόρτωση emails | `query`, `max_results` |
| `sync_emails` | Sync στο RAG | `emails[]` |
| `sync_note` | Sync σημείωσης | `title`, `content` |
| `fetch_calendar` | Google Calendar | - |
| `fetch_contacts` | Google Contacts | - |
| `ai_chat` | Claude AI chat | `message`, `ai_action`, `settings` |
| `set_claude_key` | Set API key | `api_key` |
| `generate_pdf` | Δημιουργία PDF | `quote_data` |
| `get_email_templates` | Get templates | - |
| `fill_template` | Fill template | `template_id`, `variables` |
| `stats` | Στατιστικά | - |
| `list` | Λίστα εγγράφων | - |
| `delete` | Διαγραφή | `doc_id` |

---

## 📊 Data Schema

### Pinecone Vector
```json
{
  "id": "hash_16chars",
  "values": [1024 floats],
  "metadata": {
    "text": "content (max 8000)",
    "category": "panel|inverter|battery|pricelist|email|note",
    "title": "Smart generated title",
    "from": "sender (for emails)",
    "date": "date string"
  }
}
```

### LocalStorage Keys
| Key | Content |
|-----|---------|
| `enercon_notes` | `[{id, title, content, updated}]` |
| `enercon_events` | `[{id, title, date, time, desc, googleId?}]` |
| `enercon_settings` | `{autoSync, useRAG, claudeKey}` |
| `enercon_prompts` | `{search, quote, email, general}` |

---

## 🔄 Google API Setup

1. **Google Cloud Console** → Create Project
2. **Enable APIs**:
   - Gmail API
   - Google Calendar API
   - People API (Contacts)
3. **OAuth Consent Screen** → External
4. **Credentials** → OAuth 2.0 → Desktop App
5. **Download** `credentials.json` → project folder
6. **Delete** `token.pickle` για re-auth με νέα permissions

---

## 📝 Default AI Prompts

```javascript
{
  search: "Βοήθησε με την αναζήτηση προϊόντων και τιμών. Χρησιμοποίησε το RAG context.",
  quote: "Δημιούργησε επαγγελματική προσφορά φωτοβολταϊκού. Προϊόντα, τιμές, εγγύηση.",
  email: "Σύνταξε επαγγελματικό email. Τόνος φιλικός αλλά επαγγελματικός.",
  general: "Είσαι ο AI βοηθός του Enercon. Βοηθάς με φωτοβολταϊκά, τιμές, εγκαταστάσεις."
}
```

---

## 🎨 UI Theme

- **Background**: `#1a1a2e` → `#16213e` gradient
- **Cards**: `#2d2d44`
- **Accent**: `#f39c12` (orange)
- **Success**: `#27ae60` (green)
- **Error**: `#e74c3c` (red)
- **AI**: `#9b59b6` → `#3498db` gradient

---

## 📈 Memory Stats

- **Max Vectors**: 10,000 (Pinecone free tier)
- **Chunk Size**: 3,000 chars
- **Overlap**: 300 chars
- **Embedding Dim**: 1024

---

## 🐛 Troubleshooting

### "Gmail API not configured"
→ Βάλε `credentials.json` στον φάκελο

### "redirect_uri_mismatch"
→ Χρησιμοποίησε Desktop App (όχι Web App)

### "token.pickle error"
→ Διέγραψέ το και restart server

### "Claude API error"
→ Έλεγξε το API key στα Settings

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | - | Basic RAG search |
| v2.0 | - | Email sync, Notes, Calendar |
| v2.1 | - | Contacts, Auto-sync |
| v3.0 | Dec 2024 | Claude AI, PDF Generator, Email Templates, Prompts Menu |

---

## 🔜 Future Improvements

- [ ] Send emails από την εφαρμογή
- [ ] Attachment extraction από emails
- [ ] Multi-user support
- [ ] Cloud deployment
- [ ] Mobile app (React Native)
- [ ] Voice commands
- [ ] Analytics dashboard

---

## 👤 Contact

Project για: **Enercon Φωτοβολταϊκά**

---

*Last updated: December 2024*
