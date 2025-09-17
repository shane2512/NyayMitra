"""
Vector Embedding Module

This module provides functionality to convert text chunks into vector embeddings
and store them in a FAISS vector database for efficient retrieval.
"""

import os
import logging
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LegalEmbeddingEngine:
    """
    Class for managing document embeddings and vector storage for legal documents.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding engine with a specified model.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        
        # Determine device (use GPU if available)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Initialize the embedding model
        self.initialize_embeddings()
    
    def initialize_embeddings(self):
        """Initialize the embedding model"""
        try:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={"device": self.device}
            )
            logger.info(f"Embedding model {self.model_name} initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {str(e)}")
            raise
    
    def create_vector_store(self, documents: List[Document], save_path: Optional[str] = None) -> Any:
        """
        Create a vector store from a list of documents.
        
        Args:
            documents: List of Document objects
            save_path: Path to save the vector store (optional)
            
        Returns:
            FAISS vector store
        """
        logger.info(f"Creating vector store from {len(documents)} documents")
        
        try:
            # Create vector store
            vector_store = FAISS.from_documents(documents, self.embedding_model)
            
            # Save if path provided
            if save_path:
                self.save_vector_store(vector_store, save_path)
            
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def save_vector_store(self, vector_store: Any, save_path: str) -> None:
        """
        Save a vector store to disk.
        
        Args:
            vector_store: FAISS vector store
            save_path: Path to save the vector store
        """
        save_dir = Path(save_path)
        save_dir.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            vector_store.save_local(save_path)
            logger.info(f"Vector store saved to {save_path}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load_vector_store(self, load_path: str) -> Any:
        """
        Load a vector store from disk.
        
        Args:
            load_path: Path to load the vector store from
            
        Returns:
            FAISS vector store
        """
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Vector store path not found: {load_path}")
        
        try:
            vector_store = FAISS.load_local(load_path, self.embedding_model)
            logger.info(f"Vector store loaded from {load_path}")
            return vector_store
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise

def embed_legal_documents(documents: List[Document], 
                          vector_store_path: Optional[str] = None,
                          model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> Any:
    """
    Convenience function to embed documents and create a vector store.
    
    Args:
        documents: List of Document objects
        vector_store_path: Path to save the vector store (optional)
        model_name: Name of the embedding model to use
        
    Returns:
        FAISS vector store
    """
    embedding_engine = LegalEmbeddingEngine(model_name=model_name)
    return embedding_engine.create_vector_store(documents, vector_store_path)


if __name__ == "__main__":
    """
    Simple test for the embedding engine.
    """
    from document_loader import LegalDocumentLoader, chunk_documents
    import sys
    
    if len(sys.argv) > 1:
        pdf_dir = sys.argv[1]
        vector_store_path = sys.argv[2] if len(sys.argv) > 2 else "../data/vector_store"
    else:
        # Use default directories for testing
        pdf_dir = "../data/raw"
        vector_store_path = "../data/vector_store"
    
    # Load and chunk documents
    loader = LegalDocumentLoader(pdf_dir)
    documents = loader.load_documents()
    chunked_docs = chunk_documents(documents)
    
    # Create and save vector store
    embedding_engine = LegalEmbeddingEngine()
    vector_store = embedding_engine.create_vector_store(chunked_docs, vector_store_path)
    
    print(f"Created vector store with {len(chunked_docs)} chunks")
    print(f"Saved to {vector_store_path}")
    
    # Test similarity search
    if chunked_docs:
        test_query = "legal precedent regarding property rights"
        results = vector_store.similarity_search(test_query, k=2)
        
        print("\nTest query:", test_query)
        print(f"Found {len(results)} relevant documents")
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Source: {doc.metadata.get('source_file', 'Unknown')}, Page: {doc.metadata.get('page', 'Unknown')}")
            print(doc.page_content[:300] + "...")