# YouTube Video Q&A Assistant

<img width="724" height="870" alt="Screenshot from 2025-12-16 22-59-29" src="https://github.com/user-attachments/assets/26f59d76-399d-4495-9183-567a22e16b7c" />

<img width="724" height="870" alt="Screenshot from 2025-12-16 22-59-36" src="https://github.com/user-attachments/assets/bad66abd-e31b-4c56-85f3-da9ea05b5d64" />


A comprehensive AI-powered assistant that allows users to fetch YouTube video transcripts, generate summaries, and ask questions about video content using Retrieval-Augmented Generation (RAG).

## Features

- **Transcript Fetching**: Automatically fetch and save YouTube video transcripts
- **Video Summarization**: Generate structured summaries with key takeaways using OpenAI GPT models
- **Q&A System**: Ask questions about video content with context-aware answers
- **Vector Database**: Persistent storage using ChromaDB for efficient retrieval
- **Multiple Interfaces**:
  - Command-line interface (`main.py`)
  - REST API (`app.py` with FastAPI)
  - Web GUI (`gui.py` with Streamlit)
- **Incremental Processing**: Avoid reprocessing videos already in the system

## Project Structure

```
yt_video_summary/
├── README.md
├── requirements.txt
├── video_id.txt                 # Tracks processed video IDs
├── test.ipynb                   # Simple test notebook
├── src/
│   ├── main.py                  # Command-line interface
│   ├── app.py                   # FastAPI backend server
│   ├── gui.py                   # Streamlit web interface
│   └── utils/
│       ├── fetch_transcript.py  # YouTube transcript fetching
│       ├── ingestion.py         # Document processing and vector store operations
│       ├── vectorstore.py       # ChromaDB vector store management
│       └── yt_summarizer.py     # AI summarization and Q&A logic
├── transcripts/                 # Saved transcript text files
│   ├── transcript_[video_id].txt
└── .transcript_chroma/          # ChromaDB persistent storage (auto-created)
```

## How It Works

1. **Transcript Fetching**: Uses `youtube-transcript-api` to download video transcripts
2. **Document Processing**: Splits transcripts into chunks using LangChain's text splitters
3. **Vector Storage**: Embeds and stores chunks in ChromaDB using OpenAI embeddings
4. **Retrieval**: Uses similarity search to find relevant content for questions
5. **Generation**: Combines retrieved context with user questions for accurate answers
6. **Summarization**: Structured output with video title, summary, and key takeaways


## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/yt_video_summary
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Command-Line Interface

Run the main script to process a video and interact via terminal:

```bash
python src/main.py
```

This will:
1. Process the default video URL (or modify `VIDEO_URL` in `main.py`)
2. Generate a summary
3. Allow you to ask questions interactively

### REST API Server

Start the FastAPI server:

```bash
python src/app.py
```

The API will be available at `http://127.0.0.1:8000` with endpoints:

- `GET /` - Health check
- `POST /add_transcript_to_system` - Add a video transcript (params: `video_url`)
- `POST /chat` - Ask a question (params: `question`)
- `POST /summarize` - Generate summary (params: `transcript`)

### Web GUI

Start the Streamlit interface:

```bash
streamlit run src/gui.py
```

This provides a user-friendly web interface to:
1. Enter YouTube video URLs
2. View generated summaries
3. Ask questions in a chat-like interface

**Note**: The GUI requires the FastAPI server to be running in the background.


## Dependencies

Key libraries used:
- `langchain-openai`: OpenAI integration
- `langchain-chroma`: Vector database
- `youtube-transcript-api`: YouTube transcript fetching
- `fastapi`: REST API framework
- `streamlit`: Web interface



## License

This project is open-source. Please check the license file for details.





