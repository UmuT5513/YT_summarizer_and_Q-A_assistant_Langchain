# YouTube Video Q&A Assistant

<img width="724" height="870" alt="Screenshot from 2025-12-16 22-59-29" src="https://github.com/user-attachments/assets/26f59d76-399d-4495-9183-567a22e16b7c" />

<img width="724" height="870" alt="Screenshot from 2025-12-16 22-59-36" src="https://github.com/user-attachments/assets/bad66abd-e31b-4c56-85f3-da9ea05b5d64" />

An AI-powered assistant that fetches YouTube video transcripts, generates structured summaries, and answers questions about video content using **Retrieval-Augmented Generation (RAG)** with LangChain and OpenAI.

---

## Features

- **Transcript Fetching** — Automatically fetch and save YouTube video transcripts using `youtube-transcript-api` and `yt-dlp`
- **Video Summarization** — Generate structured summaries with title, bullet-point summary, and key takeaways via OpenAI GPT-4o-mini
- **Q&A with RAG** — Ask questions about video content; relevant transcript chunks are retrieved from a vector database and passed to the LLM for context-aware answers
- **Scope-Based Q&A** — Chat with a single video's transcript or query across an entire channel's cumulative knowledge
- **Vector Database** — Persistent storage with ChromaDB and OpenAI embeddings for efficient similarity search
- **SQLite Database** — Stores video and channel metadata (title, duration, language, word count, etc.) via SQLAlchemy
- **Multiple Interfaces**:
  - **CLI** — Command-line interface (`main.py`)
  - **REST API** — FastAPI backend (`app.py`) with full CRUD endpoints
  - **Web GUI** — Streamlit frontend (`gui.py`) with dark-themed modern UI
- **Incremental Processing** — Skips videos that have already been processed to avoid duplication

---

## Project Structure

```
YT_summarizer_and_Q-A_assistant_Langchain/
├── README.md
├── requirements.txt
├── video_id.txt                    # Tracks processed video IDs
├── app.db                          # SQLite database (auto-created)
├── .env                            # OpenAI API key (user-created)
├── src/
│   ├── __init__.py
│   ├── main.py                     # CLI entry point
│   ├── app.py                      # FastAPI REST API server
│   ├── gui.py                      # Streamlit web interface
│   ├── models.py                   # SQLAlchemy ORM models (Channel, Video)
│   ├── database.py                 # Database engine & session configuration
│   ├── schemas.py                  # Pydantic schemas for API validation
│   ├── test_models.py              # Unit tests
│   └── utils/
│       ├── __init__.py
│       ├── fetch_transcript.py     # Transcript fetching, metadata extraction & DB storage
│       ├── ingestion.py            # Document loading, splitting & vector store ingestion
│       ├── vectorstore.py          # ChromaDB vector store creation & loading
│       └── yt_summarizer.py        # LLM summarization & Q&A chains
├── transcripts/                    # Saved transcript .txt files
│   └── transcript_[video_id].txt
└── .transcript_chroma/             # ChromaDB persistent storage (auto-created)
```

---

## How It Works

```
YouTube URL
    │
    ▼
┌─────────────────────┐
│  1. Fetch Metadata   │  yt-dlp extracts video title, duration, channel info
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Fetch Transcript │  youtube-transcript-api downloads the transcript
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Store Metadata   │  SQLAlchemy saves Channel & Video records to SQLite
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Chunk & Embed    │  LangChain splits text into 500-char chunks,
│                      │  OpenAI embeds them, stored in ChromaDB
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  5. Summarize / Q&A                         │
│                                             │
│  Summarize: Full transcript → GPT-4o-mini   │
│             → Structured output (title,     │
│               summary, key takeaways)       │
│                                             │
│  Q&A: Question → Similarity search on       │
│       ChromaDB → Top 3 chunks + question    │
│       → GPT-4o-mini → Answer                │
└─────────────────────────────────────────────┘
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/YT_summarizer_and_Q-A_assistant_Langchain.git
cd YT_summarizer_and_Q-A_assistant_Langchain
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Usage

### Option 1: Command-Line Interface

```bash
python -m src.main
```

- Processes a YouTube video URL (set `VIDEO_URL` in `main.py`)
- Generates a summary
- Lets you ask questions interactively in the terminal

### Option 2: REST API + Web GUI (Recommended)

**Terminal 1 — Start the FastAPI server:**

```bash
uvicorn src.app:app --reload
```

The API runs at `http://127.0.0.1:8000` with the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/videos` | List all processed videos |
| `GET` | `/channels` | List all channels |
| `GET` | `/channels/{channel_id}` | Get channel details |
| `GET` | `/transcript/{video_id}` | View a saved transcript |
| `POST` | `/add_transcript_to_system` | Process a new YouTube video |
| `POST` | `/summarize/{video_id}` | Generate AI summary |
| `POST` | `/chat_video/{video_id}` | Q&A scoped to a single video |
| `POST` | `/chat_channel/{channel_id}` | Q&A across an entire channel |

**Terminal 2 — Start the Streamlit GUI:**

```bash
streamlit run src/gui.py
```

The web interface provides:

- **Add Video** — Paste a YouTube URL and process it
- **Summarize** — Select a video and generate an AI summary
- **Q&A Chat** — Ask questions scoped to a video or channel
- **Transcript** — View saved transcripts

> **Note:** The Streamlit GUI requires the FastAPI server to be running.

---

## License

This project is open-source. Please check the license file for details.





