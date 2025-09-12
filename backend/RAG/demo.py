"""
Demo script for the RAG model
"""
import os
import sys
from rag_model import SimpleLegalRAG, convert_pdf_to_text

def main():
    """Main function to demonstrate RAG model usage."""
    print("=" * 50)
    print("SIMPLIFIED LEGAL DOCUMENT ANALYSIS DEMO")
    print("=" * 50)
    
    # Get paths to PDF files in the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_files = [
        os.path.join(current_dir, "law1.pdf"),
        os.path.join(current_dir, "The_Delhi_Rent_Act_1995.PDF")
    ]
    
    # Check if files exist
    for file_path in pdf_files:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return
    
    # Convert PDFs to text (simulated)
    for pdf_path in pdf_files:
        convert_pdf_to_text(pdf_path)
    
    print("\nInitializing Legal Document Analysis system...")
    
    try:
        # Initialize the RAG model
        rag = SimpleLegalRAG(pdf_files)
        
        # Example query (this would come from OCR in a real scenario)
        print("\nPROCESSING SAMPLE QUERY:")
        query = """
        I am a tenant in Delhi and my landlord is asking me to vacate the premises
        with only 15 days notice. He has also increased the rent by 50% last month.
        I've been living there for 3 years with a proper rental agreement.
        What are my legal rights in this situation?
        """
        print(query)
        
        print("\nANALYZING...")
        result = rag.analyze_text(query)
        
        print("\n=== Analysis Result ===")
        print(result["answer"])
        
        print("\n=== Sources ===")
        for source in result["sources"]:
            print(f"- {source['file']}, Page {source['page']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\nDEMO COMPLETE")

if __name__ == "__main__":
    main()
