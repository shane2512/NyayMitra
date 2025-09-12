"""
Simplified RAG Model for Legal Document Analysis
This implementation uses basic Python without external ML libraries
"""

import os
import re
import logging
from typing import List, Dict, Any
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleLegalRAG:
    """
    A simplified implementation of a RAG system for legal document analysis.
    This class provides basic document retrieval functionality.
    """
    
    def __init__(self, pdf_paths: List[str]):
        """
        Initialize the RAG model with paths to PDF files.
        
        Args:
            pdf_paths: List of paths to PDF documents that serve as knowledge base
        """
        self.pdf_paths = pdf_paths
        self.documents = []
        
        # Check if PDFs exist
        for path in pdf_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"PDF file not found: {path}")
        
        # Initialize the system
        self._load_documents()
    
    def _load_documents(self):
        """
        Simple document loader that reads text files created from PDFs.
        For actual PDF processing, you'd use a library like PyPDF2 or pdfplumber.
        """
        logger.info("Loading documents...")
        
        for pdf_path in self.pdf_paths:
            # Get the base name without extension
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            # Check if there's a corresponding text file
            txt_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}.txt")
            
            # If no text version exists, create a placeholder message
            if not os.path.exists(txt_path):
                logger.warning(f"No text version found for {pdf_path}. Creating placeholder.")
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"[This is placeholder text for {base_name}]\n")
                    f.write("In a real implementation, this would contain the extracted text from the PDF.\n")
                    f.write("For demo purposes, we're simulating some legal content:\n\n")
                    
                    # Add some simulated legal content based on the filename
                    if "rent" in base_name.lower():
                        f.write("Section 1: Protection of Tenants\n")
                        f.write("The landlord shall provide at least 30 days notice before any rent increase.\n")
                        f.write("Rent increases are limited to 10% per year unless otherwise specified.\n\n")
                        f.write("Section 2: Eviction Procedures\n")
                        f.write("A minimum of 90 days notice must be provided for eviction without cause.\n")
                        f.write("Tenants must be given written notice with specific reasons for eviction.\n\n")
                    else:
                        f.write("General Legal Provisions\n")
                        f.write("All parties must adhere to the procedures outlined in this document.\n")
                        f.write("Violations may result in legal penalties as described in Section 15.\n\n")
            
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split the content into paragraphs
                paragraphs = [p for p in content.split('\n\n') if p.strip()]
                
                # Add each paragraph as a document with metadata
                for i, para in enumerate(paragraphs):
                    self.documents.append({
                        'content': para,
                        'metadata': {
                            'source_file': os.path.basename(pdf_path),
                            'paragraph': i,
                            'page': i // 3 + 1  # Simulate page numbers (3 paragraphs per page)
                        }
                    })
                
                logger.info(f"Successfully loaded {len(paragraphs)} paragraphs from {txt_path}")
            except Exception as e:
                logger.error(f"Error loading {txt_path}: {str(e)}")
                raise
        
        logger.info(f"Document processing complete. Created {len(self.documents)} chunks.")
    
    def _simple_keyword_match(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        A simple keyword matching algorithm.
        In a real implementation, this would use vector embeddings and semantic search.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            
        Returns:
            List of matching documents with scores
        """
        # Extract keywords from the query
        keywords = set(re.findall(r'\b\w{3,}\b', query.lower()))
        
        results = []
        for doc in self.documents:
            content = doc['content'].lower()
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in content)
            if matches > 0:
                results.append({
                    'document': doc,
                    'score': matches / len(keywords) if keywords else 0
                })
        
        # Sort by score (descending) and take top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def analyze_text(self, query_text: str) -> Dict[str, Any]:
        """
        Analyze the input text against legal documents.
        
        Args:
            query_text: The input text to analyze (e.g., OCR output from a letter)
            
        Returns:
            A dictionary containing the retrieved documents and analysis
        """
        logger.info(f"Analyzing text: {query_text[:100]}...")
        
        try:
            # Find relevant documents
            matches = self._simple_keyword_match(query_text)
            
            # Extract source information and content
            sources = []
            content_extracts = []
            
            for match in matches:
                doc = match['document']
                sources.append({
                    "file": doc['metadata'].get("source_file", "Unknown"),
                    "page": doc['metadata'].get("page", "Unknown"),
                })
                content_extracts.append(doc['content'])
            
            # Simple analysis based on retrieved documents
            answer = "Based on the legal documents, the following sections may be relevant:\n\n"
            
            for i, extract in enumerate(content_extracts):
                section_match = re.search(r'Section (\d+):', extract)
                section_num = section_match.group(1) if section_match else "N/A"
                
                answer += f"{i+1}. From {sources[i]['file']} (Page {sources[i]['page']}): "
                answer += f"Section {section_num}\n"
                answer += f"   Relevance: This section discusses {self._get_topic(extract)}\n\n"
            
            response = {
                "answer": answer,
                "sources": sources
            }
            
            logger.info("Analysis complete.")
            return response
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise
    
    def _get_topic(self, text: str) -> str:
        """Extract a topic description from the text."""
        # Try to find a key phrase or first sentence
        first_sentence = re.match(r'^([^.!?]+[.!?])', text.strip())
        if first_sentence:
            return first_sentence.group(1)
        
        # If no clear first sentence, return a substring
        if len(text) > 60:
            return text[:60] + "..."
        return text


# Helper function to convert PDF to text (placeholder)
def convert_pdf_to_text(pdf_path: str, output_path: str = None):
    """
    Convert a PDF file to text (simplified implementation).
    In a real app, you would use a proper PDF extraction library.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path to save the text file (if None, use the same name with .txt extension)
    """
    if output_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_path = base_name + '.txt'
    
    logger.info(f"Converting {pdf_path} to {output_path}")
    
    # This is a placeholder - in a real application, you'd use a PDF parsing library
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Converted text from {os.path.basename(pdf_path)}\n\n")
        
        # Generate some fake content based on the filename
        if "rent" in pdf_path.lower() or "delhi" in pdf_path.lower():
            f.write("THE DELHI RENT CONTROL ACT\n\n")
            
            f.write("Section 1: Short Title and Commencement\n")
            f.write("This Act may be called the Delhi Rent Control Act, 1995.\n")
            f.write("It extends to the areas under the jurisdiction of the Delhi Municipal Corporation.\n\n")
            
            f.write("Section 2: Definitions\n")
            f.write("In this Act, unless the context otherwise requires:\n")
            f.write("(a) 'Landlord' means any person who receives rent in respect of any premises.\n")
            f.write("(b) 'Tenant' means any person who pays rent for any premises.\n\n")
            
            f.write("Section 3: Rent Increases\n")
            f.write("No landlord shall increase the rent of any premises by more than 10% annually.\n")
            f.write("Any increase in rent shall require a written notice of at least 30 days.\n\n")
            
            f.write("Section 4: Eviction of Tenants\n")
            f.write("No tenant shall be evicted except in accordance with the provisions of this Act.\n")
            f.write("The landlord must provide at least 90 days notice for eviction without cause.\n\n")
            
            f.write("Section 5: Maintenance and Repairs\n")
            f.write("The landlord shall be responsible for all major repairs to the premises.\n")
            f.write("The tenant shall be responsible for minor day-to-day maintenance.\n\n")
        else:
            f.write("GENERAL LEGAL DOCUMENT\n\n")
            
            f.write("Section 1: General Provisions\n")
            f.write("This document outlines the legal framework applicable to all parties.\n\n")
            
            f.write("Section 2: Compliance Requirements\n")
            f.write("All parties must adhere to the procedures outlined herein.\n\n")
            
            f.write("Section 3: Enforcement\n")
            f.write("Violations may result in legal penalties as described in Section 15.\n\n")
    
    logger.info(f"Conversion complete (simulated)")
    return output_path
