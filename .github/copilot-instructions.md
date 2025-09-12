# NyayMitra AI Agent Instructions

## Project Overview
NyayMitra is a multi-agent AI system for legal contract risk analysis with:
- **Backend**: Python Flask API with 4 specialized AI agents
- **Frontend**: React app with Tailwind UI for contract visualization
- **AI Integration**: Google Gemini models for legal analysis

## Architecture Patterns

### Agent System Structure
- Each agent in `backend/agents/` is a standalone class with specific responsibilities
- **RiskAnalyzerAgent**: PDF extraction + clause-level risk assessment via Gemini
- **SummarizerAgent**: Converts technical analysis to plain language
- **SimulationAgent**: Risk quantification + safety index calculation
- **ModeratorAgent**: Orchestrates agent workflow and API responses

### Key Integration Points
- All agents require `api_key` parameter for Gemini configuration
- Risk reports use standardized JSON: `{"analysis": {"risk_level": "High/Medium/Low", "analysis": "text"}}`
- Frontend expects specific API response format from `/analyze` endpoint

## Development Workflows

### Backend Development
```bash
cd backend
pip install -r requirements.txt
set GEMINI_API_KEY=your_key_here
python app.py  # Starts Flask server on port 5000
```

### Frontend Development
```bash
cd frontend
npm install
npm start  # Starts React dev server on port 3000
```

### File Upload Testing
- Use PDF files only - system validates file extensions
- Temporary files auto-deleted after processing
- CORS enabled for local development (localhost:3000 → localhost:5000)

## Project-Specific Conventions

### Error Handling Pattern
All agents return `{"status": "success/error", "error": "message"}` format for consistent frontend handling.

### Risk Level Mapping
- Frontend color coding: High=red, Medium=yellow, Low=green
- Risk percentages calculated as `(count/total) * 100`
- Safety index logic: >50% High = "High Risk", else Medium≥High = "Moderate Risk"

### UI Component Structure
- `ClauseHighlighter`: Right panel showing color-coded contract text
- `RiskSummary`: Bottom-left with plain language explanations  
- `SimulationCharts`: Bottom-right with Recharts visualizations
- Responsive grid layout: `lg:grid-cols-2` with nested `grid-rows-2`

## Critical Dependencies
- **PyMuPDF**: PDF text extraction - import as `fitz`
- **google-generativeai**: AI model integration - configure with API key first
- **flask-cors**: Essential for React ↔ Flask communication
- **recharts**: Frontend charts - PieChart + BarChart components

## API Integration Notes
- `/analyze` endpoint expects `multipart/form-data` with 'file' field
- Frontend uses axios with FormData for file uploads
- Health check available at `/health` for deployment verification

When adding new features, follow the agent-based architecture and maintain the standardized JSON response formats for seamless frontend integration.
