# vector database
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# environment
from dotenv import load_dotenv
import os


load_dotenv()
EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-3-small")


def create_vectorstore():
    '''Creates vector store from given transcript.
    
    Parametres:
    
            transcript: str = It can only be one txt file. (for now)

    Returns:

            vectorstore: Chroma tipinde bir vector store
    '''

 
    vectorstore = Chroma(embedding_function=EMBEDDING_MODEL, 
                        collection_name="youtube_summarizer",
                        persist_directory="./.transcript_chroma")
    
    return vectorstore



def read_vectorstore():
    vectorstore = Chroma(embedding_function=EMBEDDING_MODEL, 
                        collection_name="youtube_summarizer",
                        persist_directory="./.transcript_chroma")
    
    return vectorstore





