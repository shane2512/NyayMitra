import requests
import json

def test_nyaymitra_api():
    print("Testing NyayMitra API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        health_response = requests.get('http://localhost:5000/health')
        print(f"✅ Health check: {health_response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test file upload
    print("\n2. Testing file upload...")
    try:
        file_path = r"d:\New folder\nyaymitra\sample_contracts\sample_contract.pdf"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            print(f"Uploading {file_path}...")
            response = requests.post('http://localhost:5000/analyze', files=files)
            
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print("\n📊 Analysis Results:")
            print(f"Status: {result.get('status')}")
            print(f"Full Response: {json.dumps(result, indent=2)}")
            
            if 'risk_report' in result:
                risk_report = result['risk_report']
                print(f"Risk Report Keys: {list(risk_report.keys())}")
                
                # Count risk levels
                if 'analysis' in risk_report:
                    analysis = risk_report['analysis']
                    high_risk = sum(1 for clause in analysis.values() if clause.get('risk_level') == 'High')
                    medium_risk = sum(1 for clause in analysis.values() if clause.get('risk_level') == 'Medium')
                    low_risk = sum(1 for clause in analysis.values() if clause.get('risk_level') == 'Low')
                    print(f"High Risk: {high_risk}, Medium Risk: {medium_risk}, Low Risk: {low_risk}")
            
            if 'summary' in result:
                summary = result['summary'][:200] + "..." if len(result['summary']) > 200 else result['summary']
                print(f"Summary: {summary}")
                
            if 'simulation' in result:
                simulation = result['simulation']
                print(f"Safety Index: {simulation.get('safety_index')}")
                print(f"Total Clauses: {simulation.get('total_clauses')}")
                
            print("\n🎉 All tests passed! NyayMitra is working correctly.")
            
        else:
            print(f"❌ Upload failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")

if __name__ == "__main__":
    test_nyaymitra_api()
