import os
import glob
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Constants:
MODEL = 'gpt-4.1-nano'
DB_NAME = str(Path(__file__).parent.parent / 'vector_db')
KNOWLEDGE_BASE = str(Path(__file__).parent.parent / 'knowledge-base')

