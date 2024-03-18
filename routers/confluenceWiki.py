from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import schemas
import crudConfluence

# Necessary imports for langchain summarization
from langchain_community.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

# Necessary imports to chat with a PDF file
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Replicate
from schemas import QuestionRequest
from dotenv import load_dotenv
import os

load_dotenv()

# llmOpenAI = OpenAI()

replicate_api_token = os.environ['REPLICATE_API_TOKEN']
replicate_id = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"
llm = Replicate(
    model=replicate_id,
    input={"temperature": 0.01,
            "max_length": 500,
            "top_p": 1})

router = APIRouter(prefix="/confluenceWiki")

# @router.get("/list", response_model=schemas.ConfluenceResponse)
@router.get("/list")
def get_confluenceTitles():
    return crudConfluence.getListContent()

@router.get("/list/article")
def get_ArticleList(content_id:int):
    return crudConfluence.getArticle(content_id)

# LANGCHAIN
# langchain_llm = OpenAI(temperature=0)
langchain_llm = Replicate(
    model=replicate_id,
    input={"temperature": 0.01,
            "max_length": 500,
            "top_p": 1})

summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)

@router.post('/summarize-text')
async def summarize_text(id:int):
    text = crudConfluence.getArticle(id)
    summary = summarize_chain.run(text=text)
    return {'summary': summary}


# Ask a question about one PDF file
@router.post("/question-to-ai/{id}")
def question_to_ai(id: int, question_request: str):
    article = crudConfluence.getArticle(id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    document_chunks = split_documents(article)
    embeddings = LlamaCppEmbeddings(model_path="model.bin")
    stored_embeddings = FAISS.from_texts(document_chunks, embeddings)
    QA_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=stored_embeddings.as_retriever())
    question = question_request.question
    answer = QA_chain.run(question)
    return answer

def split_documents(article_text: str):
    document_chunks = []
    chunk_size = 3000
    chunk_overlap = 400
    for i in range(0, len(article_text), chunk_size - chunk_overlap):
        chunk = article_text[i:i + chunk_size]
        document_chunks.append(chunk)
    return document_chunks