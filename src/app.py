from fastapi import FastAPI
import uvicorn
from main import q_answer, summarizer, 
from pydantic import BaseModel
from utils.fetch_transcript import read_transcript
import database


app = FastAPI()

# DB oturumu alma
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"Project Name": "YT Video Q&A Assistant"}


@app.post("/add_transcript_to_system")
def add_transcript_to_system(video_url):

    video_id = url_to_vectorstore(video_url=video_url)

    transcript = read_transcript(video_id=video_id)

    return transcript

@app.post("/chat")
def chat(question):

    answer = q_answer(question=question)

    return answer


@app.post("/summarize")
def summarize(transcript):

    summary = summarizer(transcript)

    return summary



if __name__ == "__main__":
    uvicorn.run(app, port=8000)


