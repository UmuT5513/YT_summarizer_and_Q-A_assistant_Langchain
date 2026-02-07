# vector database
from langchain_text_splitters import RecursiveCharacterTextSplitter

# document laoder
from langchain_community.document_loaders import TextLoader


# environment
from dotenv import load_dotenv
import os


load_dotenv()

def load_documents(video_id):
    '''convert txt file to langchain documents'''
    loader = TextLoader(f"./transcripts/transcript_{video_id}.txt", encoding="utf-8")
    video_document = loader.load()
    return video_document


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splitted_docs=splitter.split_documents(documents)
    return splitted_docs



def add_transcript_to_vectorstore(video_id, vectorstore ,collection_name="youtube_summarizer"):

    documents = load_documents(video_id=video_id)

    splitted_documents = split_documents(documents=documents)

    vectorstore.add_documents(documents=splitted_documents, collection_name=collection_name)










