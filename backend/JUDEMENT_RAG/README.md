# Legal Judgment Analysis using RAG with Gemma 2B

A Retrieval-Augmented Generation (RAG) system that analyzes legal documents and identifies relevant precedents, citations, and laws based on OCR-scanned text input.

## Project Overview

This system analyzes text from letters or documents using a RAG approach:

1. **Document Processing**: Extracts text from legal judgment PDFs
2. **Chunking**: Splits the documents into logical segments
3. **Embedding**: Creates vector embeddings for efficient semantic search
4. **Retrieval**: Finds the most relevant legal content based on a query
5. **Generation**: Uses Gemma 2B to generate structured responses with case citations, precedents, and laws

## System Requirements

- Python 3.8 or higher
- 8+ GB RAM recommended
- GPU support optional but recommended for faster performance
- Hugging Face API token for Gemma 2B integration

## Installation

1. Clone this repository or download the files
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment:
   ```
   python setup_env.py --api_token YOUR_HUGGINGFACE_API_TOKEN
   ```
   *Note: If you don't have an API token, the system will run in simulated mode*

## Directory Structure

```
JUDEMENT_RAG/
  ├── data/               # Data files
  │   ├── raw/            # Raw PDF documents
  │   ├── processed/      # Processed text files
  │   ├── vector_store/   # Vector embeddings
  │   └── sample_input/   # Sample OCR input files
  │
  ├── src/                # Source code
  │   ├── document_loader.py    # PDF loading and processing
  │   ├── embedding_engine.py   # Vector embeddings and storage
  │   └── rag_engine.py         # RAG implementation with Gemma 2B
  │
  ├── demo.py             # Demo application
  ├── setup_env.py        # Environment setup utility
  ├── requirements.txt    # Python dependencies
  └── README.md           # Documentation
```

## Usage

### Running the Demo

The demo script provides a complete end-to-end example:

```bash
python demo.py
```

This will:
1. Load the legal judgment PDFs from `data/raw/`
2. Create vector embeddings and store them
3. Process a sample query from `data/sample_input/`
4. Generate a response with relevant legal information

### Using Your Own Input

To analyze your own OCR text:

```bash
python demo.py --query_file path/to/your/ocr_text.txt
```

### Rebuilding the Vector Store

To force rebuilding the vector store (e.g., after adding new documents):

```bash
python demo.py --rebuild
```

### More Accurate PDF Processing

For more accurate (but slower) PDF text extraction:

```bash
python demo.py --plumber
```

## Development Notes

### Simulated Mode

If no Hugging Face API token is provided, the system will run in simulated mode, which:
- Still performs document retrieval
- Uses pattern matching to extract potential legal references
- Doesn't use the actual Gemma 2B model

This is useful for testing the pipeline without incurring API costs.

### Adding New Documents

To add new legal judgments:
1. Place PDF files in the `data/raw/` directory
2. Run `python demo.py --rebuild` to recreate the vector store

## License

This project is provided for educational and research purposes only.

## Acknowledgments

- This project uses the Gemma 2B model from Google via Hugging Face
- Built with LangChain, sentence-transformers, and FAISS for the RAG pipeline