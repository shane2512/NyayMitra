import json
import os
from urllib.parse import parse_qs

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
            # Parse query parameters
            query_params = parse_qs(request.url.split('?')[1] if '?' in request.url else '')
            language = query_params.get('language', ['en'])[0]
            interests = query_params.get('interests', ['[]'])[0]
            
            try:
                interests = json.loads(interests) if isinstance(interests, str) else interests
            except:
                interests = []
            
            # Demo analysis response
            if language != 'en' or interests:
                result = {
                    "status": "success",
                    "summary": f"Contract analysis completed in {language}",
                    "risk_score": 75,
                    "key_findings": [
                        "Standard commercial agreement",
                        "Moderate risk level identified", 
                        "Review recommended for specific clauses"
                    ],
                    "language": language,
                    "interests": interests,
                    "processing_time": "45 seconds"
                }
            else:
                result = {
                    "status": "success",
                    "summary": "Contract analysis completed successfully",
                    "risk_score": 65,
                    "key_findings": [
                        "Standard terms and conditions",
                        "Low to moderate risk",
                        "No major red flags identified"
                    ],
                    "processing_time": "30 seconds"
                }
            
            response_data = {
                'status': 'success',
                'analysis': result,
                'language': language,
                'interests': interests,
                'processing_time': result.get('processing_time', 'N/A')
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response_data)
            }
            
        except Exception as e:
            error_response = {
                'error': f'Analysis handler error: {str(e)}',
                'type': 'server_error'
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
