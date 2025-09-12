"""
Utility for processing OCR text with the RAG model
"""
import argparse
import os
from rag_model import SimpleLegalRAG, convert_pdf_to_text

def process_ocr_text(text_file, pdf_files):
    """
    Process OCR text from a file and analyze it against legal documents.
    
    Args:
        text_file: Path to the file containing OCR text
        pdf_files: List of paths to PDF documents
    """
    # Read OCR text
    try:
        with open(text_file, "r", encoding="utf-8") as f:
            ocr_text = f.read()
    except Exception as e:
        print(f"Error reading OCR text file: {str(e)}")
        return
    
    # Convert PDFs to text (if needed)
    for pdf_path in pdf_files:
        pdf_txt_path = os.path.splitext(pdf_path)[0] + '.txt'
        if not os.path.exists(pdf_txt_path):
            convert_pdf_to_text(pdf_path)
    
    # Initialize the RAG model
    try:
        rag = SimpleLegalRAG(pdf_files)
        
        # Analyze the OCR text
        print(f"\nAnalyzing text from {os.path.basename(text_file)}...")
        result = rag.analyze_text(ocr_text)
        
        # Print the results
        print("\n=== Legal Analysis ===")
        print(result["answer"])
        
        print("\n=== Sources ===")
        for source in result["sources"]:
            print(f"- {source['file']}, Page {source['page']}")
            
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

def main():
    """Main function to parse command line arguments and run the processor."""
    parser = argparse.ArgumentParser(description="Process OCR text and analyze against legal documents.")
    
    parser.add_argument("text_file", help="Path to the file containing OCR text")
    parser.add_argument("--pdfs", nargs="+", help="Paths to the PDF documents to use as knowledge base")
    
    args = parser.parse_args()
    
    if args.pdfs:
        pdf_files = args.pdfs
    else:
        # Default to PDFs in the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_files = [
            os.path.join(current_dir, "law1.pdf"),
            os.path.join(current_dir, "The_Delhi_Rent_Act_1995.PDF")
        ]
    
    process_ocr_text(args.text_file, pdf_files)

if __name__ == "__main__":
    main()
