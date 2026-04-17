from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
from dotenv import load_dotenv

# Constants:
load_dotenv()
MODEL= 'gpt-4.1-nano'
DB_NAME= str(Path(__file__).parent.parent / 'vector_db')
embeddings= OpenAIEmbeddings(model= 'text_embedding-3-large')
RETRIEVAL_K = 10