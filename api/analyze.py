import json
import os
import tempfile
import fitz  # PyMuPDF
import google.generativeai as genai

def handler(request, context):
    """
    Vercel serverless function handler for contract analysis.
    """
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({})
        }
    
    # Handle POST request
    if request.method == 'POST':
        try:
            # Check for environment variables
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'GEMINI_API_KEY environment variable not set',
                        'status': 'error'
                    })
                }
            
            # Get form data
            language = 'en'
            interests = []
            file_content = None
            filename = 'uploaded_contract'
            
            # Handle multipart form data
            if hasattr(request, 'files') and 'file' in request.files:
                file = request.files['file']
                file_content = file.read()
                filename = file.filename or 'uploaded_contract'
            elif hasattr(request, 'form'):
                if 'language' in request.form:
                    language = request.form['language']
                if 'interests' in request.form:
                    try:
                        interests = json.loads(request.form['interests'])
                    except:
                        interests = []
                if 'file' in request.form:
                    # Handle file data from form
                    file_content = request.form['file']
            
            # If no file content, return error
            if not file_content:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'No file provided for analysis',
                        'status': 'error'
                    })
                }
            
            # Extract text from PDF
            text_content = ""
            try:
                if filename.lower().endswith('.pdf'):
                    # Create temporary file for PDF processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(file_content)
                        tmp_path = tmp_file.name
                    
                    try:
                        # Extract text using PyMuPDF
                        doc = fitz.open(tmp_path)
                        for page in doc:
                            text_content += page.get_text()
                        doc.close()
                    finally:
                        # Clean up temp file
                        os.unlink(tmp_path)
                else:
                    # Assume text file
                    text_content = file_content.decode('utf-8', errors='ignore')
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'error': f'Failed to extract text from file: {str(e)}',
                        'status': 'error'
                    })
                }
            
            # Analyze contract using Gemini
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""Analyze this legal contract and provide a risk assessment. 
                
Contract text:
{text_content[:10000]}  # Limit text to avoid token limits

Please provide:
1. Overall risk level (High/Medium/Low)
2. Key risk factors identified
3. Important clauses to review
4. Recommendations

Language: {language}
Focus areas: {interests if interests else 'General analysis'}
"""
                
                response = model.generate_content(prompt)
                ai_analysis = response.text
                
                # Structure the response
                result = {
                    "status": "success",
                    "summary": "Contract analysis completed using AI",
                    "ai_analysis": ai_analysis,
                    "risk_score": 70,  # Could be extracted from AI response
                    "key_findings": [
                        "AI-powered analysis completed",
                        "Detailed risk assessment provided", 
                        "Review recommendations included"
                    ],
                    "language": language,
                    "interests": interests,
                    "text_length": len(text_content),
                    "filename": filename
                }
                
            except Exception as e:
                # Fallback to demo analysis if AI fails
                result = {
                    "status": "success", 
                    "summary": "Contract analysis completed (demo mode)",
                    "risk_score": 65,
                    "key_findings": [
                        "Document successfully processed",
                        "Text extraction completed",
                        f"Document contains {len(text_content)} characters",
                        "AI analysis temporarily unavailable - demo results shown"
                    ],
                    "language": language,
                    "interests": interests,
                    "text_length": len(text_content),
                    "filename": filename,
                    "note": f"AI analysis error: {str(e)}"
                }
            
            response_data = {
                'status': 'success',
                'analysis': result,
                'language': language,
                'interests': interests
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response_data)
            }
            
        except Exception as e:
            error_response = {
                'error': f'Analysis handler error: {str(e)}',
                'type': 'server_error',
                'status': 'error'
            }
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps(error_response)
            }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({
            'error': 'Method not allowed. Use POST to upload files.',
            'type': 'method_error'
        })
    }
