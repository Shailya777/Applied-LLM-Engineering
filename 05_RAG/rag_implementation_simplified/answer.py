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

SYSTEM_PROMPT= """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

vectorstore = Chroma(persist_directory= DB_NAME, embedding_function= embeddings)
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(temperature= 0, model= MODEL)