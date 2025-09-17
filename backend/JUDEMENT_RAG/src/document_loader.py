"""
PDF Document Loader Module

This module provides utilities to load and process PDF documents for the Legal Judgment RAG system.
It extracts text from PDF files and handles document metadata.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LegalDocumentLoader:
    """
    Class for loading and processing legal PDF documents.
    """
    
    def __init__(self, pdf_directory: str):
        """
        Initialize the document loader with a directory path containing PDFs.
        
        Args:
            pdf_directory: Path to the directory containing PDF documents
        """
        self.pdf_directory = Path(pdf_directory)
        if not os.path.exists(self.pdf_directory):
            raise FileNotFoundError(f"PDF directory not found: {pdf_directory}")
        
        self.pdf_files = self._get_pdf_files()
        logger.info(f"Found {len(self.pdf_files)} PDF files in {pdf_directory}")
    
    def _get_pdf_files(self) -> List[Path]:
        """
        Find all PDF files in the specified directory.
        
        Returns:
            List of paths to PDF files
        """
        return list(self.pdf_directory.glob("*.pdf"))
    
    def load_documents(self, use_plumber: bool = False) -> List[Document]:
        """
        Load all PDF documents from the directory.
        
        Args:
            use_plumber: Whether to use PDFPlumber (more accurate but slower) instead of PyPDF
            
        Returns:
            List of Document objects
        """
        all_documents = []
        
        for pdf_path in self.pdf_files:
            try:
                logger.info(f"Loading {pdf_path.name}...")
                
                # Choose loader based on parameter
                if use_plumber:
                    loader = PDFPlumberLoader(str(pdf_path))
                else:
                    loader = PyPDFLoader(str(pdf_path))
                
                # Load the document
                documents = loader.load()
                
                # Enhance metadata
                for doc in documents:
                    doc.metadata.update({
                        "source_file": pdf_path.name,
                        "file_path": str(pdf_path),
                        "document_type": "legal_judgment"
                    })
                
                all_documents.extend(documents)
                logger.info(f"Successfully loaded {len(documents)} pages from {pdf_path.name}")
            
            except Exception as e:
                logger.error(f"Error loading {pdf_path.name}: {str(e)}")
        
        return all_documents
    
    def extract_text_with_metadata(self) -> List[Dict[str, Any]]:
        """
        Extract text from PDF documents along with metadata.
        
        Returns:
            List of dictionaries containing text and metadata
        """
        documents = self.load_documents()
        
        result = []
        for doc in documents:
            result.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })
        
        return result

def chunk_documents(documents: List[Document], 
                    chunk_size: int = 1000,
                    chunk_overlap: int = 200) -> List[Document]:
    """
    Split documents into smaller chunks for better processing.
    
    Args:
        documents: List of Document objects to split
        chunk_size: Size of each chunk in characters
        chunk_overlap: Overlap between chunks in characters
        
    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunked_documents = text_splitter.split_documents(documents)
    
    logger.info(f"Split {len(documents)} documents into {len(chunked_documents)} chunks")
    return chunked_documents

def load_and_chunk_legal_documents(pdf_directory: str, 
                                  chunk_size: int = 1000,
                                  chunk_overlap: int = 200,
                                  use_plumber: bool = False) -> List[Document]:
    """
    Convenience function to load PDFs and chunk them in one step.
    
    Args:
        pdf_directory: Path to the directory containing PDF documents
        chunk_size: Size of each chunk in characters
        chunk_overlap: Overlap between chunks in characters
        use_plumber: Whether to use PDFPlumber instead of PyPDF
        
    Returns:
        List of chunked Document objects
    """
    loader = LegalDocumentLoader(pdf_directory)
    documents = loader.load_documents(use_plumber=use_plumber)
    return chunk_documents(documents, chunk_size, chunk_overlap)


if __name__ == "__main__":
    """
    Simple test for the document loader.
    """
    import sys
    
    if len(sys.argv) > 1:
        pdf_dir = sys.argv[1]
    else:
        # Use default directory for testing
        pdf_dir = "../data/raw"
    
    loader = LegalDocumentLoader(pdf_dir)
    docs = loader.load_documents()
    
    print(f"Loaded {len(docs)} document pages")
    if docs:
        print("Sample content from first page:")
        print(docs[0].page_content[:500] + "...")
        print("\nMetadata:", docs[0].metadata)
        
        chunked_docs = chunk_documents(docs)
        print(f"\nChunked into {len(chunked_docs)} segments")
        print("Sample chunk:")
        print(chunked_docs[0].page_content[:300] + "...")