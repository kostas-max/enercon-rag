# Enercon RAG - Context για νέα συζήτηση

## 📍 Project Path
```
C:\Users\USER\Desktop\Enercon-RAG\
```

## 📦 Κύρια Αρχεία
- `pinecone_app_v2.html` - Frontend (πλήρες UI)
- `pinecone_server_v2.py` - Backend WebSocket Server
- `credentials.json` - Google OAuth
- `ENERCON_RAG_DOCUMENTATION.md` - Πλήρης τεκμηρίωση

## 🔧 Stack
- Python WebSocket server (port 8765)
- Pinecone vector DB (index: `enercon`)
- Claude AI (Anthropic API)
- Google APIs (Gmail, Calendar, Contacts)
- PyMuPDF για PDF generation

## ✅ Τι έχει υλοποιηθεί
1. **RAG Search** - Αναζήτηση με embeddings (multilingual-e5-large)
2. **Document Upload** - PDF, Excel, TXT με auto-categorization
3. **Gmail Sync** - Φόρτωση & sync emails στο RAG
4. **Google Calendar** - Sync events
5. **Google Contacts** - Φόρτωση επαφών
6. **Σημειώσεις** - CRUD + sync στο RAG
7. **AI Assistant** - Claude integration με RAG context
8. **PDF Generator** - Δημιουργία προσφορών
9. **Email Templates** - 4 πρότυπα (quote, followup, thankyou, reminder)
10. **Prompts Settings** - Customizable AI prompts
11. **Auto-sync** - Emails κάθε 10 λεπτά
12. **Memory Stats** - Χρήση Pinecone

## 🔑 APIs
- **Pinecone**: `pcsk_5cxk9S_...` (index: enercon)
- **Google OAuth**: Desktop App client
- **Claude**: Ρυθμίζεται από UI

## 🚀 Εκκίνηση
```bash
cd C:\Users\USER\Desktop\Enercon-RAG
python pinecone_server_v2.py
# Άνοιξε pinecone_app_v2.html σε browser
```

## 📝 Σημειώσεις
- Για νέο Google auth: διαγράψε `token.pickle`
- Claude API key βάζεις στο UI Settings
- WebSocket: `ws://localhost:8765`

## 🔜 Πιθανές επεκτάσεις
- Send emails
- Attachment extraction
- Cloud deployment
- Mobile app
