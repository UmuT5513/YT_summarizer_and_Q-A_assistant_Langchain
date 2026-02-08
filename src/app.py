from fastapi import FastAPI
import uvicorn
from utils.yt_summarizer import summarizer 
from main import ai_process, main_add_transcript_to_system
from utils.fetch_transcript import read_transcript
import database
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas


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



# transcript endpoints
@app.get("/transcript/{video_id}")
def get_transcript(video_id: str, session: Session = Depends(get_db)):
    """Read a saved transcript"""
    video = session.query(models.Video).filter(models.Video.video_id == video_id).first()
    text = read_transcript(video_id=video.video_id)
    return {"video_id": video_id, "transcript": text}

@app.post("/add_transcript_to_system")
def add_transcript_to_system(video_url, session: Session = Depends(get_db))-> None:
    
    video_id, channel_id = main_add_transcript_to_system(video_url=video_url, db=session)

    return {"video_id":video_id,"channel_id":channel_id,"message":"[INFO] Transcript was added to system."}
    


# ---- Channel Endpoints ----
@app.get("/channels")
def list_channels(db: Session = Depends(get_db)):
    return db.query(models.Channel).all()

@app.get("/channels/{channel_id}")
def get_channel(channel_id: str, db: Session = Depends(get_db)):
    return db.query(models.Channel).filter(models.Channel.channel_id == channel_id).first()

@app.post("/chat_channel/{channel_id}")
def chat_channel(question, channel_id):
    scope="channel"

    answer = ai_process(scope=scope, question=question, channel_id=channel_id)

    return {"channel_id": channel_id, "question": question, "answer": answer}


@app.get("/videos")
def list_videos(db: Session = Depends(get_db)):
    return db.query(models.Video).all()

@app.post("/chat_video/{video_id}")
def chat_video(question, video_id):
    scope="video"

    answer = ai_process(scope=scope, question=question, video_id=video_id)

    return {"video_id": video_id, "question": question, "answer": answer}


@app.post("/summarize/{video_id}")
def summarize(video_id):

    transcript = read_transcript(video_id=video_id)
    summary = summarizer(transcript=transcript)

    return {"video_id": video_id, "summary": summary}



if __name__ == "__main__":
    uvicorn.run("src.app:app", port=8000, reload=True)


