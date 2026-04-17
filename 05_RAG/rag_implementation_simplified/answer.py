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

def fetch_context(question: str) -> list[Document]:
    """
    Retrieves relevant document fragments from the vector store based on a provided query.

    Args:question (str): The user query or search string.

    Returns:list[Document]: A list containing the top k most relevant Document objects, where k is defined by RETRIEVAL_K.
    """
    return retriever.invoke(question, k= RETRIEVAL_K)

def combined_question(question: str, history: list[dict]= []) -> str:
    """
    Concatenates the current query with previous user messages from the conversation history to create a contextually enriched prompt.

    Args:
    question (str): The current user inquiry.
    history (list[dict]): A list of message dictionaries containing 'role' and 'content' keys. Defaults to an empty list.

    Returns:
    str: A single string merging past user inputs and the new question, separated by newlines.
    """

    prior = '\n'.join(m['content'] for m in history if m['role'] == 'user')
    return prior + '\n' + question