import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_analyze_endpoint():
    with open("sample_contracts/sample_contract.pdf", "rb") as pdf_file:
        response = client.post("/analyze", files={"file": pdf_file})
    
    assert response.status_code == 200
    assert "risk_report" in response.json()
    assert "summary" in response.json()
    assert "simulation" in response.json()

def test_analyze_endpoint_invalid_file():
    response = client.post("/analyze", files={"file": ("invalid.txt", "This is not a PDF")})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type. Please upload a PDF."}