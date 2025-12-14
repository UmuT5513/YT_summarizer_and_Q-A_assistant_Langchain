

# model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser, JsonOutputParser
from langchain_core.messages import SystemMessage

# environment
from dotenv import load_dotenv
import os


#Schema
from pydantic import BaseModel, Field

load_dotenv()



def q_and_a(question, retriever):
    """
    Temel akış:

        Question a göre vectordatabase den *similar* metinleri alır.

        Aldığı metinleri llm e *bu metinlerden bir özet çıkar* diye gönderir. llm bu metinlerle beraber question u da parametre olarak alır.
        llm bu metinleri ve question u kullanarak cevap verir.

        Sonuc: 
        
        DB deki tüm metinleri llm e vermek yerine ilgili metinleri vererek api maliyetini azaltıyoruz.
        
        
    Parametres:
        
            question: str 
            retriever: langchain_retriever from ingestion.py


    Returns:

            answer: str = llm cevabı
        
    """

    parser=StrOutputParser()

    # step 3: model 
    model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0, model="gpt-4o-mini")

    prompt = PromptTemplate(
        template="""you have 2 repsonsebility. One is to answer the {question} and the other is to generate a summary only for the {context}. If the answer is unsufficient for the question, reply with 'I don't know'. The answer must be in Turkish Language.""",
        input_variables=["context", "question"]
    )


    retrieved_informations = retriever.invoke(question)
    context_text="\n\n".join(doc.page_content for doc in retrieved_informations)

    # print("---DB den alınan metin: ", context_text)

    final_prompt = {"context":context_text, "question":question}

    # Step 4: Generation

    chain = prompt | model | parser
    answer = chain.invoke(final_prompt)

    return answer



class SummaryScheme(BaseModel):
    video_title: str = Field(description="The title of the video")
    summary: str = Field(description="Summary of the video")
    key_takeaways: str = Field(description="Key takeaways of the video")

def summarizer(transcript):
    

    model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0, model="gpt-4o-mini")

    model = model.with_structured_output(SummaryScheme)

    
    prompt = PromptTemplate(
        template=""""You are a summarizer. Summarize this text in the structure according to the text only: The text is {transcript}\n Give a title for the video, a summary which consists of 10-15 sentences with bullet points, and key takeaways.""",
        input_variables=["transcript"]
    )


    chain = prompt | model 

    summary = chain.invoke({"transcript": transcript})
    return summary





