# NyayMitra API Documentation

## Overview
NyayMitra is a multi-agent system designed to assist users in analyzing legal contracts. The backend exposes a set of RESTful API endpoints that facilitate interaction with the various agents responsible for risk analysis, summarization, and simulation of legal contracts.

## API Endpoints

### 1. Analyze Contract
- **Endpoint:** `/analyze`
- **Method:** `POST`
- **Description:** Analyzes a PDF contract and returns a risk report, summary, and simulation results.
- **Request Body:**
  ```json
  {
    "pdf": "<base64_encoded_pdf>"
  }
  ```
  - `pdf`: The PDF contract encoded in base64 format.

- **Response:**
  ```json
  {
    "risk_report": {
      "total_clauses": 10,
      "risk_distribution": {
        "High": 3,
        "Medium": 4,
        "Low": 3
      },
      "risk_percentages": {
        "High": 30,
        "Medium": 40,
        "Low": 30
      },
      "safety_index": "Moderate Risk"
    },
    "summary": "The contract contains several high-risk clauses that may be unfavorable to the tenant.",
    "simulation": {
      "simulation_result": "If the high-risk clauses are rewritten, the overall safety index would improve to Low Risk."
    }
  }
  ```
  - `risk_report`: Contains details about the risk levels of the clauses.
  - `summary`: A plain language summary of the risks identified.
  - `simulation`: Results of any simulated negotiation outcomes.

## Error Handling
- **Response on Error:**
  ```json
  {
    "error": "Invalid PDF format."
  }
  ```
  - The API will return appropriate error messages for invalid requests or processing issues.

## Usage
To use the API, send a POST request to the `/analyze` endpoint with the PDF contract encoded in base64. The response will include a structured risk report, a summary, and any simulation results.

## Example Request
```bash
curl -X POST http://localhost:8000/analyze \
-H "Content-Type: application/json" \
-d '{"pdf": "<base64_encoded_pdf>"}'
```

## Conclusion
This API provides a comprehensive solution for analyzing legal contracts, making it easier for users to understand potential risks and outcomes without needing legal expertise.