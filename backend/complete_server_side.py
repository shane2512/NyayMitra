# app.py
import os
import io
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Google Cloud Document AI
from google.cloud import documentai_v1 as documentai

# Gemini (Google AI for Developers - Gemini API)
from google import genai
from google.genai import types as genai_types

# Config
ALLOWED_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB

# Env (use .env or GCP Secret Manager in prod)
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("DOCAI_LOCATION", "us")  # 'us' or 'eu'
PROCESSOR_ID = os.getenv("DOCAI_PROCESSOR_ID")  # Document AI processor
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Gemini API key

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Initialize clients once
docai_client = documentai.DocumentProcessorServiceClient()
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/analyze", methods=["POST"])
def analyze():
    # Validate file
    if "file" not in request.files:
        return jsonify({"error": "No file part 'file' in form-data"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(f.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    filename = secure_filename(f.filename)
    pdf_bytes = f.read()
    if not pdf_bytes:
        return jsonify({"error": "Empty file"}), 400

    # Step 1: Extract text via Document AI
    try:
        name = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        raw_document = documentai.RawDocument(content=pdf_bytes, mime_type="application/pdf")
        request_docai = documentai.ProcessRequest(name=name, raw_document=raw_document)
        result = docai_client.process_document(request=request_docai)
        doc = result.document

        # Prefer plain text; positions map into text_anchor offsets
        extracted_text = doc.text or ""
        if not extracted_text.strip():
            return jsonify({"error": "No text extracted from PDF"}), 422
    except Exception as e:
        return jsonify({"error": f"Document AI processing failed: {str(e)}"}), 502

    # Step 2: Ask Gemini to segment into sentences, compute offsets, and classify importance color
    # Use structured output with a response schema to guarantee valid JSON
    # Colors: "red" (high risk), "amber" (medium risk), "green" (low/neutral)
    response_schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["sentence", "sentence_start", "sentence_end", "color"],
                    "properties": {
                        "sentence": {"type": "string"},
                        "sentence_start": {"type": "integer", "minimum": 0},
                        "sentence_end": {"type": "integer", "minimum": 0},
                        "color": {"type": "string", "enum": ["red", "amber", "green"]}
                    },
                    "propertyOrdering": ["sentence", "sentence_start", "sentence_end", "color"]
                }
            }
        },
        "required": ["items"],
        "propertyOrdering": ["items"]
    }

    system_prompt = (
        "You are a legal risk annotator. "
        "Input is full document text. "
        "Task: split into sentences and return start/end character offsets (0-based, end exclusive) "
        "into the provided text, and a color importance level: "
        "'red' for potentially unfavorable or risky legal clauses (e.g., indemnity, unilateral termination, liquidated damages, arbitration venue far from user, auto-renew with tight cancellation, data sharing without consent); "
        "'amber' for cautionary clauses; 'green' for neutral/informational. "
        "Do not invent text. Compute offsets against the exact input string. "
        "Return strictly JSON per the provided schema."
    )

    try:
        gemini_response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                system_prompt,
                genai_types.Part.from_text(f"DOCUMENT_TEXT:\n{extracted_text}")
            ],
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        # The SDK returns parsed JSON when response_mime_type is application/json.
        parsed = gemini_response.parsed  # {'items': [...]} expected
        items = parsed.get("items", [])
    except Exception as e:
        return jsonify({"error": f"Gemini analysis failed: {str(e)}"}), 502

    # Optional: server-side sanity checks
    clean = []
    n = len(extracted_text)
    for it in items:
        s = it.get("sentence", "")
        a = it.get("sentence_start", 0)
        b = it.get("sentence_end", 0)
        c = it.get("color", "green")
        if not isinstance(s, str) or not isinstance(a, int) or not isinstance(b, int):
            continue
        if a < 0 or b <= a or b > n:
            continue
        # light consistency check: the substring should contain the provided sentence (not strict equality because of trimming)
        sub = extracted_text[a:b].strip()
        if s.strip() and s.strip() not in sub:
            # If mismatch, fallback to substring to ensure frontend highlighting matches
            s = sub
        if c not in ("red", "amber", "green"):
            c = "green"
        clean.append({
            "sentence": s,
            "sentence_start": a,
            "sentence_end": b,
            "color": c
        })

    return jsonify({
        "filename": filename,
        "text_length": len(extracted_text),
        "items": clean
    }), 200

if __name__ == "__main__":
    # For local dev: set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON with Document AI access.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
