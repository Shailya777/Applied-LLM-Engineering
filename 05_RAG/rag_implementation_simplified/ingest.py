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
embeddings = OpenAIEmbeddings(model= 'text-embedding-3-large')

def fetch_documents():
    """
    Iterates through subdirectories in the knowledge base,
    loads Markdown files using a DirectoryLoader,
    and tags each document with its source folder name as a metadata attribute.

    Returns:
    list: A list of Document objects,
    each containing the file content and updated metadata including 'doc_type'.
    """
    folders = str(Path(KNOWLEDGE_BASE) / '*')
    documents = []

    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(path= folder,
                                 glob= '**/*.md',
                                 loader_cls= TextLoader,
                                 loader_kwargs= {'encoding': 'utf-8'}
                                 )

        folder_docs = loader.load()

        for doc in folder_docs:
            doc.metadata['doc_type'] = doc_type
            documents.append(doc)

    return documents