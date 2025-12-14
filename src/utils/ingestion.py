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
    loader = TextLoader(f"./transcripts/transcript_{video_id}.txt")
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


    

def retriever(vectorstore):
    '''
    Parametres:

                vectorstore: Chroma tipinde bir vector store
                
    Returns:
    
                retriever: a vectore store retriever
    '''
   
    print("[INFO] Retriever is searching in vectorstore...")
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # -- example
    #answer_from_retriever=retriever.invoke("Altay cem meriç in anlattığı yayın evi sahibi adam nasıl zoom toplantısı elde etmiş?")
    #print(answer_from_retriever)
    #print(len(answer_from_retriever[0].page_content))
    #context_text="\n\n".join(doc.page_content for doc in answer_from_retriever)
    #print(context_text)

    return retriever

