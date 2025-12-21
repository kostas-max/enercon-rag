# Enercon RAG - Knowledge Base για Φωτοβολταϊκά

AI-powered knowledge base για διαχείριση εγγράφων, emails και επαφών φωτοβολταϊκών συστημάτων.

## Features

- 🔍 **Semantic Search** - Αναζήτηση με AI (RAG)
- 📄 **Document Upload** - PDF, Excel, TXT
- 📧 **Gmail Sync** - Συγχρονισμός emails
- 📅 **Google Calendar** - Events
- 👥 **Google Contacts** - Επαφές
- 📝 **Notes** - Σημειώσεις
- 🤖 **AI Assistant** - Claude integration
- 📊 **PDF Generator** - Δημιουργία προσφορών

## Installation

### 1. Clone & Install dependencies

```bash
git clone https://github.com/yourusername/enercon-rag.git
cd enercon-rag
pip install -r requirements.txt
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required keys:
- `PINECONE_API_KEY` - Get from [Pinecone Console](https://app.pinecone.io/)
- `PINECONE_INDEX_NAME` - Your index name (default: enercon)
- `CLAUDE_API_KEY` - Get from [Anthropic Console](https://console.anthropic.com/) (optional)

### 3. Google OAuth Setup (for Gmail/Calendar/Contacts)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable APIs: Gmail, Calendar, People
4. Create OAuth 2.0 credentials (Desktop App)
5. Download `credentials.json` to project folder

### 4. Run

```bash
python pinecone_server_v2.py
```

Then open `pinecone_app_v2.html` in your browser.

## Tech Stack

- **Backend**: Python, WebSocket, asyncio
- **Database**: Pinecone (vector DB)
- **AI**: Claude (Anthropic), multilingual-e5-large embeddings
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: Gmail, Google Calendar, Google Contacts

## File Structure

```
enercon-rag/
├── pinecone_server_v2.py   # Backend server
├── pinecone_app_v2.html    # Frontend UI
├── credentials.json        # Google OAuth (not in git)
├── token.pickle           # OAuth token (not in git)
├── .env                   # API keys (not in git)
├── .env.example           # Example env file
├── .gitignore
├── requirements.txt
├── uploads/               # Uploaded files (not in git)
└── README.md
```

## License

MIT
