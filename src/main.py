import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.ingestion import add_transcript_to_vectorstore
from utils.vectorstore import create_vectorstore, read_vectorstore
from utils.fetch_transcript import save_transcript_as_txt, read_transcript, get_video_metadata, store_metadata
from utils.yt_summarizer import q_and_a, summarizer
import models
import database


models.Base.metadata.create_all(bind=database.engine)
video=database.SessionLocal().query(models.Video).filter(models.Video.video_id == "3Ul_dn4da5o").first()
print(video)



# it's created for only one time
if not os.path.exists("./.transcript_chroma"):
    VECTORSTORE = create_vectorstore()
    print("[INFO] Vectorstore was created.")
else:
    print("[INFO] Vectorstore was found.")
    VECTORSTORE = read_vectorstore()
    



# check video_id in database(txt file in this case)
def check_video_id(video_id):
    if not os.path.exists("video_id.txt"):
        f = open("video_id.txt", "w")
        f.close()
    else:
        try:
            with open("video_id.txt", "r") as f:
                
                lines = f.readlines()
                
                for line in lines:
                    
                    if video_id == line.strip():
                        
                        return True
                
                return False
                
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            print("Error: video_id.txt not found.")
            return False
            

def check_video_id_in_db(video_id, db=database.SessionLocal()):
    '''Check if video_id already exists in database'''
    try:
        video = next(db.query(models.Video).filter(models.Video.video_id == video_id).first())
        return video is not None
    finally:
        db.close()

def summary(video_id):
    """generate summary from video id.
    
    Parameters:
        video_id: str
        
    Returns:
        summary: str
    """
    transcript = read_transcript(video_id)
    summary = summarizer(transcript)
    return summary

def ai_process(scope, question, channel_id=None, video_id=None):
    """does q_and_a and returns answer
    
    Parameters:
        scope: str
        question: str
        channel_id: str | None
        video_id: str | None
        
    Returns:
        answer: str
    """

    if scope == "video":
        retriever = VECTORSTORE.as_retriever(search_type="similarity", search_kwargs={"k": 3, "filter": {"video_id": video_id}}) # 1 videonun transcriptinden gelir
        answer = q_and_a(question=question, retriever=retriever)
    elif scope == "channel":
        retriever = VECTORSTORE.as_retriever(search_type="similarity", search_kwargs={"k": 3, "filter": {"channel_id": channel_id}}) # 1 kanalın 1 den fazla videosununn transcriptinden gelir
        answer = q_and_a(question=question, retriever=retriever)
    
    return answer

def main_add_transcript_to_system(video_url, db):
    metadata = get_video_metadata(video_url=video_url)
    VIDEO_ID = metadata["video_id"]
    CHANNEL_ID = metadata["channel_id"]
    print(metadata)
    

    if check_video_id(video_id=VIDEO_ID):
        print("[INFO] Video id have already found in database. ")
    else:
        print("[INFO] Video id was not found in video_id.txt file. It will be added to it.")
        save_transcript_as_txt(video_id=VIDEO_ID)
        print("[INFO] Transcript was saved as txt to transcript folder.")
        store_metadata(metadata=metadata, db=db, video_url=video_url)
        print("[INFO] Informations were saved to database.")
        add_transcript_to_vectorstore(video_id=VIDEO_ID, vectorstore=VECTORSTORE)
        print("[INFO] Transcript was added to vectorstore as document.")

    return VIDEO_ID, CHANNEL_ID

if __name__ == "__main__":

    VIDEO_URL = "https://www.youtube.com/watch?v=_WEkqYF1Jgk"

    VIDEO_ID, CHANNEL_ID = main_add_transcript_to_system(video_url=VIDEO_URL, db=database.SessionLocal())
    
    opt = input("type 0 to chat with video only and see the summary or 1 to chat with cumulative channel knowledge: ")

    # for the extracted video only
    if opt == "0":
        summary = summary(video_id=VIDEO_ID)
        print("[INFO] Summary Generated: ", summary)
        user_question = input("> Ask a question about the video: ")
        answer = ai_process(vectorstore=VECTORSTORE, scope="video", question=user_question, video_id=VIDEO_ID)
        print(answer)
    
    # for the cumulative channel knowledge
    elif opt == "1":    
        user_question = input("> Ask a question about the video: ")
        answer = ai_process(vectorstore=VECTORSTORE, scope="channel", question=user_question, channel_id=CHANNEL_ID)
        print(answer)
    else:
        print("Enter a valid value!")

    

