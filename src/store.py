"""Acesso ao banco vetorial."""
import os

import chromadb
from chromadb.utils import embedding_functions

MODELO_EMBEDDING = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def colecao():
    client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", ".chroma"))
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODELO_EMBEDDING)
    return client.get_or_create_collection("documentos", embedding_function=ef, metadata={"hnsw:space": "cosine"})
