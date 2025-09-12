from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.moderator import ModeratorAgent
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'pdf'}
API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyD3W4JSQzZ8nGyqxf-LWP_jtpi25ofX-gE')

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize moderator
moderator = ModeratorAgent(API_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze():
    print("=== ANALYZE ENDPOINT CALLED ===")
    print(f"Request files: {request.files}")
    print(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        print("ERROR: No file part in request")
        return jsonify({"error": "No file part", "status": "error"}), 400

    file = request.files['file']
    print(f"File object: {file}")
    print(f"Filename: {file.filename}")
    print(f"Content type: {file.content_type}")
    
    if file.filename == '':
        print("ERROR: No filename provided")
        return jsonify({"error": "No selected file", "status": "error"}), 400

    if not allowed_file(file.filename):
        print(f"ERROR: File type not allowed: {file.filename}")
        return jsonify({"error": "Only PDF files are allowed", "status": "error"}), 400

    try:
        # Save the uploaded PDF temporarily
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        # Use absolute path to avoid issues with relative paths
        pdf_path = os.path.abspath(pdf_path)
        print(f"Saving file to: {pdf_path}")
        
        file.save(pdf_path)
        
        # Check file size after saving
        file_size = os.path.getsize(pdf_path)
        print(f"Saved file size: {file_size} bytes")
        
        if file_size == 0:
            print("ERROR: File size is 0 bytes")
            return jsonify({"error": "File is empty", "status": "error"}), 400

        # Use the Moderator Agent to analyze the contract
        print("Starting analysis...")
        result = moderator.analyze_contract(pdf_path)
        print(f"Analysis result: {result}")

        # Clean up temporary file
        os.remove(pdf_path)
        print("Temporary file cleaned up")

        return jsonify(result)
    except Exception as e:
        print(f"ERROR in analyze endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "NyayMitra API Server is running!", "version": "1.0", "endpoints": ["/health", "/analyze"]})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)