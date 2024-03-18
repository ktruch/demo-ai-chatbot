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
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from schemas import QuestionRequest
from dotenv import load_dotenv
load_dotenv()
llm = OpenAI()

router = APIRouter(prefix="/confluenceWiki")

# @router.get("/list", response_model=schemas.ConfluenceResponse)
@router.get("/list")
def get_confluenceTitles():
    return crudConfluence.getListContent()

@router.get("/list/article")
def get_ArticleList(content_id:int):
    return crudConfluence.getArticle(content_id)