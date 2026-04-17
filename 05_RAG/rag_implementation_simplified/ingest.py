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
load_dotenv()
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
    folders = glob.glob(str(Path(KNOWLEDGE_BASE) / '*'))
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

def create_chunks(documents):
    """
    Splits a list of documents into smaller, overlapping chunks using recursive character splitting to maintain semantic context.

    Args:
    documents (list): A list of Document objects to be processed.

    Returns:
    list: A list of Document chunks, each with a maximum size of 500 characters and a 200-character overlap.
    """

    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap= 200)
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_embeddings(chunks):
    """
    Generates and stores vector embeddings for text chunks in a persistent Chroma database, replacing any existing collection.

    Args:
    chunks (list): A list of Document chunks to be vectorized.

    Returns:
    None: The function persists the data to the directory specified by DB_NAME and prints the total vector count and embedding dimensionality.
    """

    if os.path.exists(DB_NAME):
        Chroma(persist_directory= DB_NAME, embedding_function=  embeddings).delete_collection()

    vectorstore = Chroma.from_documents(
        documents= chunks,
        embedding= embeddings,
        persist_directory= DB_NAME
    )

    collection = vectorstore._collection
    count = collection.count()

    sample_embedding = collection.get(limit= 1, include= ['embeddings'])['embeddings'][0]
    dimensions = len(sample_embedding)
    print(f'There are {count} Vectors with {dimensions} Dimensions in Vector Store.')


if __name__ == '__main__':
    documents = fetch_documents()
    chunks = create_chunks(documents)
    create_embeddings(chunks)
    print('Data Ingestion Completed Successfully.!')