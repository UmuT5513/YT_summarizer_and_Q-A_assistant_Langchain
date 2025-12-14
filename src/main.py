from utils.ingestion import retriever, add_transcript_to_vectorstore
from utils.vectorstore import create_vectorstore, read_vectorstore
from utils.fetch_transcript import get_video_id, save_transcript_as_txt, read_transcript
from utils.yt_summarizer import q_and_a, summarizer
import os
    
VIDEO_URL= "https://www.youtube.com/watch?v=8tjb5OBAqRQ"

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
            


def url_to_vectorstore(video_url=VIDEO_URL):
    VIDEO_ID = get_video_id(video_url=video_url)

    if check_video_id(VIDEO_ID):
        print("[INFO] Video id have already found in database. ")
    else:
        print("[INFO] Video id was not found in video_id.txt file. It will be added to it.")
        save_transcript_as_txt(VIDEO_ID)
        print("[INFO] Transcript was saved as txt to transcript folder.")
        add_transcript_to_vectorstore(video_id=VIDEO_ID, vectorstore=VECTORSTORE)
        print("[INFO] Transcript was added to vectorstore as document.")

    return VIDEO_ID

def q_answer(question):

    answer = q_and_a(question=question, retriever=retriever(vectorstore=VECTORSTORE))

    return answer


def summary(transcript):
    return summarizer(transcript)


if __name__ == "__main__":
    
    VIDEO_ID = url_to_vectorstore(video_url=VIDEO_URL)
    
    transcript = read_transcript(video_id=VIDEO_ID)
    summary = summary(transcript)
    print("Summary: ", summary)

    user_question = input("> ")

    answer = q_answer(question=user_question)
    print(answer)

    

