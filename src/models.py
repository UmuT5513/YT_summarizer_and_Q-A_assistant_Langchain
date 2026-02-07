from database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship




class Channel(Base):
    __tablename__ = "Channel"
    __table_args__ = {'extend_existing': True}

    channel_id = Column(String, primary_key=True, index=True, autoincrement=False) #unique id for each channel
    channel_name = Column(String, index=True, nullable=False) #name of the channel
    
    created_at = Column(DateTime(timezone=True), server_default=func.now()) #when channel was added to database

    videos = relationship('Video', back_populates='owner') #
    


class Video(Base):
    __tablename__ = "Video"
    __table_args__ = {'extend_existing': True}
    
    video_id = Column(String, primary_key=True, index=True, autoincrement=False) #unique id for each video can be fetched from youtube video url.
    
    video_url = Column(String, index=True, nullable=False) #url of the video
    video_title = Column(String, index=True, nullable=False) #title of the video
    transcript_file_path = Column(String, index=True, nullable=False) #path to the transcript txt file
    duration_seconds = Column(Integer, index=True, nullable=False) #duration of the video in seconds
    language = Column(String, index=True, nullable=False) #language of the transcript
    transcript_word_count = Column(Integer, index=True, nullable=False) #number of words in transcript
    fetched_at = Column(DateTime(timezone=True), server_default=func.now()) #when transcript was fetched
    status = Column(String, index=True, nullable=False) # e.g., 'fetched', 'processed', etc.
    
    channel_id = Column(Integer, ForeignKey('Channel.channel_id')) #foreign key to Channel table
    owner = relationship('Channel', back_populates='videos') # backpopulates parent class daki relationship dir.


print("""[INFO] Database tables is ok.""")