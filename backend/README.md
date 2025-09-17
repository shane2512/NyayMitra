# NyayMitra Backend

NyayMitra is an AI-powered legal assistant that demystifies legal documents clause by clause, helping users understand complex legal language and providing insights from relevant case law and precedents.

## Overview

The backend system consists of several key components that work together:

### 1. Legal Judgment RAG (JUDEMENT_RAG/)

A Retrieval-Augmented Generation (RAG) system that analyzes legal documents and identifies relevant precedents, citations, and laws. See the [RAG README](./JUDEMENT_RAG/README.md) for more details.

### 2. Assistant (assistant.py)

The main interface for user interactions, routing queries to the appropriate subsystems.

### 3. Server (complete_server_side.py)

The API server that handles HTTP requests from the frontend.

### 4. PDF Processor (pdf_processor.py)

Utility for processing and extracting text from PDF documents.

## Setup and Installation

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables (for the RAG subsystem):
   ```
   python JUDEMENT_RAG/setup_env.py --api_token YOUR_HUGGINGFACE_API_TOKEN
   ```

4. Run the server:
   ```
   python complete_server_side.py
   ```

## Usage

Once the server is running, it will listen for requests on the configured port (default: 5000). The frontend can connect to this server to access the NyayMitra services.

### API Endpoints

- `POST /query`: Submit a legal query for analysis
  - Request body: `{"query": "your legal question here"}`
  - Response: Analysis with relevant legal information

- `POST /upload_document`: Upload a PDF document for analysis
  - Uses multipart/form-data with a "file" field containing the PDF

## Development

To add more legal documents to the RAG system:

1. Place PDF files in `JUDEMENT_RAG/data/raw/`
2. Run `python JUDEMENT_RAG/demo.py --rebuild` to update the vector store
