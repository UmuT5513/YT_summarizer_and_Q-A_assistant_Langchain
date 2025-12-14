from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

    
def get_video_id(video_url):

    video_id = str(video_url).split('=')[1]

    if '&' in video_id:
        video_id = video_id.split('&')[0]

    return video_id

def save_transcript_as_txt(video_id)-> str | None:
    """Fetch the related video from youtube by video id. And save it a txt file.

    Returns:

            transcript: str = A video transcript

    """
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id=video_id)
    transcript = transcript_list.find_transcript(language_codes=['tr']).fetch()

    formatter = TextFormatter()
    transcript_formatted = formatter.format_transcript(transcript)

    try:
        with open(f"./transcripts/transcript_{video_id}.txt", "w") as f:
            f.write(transcript_formatted)
    except FileExistsError:
        pass

    # log video_ids
    with open("video_id.txt", "a") as f:
        f.write(f"{video_id}\n")
    

    return str(transcript_formatted)



def read_transcript(video_id):
    try:
        with open(f"./transcripts/transcript_{video_id}.txt", "r", encoding="utf-8") as f:
            transcript = f.read().strip()
            
            if not transcript:
                
                return "Transcript file is empty or contains only whitespace."
            
            return transcript
        
    except FileNotFoundError:
        return "Transcript file not found."

    








