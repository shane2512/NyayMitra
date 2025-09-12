import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import ClauseHighlighter from './components/ClauseHighlighter';
import RiskSummary from './components/RiskSummary';
import SimulationModal from './components/SimulationModal';
import { analyzeContract } from './api';
import { Loader2, Scale, BarChart3, FileText, AlertTriangle } from 'lucide-react';
import './index.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSimulation, setShowSimulation] = useState(false);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setError(null);
    if (file) {
      handleAnalyze(file);
    } else {
      setAnalysisResult(null);
    }
  };

  const handleAnalyze = async (file) => {
    if (!file) return;

    setIsLoading(true);
    setError(null);
    
    try {
      const result = await analyzeContract(file);
      if (result.status === 'success') {
        setAnalysisResult(result);
      } else {
        setError(result.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.error || 'Failed to analyze contract');
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskStats = () => {
    if (!analysisResult?.simulation) return { high: 0, medium: 0, low: 0, total: 0 };
    const { risk_distribution } = analysisResult.simulation;
    return {
      high: risk_distribution?.High || 0,
      medium: risk_distribution?.Medium || 0,
      low: risk_distribution?.Low || 0,
      total: analysisResult.simulation.total_clauses || 0
    };
  };

  const stats = getRiskStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
                <Scale className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">NyayMitra</h1>
                <p className="text-sm text-gray-500">AI Legal Contract Analyzer</p>
              </div>
            </div>
            
            {analysisResult && (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 text-sm">
                  <div className="flex items-center space-x-1">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span className="text-gray-600">{stats.high} High</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <span className="text-gray-600">{stats.medium} Medium</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-gray-600">{stats.low} Low</span>
                  </div>
                </div>
                <button
                  onClick={() => setShowSimulation(true)}
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <BarChart3 className="w-4 h-4" />
                  <span>View Simulation</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Upload Section */}
        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">Upload Contract</h2>
              <p className="text-gray-600">Upload a PDF contract to analyze risks and get AI-powered insights</p>
            </div>
            <FileUploader onFileSelect={handleFileSelect} isLoading={isLoading} />
          </div>
          
          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-red-500" />
                <p className="text-red-800 font-medium">Analysis Error</p>
              </div>
              <p className="text-red-700 mt-1">{error}</p>
            </div>
          )}

          {isLoading && (
            <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center space-x-3">
                <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                <div>
                  <p className="text-blue-800 font-medium">Analyzing Contract</p>
                  <p className="text-blue-700 text-sm">Our AI agents are processing your document...</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Analysis Results */}
        {analysisResult && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Contract Analysis - Left Side (2/3 width) */}
            <div className="lg:col-span-2 space-y-6">
              {/* Risk Overview Cards */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Clauses</p>
                      <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                    </div>
                    <FileText className="w-8 h-8 text-gray-400" />
                  </div>
                </div>
                
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">High Risk</p>
                      <p className="text-2xl font-bold text-red-600">{stats.high}</p>
                    </div>
                    <AlertTriangle className="w-8 h-8 text-red-400" />
                  </div>
                </div>
                
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Safety Index</p>
                      <p className={`text-2xl font-bold ${
                        analysisResult.simulation?.safety_index === 'High Risk' ? 'text-red-600' :
                        analysisResult.simulation?.safety_index === 'Low Risk' ? 'text-green-600' :
                        'text-yellow-600'
                      }`}>
                        {analysisResult.simulation?.safety_index === 'High Risk' ? 'HIGH' :
                         analysisResult.simulation?.safety_index === 'Low Risk' ? 'LOW' : 'MED'}
                      </p>
                    </div>
                    <Scale className="w-8 h-8 text-blue-400" />
                  </div>
                </div>
              </div>

              {/* Clause Analysis */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                <div className="border-b border-gray-200 px-6 py-4">
                  <h3 className="text-lg font-semibold text-gray-900">Contract Clauses</h3>
                  <p className="text-sm text-gray-600">AI-analyzed clauses with risk levels</p>
                </div>
                <div className="p-6">
                  <ClauseHighlighter 
                    contract={analysisResult.contract_text} 
                    riskReport={analysisResult.risk_report} 
                  />
                </div>
              </div>
            </div>

            {/* Risk Summary - Right Side (1/3 width) */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 sticky top-6">
                <div className="border-b border-gray-200 px-6 py-4">
                  <h3 className="text-lg font-semibold text-gray-900">Risk Analysis</h3>
                  <p className="text-sm text-gray-600">AI-generated summary and insights</p>
                </div>
                <div className="p-6">
                  <RiskSummary 
                    summary={analysisResult.summary} 
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Welcome State */}
        {!analysisResult && !isLoading && (
          <div className="text-center py-16">
            <div className="flex items-center justify-center w-24 h-24 bg-blue-100 rounded-full mx-auto mb-6">
              <Scale className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Welcome to NyayMitra
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
              Your AI-powered legal contract analyzer. Upload a contract to get started with 
              comprehensive risk analysis, plain language summaries, and negotiation insights.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="text-center p-6">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AlertTriangle className="w-8 h-8 text-red-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Risk Analysis</h3>
                <p className="text-gray-600">AI identifies and categorizes contract risks</p>
              </div>
              <div className="text-center p-6">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FileText className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Plain Language</h3>
                <p className="text-gray-600">Complex legal terms explained simply</p>
              </div>
              <div className="text-center p-6">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BarChart3 className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Simulation</h3>
                <p className="text-gray-600">Negotiation scenarios and outcomes</p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Simulation Modal */}
      {showSimulation && analysisResult && (
        <SimulationModal
          simulation={analysisResult.simulation}
          riskReport={analysisResult.risk_report}
          onClose={() => setShowSimulation(false)}
        />
      )}
    </div>
  );
}

export default App;