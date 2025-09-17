"""
Demo Application for Legal Judgment RAG System

This script demonstrates the complete pipeline of the legal judgment RAG system:
1. Loading and processing PDF documents
2. Creating vector embeddings
3. Setting up the RAG engine
4. Processing sample OCR queries
"""

import os
import logging
import argparse
from pathlib import Path
import importlib.util
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the current directory to sys.path to help with imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Check for dotenv and import it if available
if importlib.util.find_spec("dotenv") is not None:
    from dotenv import load_dotenv
    load_dotenv()
else:
    print("Warning: python-dotenv not installed. Environment variables will not be loaded.")

def setup_directories(base_dir: str = "..") -> dict:
    """
    Set up the directory structure for the demo.
    
    Args:
        base_dir: Base directory for the project
        
    Returns:
        Dictionary of directory paths
    """
    base_path = Path(base_dir)
    
    dirs = {
        "raw": base_path / "data" / "raw",
        "processed": base_path / "data" / "processed",
        "vector_store": base_path / "data" / "vector_store",
        "sample_input": base_path / "data" / "sample_input"
    }
    
    # Ensure directories exist
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        
    return dirs

def load_and_process_documents(raw_dir: str, use_plumber: bool = False):
    """
    Load and process the legal judgment PDFs.
    
    Args:
        raw_dir: Directory containing the raw PDF files
        use_plumber: Whether to use PDFPlumber for more accurate extraction
        
    Returns:
        List of chunked documents
    """
    from src.document_loader import load_and_chunk_legal_documents
    
    logger.info("Loading and processing documents...")
    documents = load_and_chunk_legal_documents(
        raw_dir, 
        chunk_size=1000,
        chunk_overlap=200,
        use_plumber=use_plumber
    )
    
    logger.info(f"Processed {len(documents)} document chunks")
    return documents

def create_embeddings(documents, vector_store_dir: str):
    """
    Create vector embeddings for the documents.
    
    Args:
        documents: List of document chunks
        vector_store_dir: Directory to save the vector store
        
    Returns:
        Path to the saved vector store
    """
    from src.embedding_engine import embed_legal_documents
    
    logger.info("Creating document embeddings...")
    vector_store = embed_legal_documents(documents, vector_store_dir)
    
    return vector_store_dir

def create_sample_ocr_input(sample_dir: str):
    """
    Create a sample OCR input file for testing.
    
    Args:
        sample_dir: Directory to save the sample input
    """
    sample_path = Path(sample_dir) / "sample_query.txt"
    
    # Skip if file already exists
    if sample_path.exists():
        logger.info(f"Sample OCR input file already exists at {sample_path}")
        return sample_path
    
    logger.info(f"Creating sample OCR input file at {sample_path}")
    
    sample_text = """
    LEGAL CONSULTATION REQUEST
    
    Date: September 15, 2025
    
    To: Legal Aid Society
    
    I am writing to seek advice regarding a property dispute I'm currently involved in. My neighbor has constructed a wall that encroaches approximately 2 feet onto my property according to the land survey and property deed. The wall was constructed 3 months ago without my consent or any consultation.
    
    When I approached my neighbor about this issue, they claimed that they had been using that portion of land for over 15 years (though I've only owned the property for 5 years) and therefore had acquired rights to it. They mentioned something about "adverse possession" and "prescriptive easements" but I'm not sure if these concepts apply in this situation.
    
    I have the following questions:
    
    1. What legal rights do I have to have the encroaching wall removed?
    2. Is there any validity to my neighbor's claim of adverse possession?
    3. What documentation should I gather to support my case?
    4. What is the statute of limitations for this type of property dispute?
    
    I would appreciate any guidance or references to relevant legal precedents that might apply to my situation.
    
    Thank you for your assistance.
    
    Sincerely,
    James Wilson
    """
    
    with open(sample_path, "w") as f:
        f.write(sample_text.strip())
    
    return sample_path

def process_query(vector_store_dir: str, query_file: str = None, query_text: str = None):
    """
    Process a query against the legal judgments.
    
    Args:
        vector_store_dir: Directory containing the vector store
        query_file: Path to a file containing the query text
        query_text: Direct query text (used if query_file is None)
        
    Returns:
        Analysis results
    """
    from src.rag_engine import create_rag_engine
    
    # Get query text
    if query_text is None:
        if query_file is None:
            raise ValueError("Either query_file or query_text must be provided")
        
        with open(query_file, "r") as f:
            query_text = f.read()
    
    # Initialize RAG engine
    logger.info("Initializing RAG engine...")
    rag_engine = create_rag_engine(vector_store_dir)
    
    # Process the query
    logger.info("Processing query...")
    result = rag_engine.analyze_query(query_text)
    
    return result

def run_pipeline(args):
    """
    Run the complete RAG pipeline.
    
    Args:
        args: Command line arguments
    """
    # Set up directories
    dirs = setup_directories()
    
    # If vector store already exists and we're not forced to rebuild, skip to query processing
    if Path(dirs["vector_store"]).exists() and not args.rebuild:
        logger.info("Using existing vector store")
    else:
        # Load and process documents
        documents = load_and_process_documents(dirs["raw"], use_plumber=args.plumber)
        
        # Create embeddings
        create_embeddings(documents, dirs["vector_store"])
    
    # Create sample input if needed
    if not args.query_file:
        sample_file = create_sample_ocr_input(dirs["sample_input"])
        args.query_file = sample_file
    
    # Process the query
    result = process_query(dirs["vector_store"], args.query_file)
    
    # Display results
    print("\n" + "="*50)
    print("LEGAL JUDGMENT ANALYSIS RESULTS")
    print("="*50 + "\n")
    
    if args.query_file:
        print(f"Query from file: {args.query_file}")
    
    print("\nANALYSIS:")
    print(result["analysis"])
    
    print("\nSOURCES:")
    for source in result["sources"]:
        print(f"- {source['file']}, Page {source['page']}")
    
    print("\n" + "="*50)

def main():
    """Main function to run the demo"""
    parser = argparse.ArgumentParser(
        description="Demo for Legal Judgment RAG System"
    )
    
    parser.add_argument(
        "--query_file", 
        type=str,
        help="Path to a file containing OCR text to analyze"
    )
    
    parser.add_argument(
        "--rebuild", 
        action="store_true",
        help="Force rebuilding the vector store even if it already exists"
    )
    
    parser.add_argument(
        "--plumber", 
        action="store_true",
        help="Use PDFPlumber for more accurate PDF extraction (slower)"
    )
    
    args = parser.parse_args()
    
    try:
        run_pipeline(args)
    except Exception as e:
        logger.error(f"Error in pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()