"""
Simple Demo for RAG System Simulation Mode

This script simulates the Legal Judgment RAG system functionality
without requiring all the dependencies to be installed.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def simulate_rag_analysis(query_text):
    """
    Simulate a RAG analysis by returning a mock response
    
    Args:
        query_text: The query text to analyze
        
    Returns:
        Dict with analysis results
    """
    logger.info(f"Simulating RAG analysis for query: {query_text[:50]}...")
    
    # Get the query type
    query_type = "property dispute"
    if "landlord" in query_text.lower() or "tenant" in query_text.lower() or "lease" in query_text.lower():
        query_type = "landlord-tenant dispute"
    elif "injury" in query_text.lower() or "accident" in query_text.lower():
        query_type = "personal injury"
    elif "property" in query_text.lower() or "neighbor" in query_text.lower():
        query_type = "property dispute"
    
    # Create a simulated response based on query type
    if query_type == "landlord-tenant dispute":
        analysis = """
RELEVANT CASE CITATIONS:
- Smith v. Jones [2020]
- Tenant Rights Association v. Landlord Corp [2018]
- Housing Authority v. Williams [2019]

LEGAL PRECEDENTS:
- Precedent 1: Landlords must return security deposits within 30 days of lease termination
- Precedent 2: Landlords must provide itemized list of deductions with receipts
- Precedent 3: Tenants have the right to dispute deductions in small claims court

APPLICABLE LAWS AND STATUTES:
- Residential Tenancies Act: Section 21(3) - Security Deposit Returns
- Property Law Act: Section 8 - Tenant Rights
- Civil Code: Article 1950-1954 - Lease Agreements

SUMMARY OF APPLICABILITY:
This is a simulated response for landlord-tenant disputes. The system would analyze your specific situation regarding security deposits, lease terms, or rental conditions and provide relevant legal information based on applicable laws and precedents.
"""
    elif query_type == "personal injury":
        analysis = """
RELEVANT CASE CITATIONS:
- Johnson v. Auto Insurance Co. [2021]
- Smith v. City Transit [2019]
- Medical Association v. Insurance Board [2022]

LEGAL PRECEDENTS:
- Precedent 1: Injured parties are entitled to compensation for medical expenses and lost wages
- Precedent 2: Insurance companies must process claims in good faith
- Precedent 3: Statute of limitations for personal injury claims is typically 2-3 years

APPLICABLE LAWS AND STATUTES:
- Personal Injury Protection Act: Section 5 - Compensation Guidelines
- Insurance Code: Article 231 - Bad Faith Practices
- Civil Procedure Code: Section 15-1 - Statute of Limitations

SUMMARY OF APPLICABILITY:
This is a simulated response for personal injury cases. The system would analyze your specific situation regarding the accident, medical expenses, insurance settlement offers, and provide relevant legal information based on applicable laws and precedents.
"""
    else:  # property dispute
        analysis = """
RELEVANT CASE CITATIONS:
- Neighbor v. Neighbor [2022]
- Property Boundaries Inc. v. Homeowner Association [2020]
- City Planning v. Development Corp [2021]

LEGAL PRECEDENTS:
- Precedent 1: Property boundaries established by survey take precedence over historical use
- Precedent 2: Adverse possession requires open, notorious, and continuous use for statutory period
- Precedent 3: Encroachment remedies include removal, easements, or compensation

APPLICABLE LAWS AND STATUTES:
- Property Law Act: Section 12 - Boundary Disputes
- Civil Code: Article 850-855 - Adverse Possession
- Land Survey Act: Section 7 - Survey Authentication

SUMMARY OF APPLICABILITY:
This is a simulated response for property disputes. The system would analyze your specific situation regarding boundaries, encroachments, or easements and provide relevant legal information based on applicable laws and precedents.
"""

    # Create a sources list
    sources = [
        {"file": "Judgment_1.pdf", "page": 15},
        {"file": "Judgment_2.pdf", "page": 42}
    ]
    
    return {
        "analysis": analysis,
        "sources": sources
    }

def main():
    """Main function to run the demo"""
    print("\n" + "="*50)
    print("LEGAL JUDGMENT RAG SIMULATION DEMO")
    print("="*50)
    print("\nNote: This is running in simulation mode.")
    print("To run the full model, install all dependencies from requirements.txt")
    
    # Define the sample queries
    queries = {
        "1": {
            "name": "Property dispute with neighbor",
            "text": """
            I am writing to seek advice regarding a property dispute I'm currently involved in. 
            My neighbor has constructed a wall that encroaches approximately 2 feet onto my property 
            according to the land survey and property deed. The wall was constructed 3 months ago 
            without my consent or any consultation.
            """
        },
        "2": {
            "name": "Landlord-tenant security deposit dispute",
            "text": """
            I'm dealing with a landlord-tenant dispute. My landlord has refused to return my 
            security deposit claiming damages to the property, but I have photos showing the 
            apartment was in perfect condition when I moved out. What legal recourse do I have?
            """
        },
        "3": {
            "name": "Personal injury from car accident",
            "text": """
            I was injured in a car accident where the other driver ran a red light. I have medical 
            bills and lost wages due to the injury. The insurance company is offering a settlement 
            that doesn't cover all my expenses. What are my rights in this situation?
            """
        }
    }
    
    # Get query choice from command line argument or use default
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ["1", "2", "3"]:
        choice = sys.argv[1]
    else:
        print("\nAvailable sample queries:")
        for key, query in queries.items():
            print(f"{key}. {query['name']}")
        print("\nUsage: python demo_simulation.py [1-3]")
        print("Using default query (1)")
        choice = "1"
    
    # Use the selected query
    sample_query = queries[choice]["text"]
    print(f"\nUsing sample query {choice}: {queries[choice]['name']}")
    
    # Process the query
    result = simulate_rag_analysis(sample_query)
    
    # Display results
    print("\n" + "="*50)
    print("LEGAL JUDGMENT ANALYSIS RESULTS (SIMULATED)")
    print("="*50 + "\n")
    
    print("QUERY:")
    print(sample_query)
    
    print("\nANALYSIS:")
    print(result["analysis"])
    
    print("\nSOURCES:")
    for source in result["sources"]:
        print(f"- {source['file']}, Page {source['page']}")
    
    print("\n" + "="*50)
    print("NOTE: This is a simulation using mock data.")
    print("Install all required dependencies to use the actual RAG model.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()