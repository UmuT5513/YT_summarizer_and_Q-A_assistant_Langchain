from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
from models import Channel, Video
    

def get_video_metadata(video_url):
    '''get video metadata from youtube
    
    
    Returns:

        dict: video metadata(id,title, duration, language, channel_id, channel_name, upload_date)
    
    '''
    ydl_opts = {'quiet': True, 'no_warnings': True}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        
        return {
            'video_id': info['id'],
            'video_title': info['title'],
            'duration_seconds': info['duration'],
            'language': info.get('language', 'unknown'),
            'channel_id': info['channel_id'],
            'channel_name': info['uploader'],
            'upload_date': info['upload_date']
        }


def fetch_transcript_yt(video_id):
    '''fetch transcript from youtube by video id in only Turkish language'''
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id=video_id)
    transcript = transcript_list.find_transcript(language_codes=['tr']).fetch()

    formatter = TextFormatter()
    transcript_formatted = formatter.format_transcript(transcript)

    return transcript_formatted

def save_transcript_as_txt(video_id)-> str | None:
    """Fetch the related video from youtube by video id. And save it a txt file.

    Returns:

            transcript: str = A video transcript

    """
    transcript = fetch_transcript_yt(video_id=video_id)

    try:
        with open(f"./transcripts/transcript_{video_id}.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
    except FileExistsError:
        pass

    # log video_ids
    with open("video_id.txt", "a") as f:
        f.write(f"{video_id}\n")
    

    return str(transcript)



def read_transcript(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            transcript = f.read().strip()
            
            if not transcript:
                
                return "Transcript file is empty or contains only whitespace."
            
            return transcript
        
    except FileNotFoundError:
        return "Transcript file not found."
    


def store_metadata(metadata, db, video_url):
    """Fetch metadata from YouTube and store in database"""
    
    video_id = metadata['video_id']
    channel_id = metadata['channel_id']
    channel_name = metadata['channel_name']
    
    # Check if channel exists, if not create it
    
    channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if not channel:
        channel = Channel(
            channel_id=channel_id, 
            channel_name=channel_name
        )
        db.add(channel)
        db.commit()
    
        
    # Get transcript word count and save it.
    transcript = read_transcript(video_id=video_id)
    word_count = len(transcript.split())
    
    # Save transcript to file
    transcript_file_path = f"./transcripts/transcript_{video_id}.txt"
    with open(transcript_file_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    
    # Create and store video record
    video = Video(
        video_id=video_id,
        video_url=video_url,
        video_title=metadata['video_title'],
        transcript_file_path=transcript_file_path,
        duration_seconds=metadata['duration_seconds'],
        language=metadata['language'],
        transcript_word_count=word_count,
        status='fetched',
        channel_id=channel_id
    )
    db.add(video)
    db.commit()
    
    return video


    








