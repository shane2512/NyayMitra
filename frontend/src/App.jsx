import React, { useState, useEffect } from 'react';
import FileUploader from './components/FileUploader';
import RiskVisualization from './components/RiskVisualization';
import ContractSummary from './components/ContractSummary';
import TranslatedSummary from './components/TranslatedSummary';
import ChatInterface from './components/ChatInterface';
import DebugPanel from './components/DebugPanel';
import SimulationModal from './components/SimulationModal';
import SimulationCharts from './components/SimulationCharts';
import ClauseHighlighter from './components/ClauseHighlighter';
import { analyzeContract } from './api';
import SummaryDialog from './components/SummaryDialog';
import Card from './components/ui/Card';
import Button from './components/ui/Button';
import { 
  FileText, AlertTriangle, Scale, BarChart3, MessageSquare, 
  Brain, TrendingUp, Shield, Loader2, Sparkles, Activity,
  CheckCircle, XCircle, AlertCircle, Info, ChevronRight,
  FileSearch, Target, Zap, Globe, Clock
} from 'lucide-react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSimulation, setShowSimulation] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [rateLimitInfo, setRateLimitInfo] = useState(null);
  const [showDebug, setShowDebug] = useState(false);

  // Keyboard shortcut for debug panel
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.ctrlKey && event.shiftKey && event.key === 'D') {
        event.preventDefault();
        setShowDebug(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Use the API function with proper error handling
  const handleApiCall = async (file, language = 'en', interests = []) => {
    try {
      const result = await analyzeContract(file, language, interests);
      return result;
    } catch (error) {
      if (error.response?.status === 429) {
        const retryAfter = error.response.headers['retry-after'] || 60;
        setRateLimitInfo({ 
          limited: true, 
          retryAfter, 
          message: `Rate limit exceeded. Please wait ${retryAfter} seconds.` 
        });
        throw { error: 'Rate limit exceeded. Please wait a moment and try again.' };
      }
      throw error; // Re-throw the original error
    }
  };

  const handleFileSelect = (file, language, interests) => {
    setSelectedFile(file);
    setSelectedLanguage(language || 'en');
    setSelectedInterests(interests || []);
    setError(null);
    setRateLimitInfo(null);
    
    if (file) {
      handleAnalyze(file, language, interests);
    } else {
      setAnalysisResult(null);
    }
  };

  const handleAnalyze = async (file, language = 'en', interests = []) => {
    if (!file) return;

    setIsLoading(true);
    setError(null);
    setAnalysisResult(null); // Clear previous results
    
    try {
      console.log('Starting analysis for file:', file.name);
      console.log('File size:', file.size, 'bytes');
      console.log('Language:', language, 'Interests:', interests);
      
      const result = await handleApiCall(file, language, interests);
      console.log('Analysis result received:', result);
      console.log('Result type:', typeof result);
      console.log('Result status:', result?.status);
      
      // More robust status checking
      if (result && typeof result === 'object') {
        if (result.status === 'success') {
          console.log('✅ Analysis successful, setting result');
          console.log('Summary length:', result.summary?.length || 0);
          console.log('Risk report entries:', Object.keys(result.risk_report || {}).length);
          
          setAnalysisResult(result);
          setError(null);
        } else if (result.status === 'error') {
          console.log('❌ Analysis returned error status:', result.error);
          setError(result.error || result.details || 'Analysis failed');
        } else {
          console.log('⚠️ Unexpected status:', result.status);
          setError(`Unexpected response status: ${result.status}`);
        }
      } else {
        console.log('❌ Invalid result format:', result);
        setError('Invalid response format from server');
      }
    } catch (err) {
      console.error('❌ Analysis error caught:', err);
      console.error('Error type:', typeof err);
      console.error('Error keys:', Object.keys(err || {}));
      console.error('Error stringified:', JSON.stringify(err, null, 2));
      console.error('Error details:', {
        message: err?.message,
        error: err?.error,
        response: err?.response,
        status: err?.status,
        statusText: err?.statusText,
        stack: err?.stack,
        data: err?.data,
        config: err?.config
      });
      
      // Better error message handling
      let errorMessage = 'Failed to analyze contract';
      
      // Handle different error formats
      if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.error) {
        errorMessage = err.error;
      } else if (err?.message) {
        if (err.message.includes('timeout')) {
          errorMessage = 'Analysis timed out. Please try again.';
        } else if (err.message.includes('Network Error')) {
          errorMessage = 'Network error. Please check if the backend server is running.';
        } else {
          errorMessage = err.message;
        }
      } else if (err?.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err?.statusText) {
        errorMessage = `HTTP Error: ${err.statusText}`;
      } else {
        errorMessage = 'Unknown error occurred during analysis';
      }
      
      console.log('Final error message:', errorMessage);
      setError(errorMessage);
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
    <div className="min-h-screen bg-midnight">
      {/* Main Dashboard */}
      <main className="relative">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-azure/10 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-teal/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header Section */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-3xl font-heading font-bold text-light-gray mb-2">
                  Contract Analysis Dashboard
                </h1>
                <p className="text-muted-gray">
                  Upload a PDF contract to analyze risks and get AI-powered insights
                </p>
              </div>
            </div>
          </div>

          {/* Upload Section */}
          <div className="mb-8">
            <Card variant="glass" className="p-6">
              <div className="mb-6">
                <h2 className="text-xl font-heading font-semibold text-light-gray mb-2 flex items-center">
                  <FileSearch className="w-5 h-5 mr-2 text-azure" />
                  Upload Contract
                </h2>
                <p className="text-muted-gray">
                  Select your preferred language and focus areas for analysis
                </p>
              </div>
              <FileUploader 
                onFileSelect={handleFileSelect} 
                isLoading={isLoading} 
                error={error}
                showLanguageSelector={true}
                showInterestsSelector={true}
              />
            </Card>
            
            {/* Rate Limit Warning */}
            {rateLimitInfo?.limited && (
              <Card variant="glass" className="mt-4 p-4 border-amber/50">
                <div className="flex items-center space-x-3">
                  <Clock className="w-5 h-5 text-amber" />
                  <div>
                    <p className="text-amber font-medium">Rate Limit Active</p>
                    <p className="text-muted-gray text-sm">{rateLimitInfo.message}</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Error State */}
            {error && (
              <Card variant="glass" className="mt-4 p-4 border-danger/50">
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="w-5 h-5 text-danger" />
                  <div>
                    <p className="text-danger font-medium">Analysis Error</p>
                    <p className="text-muted-gray text-sm">{error}</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Loading State */}
            {isLoading && (
              <Card variant="glass" className="mt-4 p-6">
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <Loader2 className="w-8 h-8 text-azure animate-spin" />
                    <div className="absolute inset-0 w-8 h-8 bg-azure/20 rounded-full animate-ping" />
                  </div>
                  <div>
                    <p className="text-light-gray font-medium">Analyzing Contract</p>
                    <p className="text-muted-gray text-sm">Our AI agents are processing your document...</p>
                  </div>
                </div>
                <div className="mt-4 w-full h-2 bg-charcoal rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-premium animate-pulse" style={{ width: '60%' }} />
                </div>
              </Card>
            )}
          </div>

          {/* Analysis Results */}
          {analysisResult && !isLoading && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
              {/* Main Analysis - Left Side (2/3 width) */}
              <div className="lg:col-span-2 space-y-6">
                {/* Risk Overview Cards */}
                <div className="grid grid-cols-3 gap-4">
                  <Card variant="glass" className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-gray">Total Clauses</p>
                        <p className="text-3xl font-heading font-bold text-light-gray">{stats.total}</p>
                      </div>
                      <div className="p-3 bg-azure/20 rounded-xl">
                        <FileText className="w-6 h-6 text-azure" />
                      </div>
                    </div>
                  </Card>
                  <Card variant="glass" className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-gray">High Risk</p>
                        <p className="text-3xl font-heading font-bold text-danger">{stats.high}</p>
                      </div>
                      <div className="p-3 bg-danger/20 rounded-xl">
                        <AlertTriangle className="w-6 h-6 text-danger" />
                      </div>
                    </div>
                  </Card>
                  <Card variant="glass" className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-gray">Safety Index</p>
                        <p className="text-3xl font-heading font-bold text-amber">{analysisResult.simulation?.safety_index === 'High Risk' ? 'HIGH' : analysisResult.simulation?.safety_index === 'Low Risk' ? 'LOW' : 'MED'}</p>
                      </div>
                      <div className="p-3 bg-teal/20 rounded-xl">
                        <Scale className="w-6 h-6 text-teal" />
                      </div>
                    </div>
                  </Card>
                </div>

                {/* Clause Analysis */}
                <Card variant="glass">
                  <Card.Header icon={<Brain className="w-5 h-5 text-azure" />}>
                    <h3 className="text-lg font-heading font-semibold text-light-gray">
                      Contract Clauses
                    </h3>
                    <p className="text-sm text-muted-gray">AI-analyzed clauses with risk levels</p>
                  </Card.Header>
                  <Card.Content>
                    <ClauseHighlighter 
                      contract={analysisResult.contract_text} 
                      riskReport={analysisResult.risk_report} 
                    />
                  </Card.Content>
                </Card>
              </div>

              {/* Right Side (1/3 width) - Only show View Summary button */}
              <div className="lg:col-span-1 flex flex-col items-center justify-start pt-4 space-y-4">
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => setShowSummary(true)}
                  glow
                  className="w-full"
                >
                  View Summary
                </Button>
                <Button
                  variant="secondary"
                  size="lg"
                  onClick={() => setShowSimulation(true)}
                  className="w-full"
                >
                  View Simulation
                </Button>
              </div>

              {/* Simulation Modal */}
              {showSimulation && analysisResult && (
                <SimulationModal
                  simulation={analysisResult.simulation}
                  riskReport={analysisResult.risk_report}
                  onClose={() => setShowSimulation(false)}
                />
              )}
            </div>
          )}

          {/* Welcome State */}
          {!analysisResult && !isLoading && (
            <div className="text-center py-20">
              <div className="flex items-center justify-center w-24 h-24 bg-gradient-premium rounded-full mx-auto mb-8 animate-pulse-glow">
                <Scale className="w-12 h-12 text-white" />
              </div>
              <h2 className="text-4xl font-heading font-bold text-light-gray mb-4">
                Welcome to NyayMitra
              </h2>
              <p className="text-xl text-muted-gray max-w-3xl mx-auto mb-12 leading-relaxed">
                Your AI-powered legal contract analyzer. Upload a contract to get started with 
                comprehensive risk analysis, plain language summaries, and negotiation insights.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                <Card variant="glass" hover className="p-8 text-center">
                  <div className="w-16 h-16 bg-danger/20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Shield className="w-8 h-8 text-danger" />
                  </div>
                  <h3 className="text-xl font-heading font-semibold mb-3 text-light-gray">
                    Risk Analysis
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    AI identifies and categorizes contract risks with precision
                  </p>
                </Card>
                <Card variant="glass" hover className="p-8 text-center">
                  <div className="w-16 h-16 bg-azure/20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <FileText className="w-8 h-8 text-azure" />
                  </div>
                  <h3 className="text-xl font-heading font-semibold mb-3 text-light-gray">
                    Plain Language
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    Complex legal terms explained in simple language
                  </p>
                </Card>
                <Card variant="glass" hover className="p-8 text-center">
                  <div className="w-16 h-16 bg-teal/20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <BarChart3 className="w-8 h-8 text-teal" />
                  </div>
                  <h3 className="text-xl font-heading font-semibold mb-3 text-light-gray">
                    Simulation
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    Advanced negotiation scenarios and outcome predictions
                  </p>
                </Card>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Floating Chat Button */}
      {!showChat && (
        <div className="fixed bottom-6 right-6 z-40">
          <Button
            variant="gradient"
            size="lg"
            onClick={() => setShowChat(true)}
            className="rounded-full shadow-2xl"
            glow
          >
            <Sparkles className="w-5 h-5 mr-2" />
            AI Assistant
          </Button>
        </div>
      )}

      {/* Chat Interface */}
      {showChat && (
        <ChatInterface
          isOpen={showChat}
          onClose={() => setShowChat(false)}
          contractContext={analysisResult}
        />
      )}

      {/* Simulation Modal */}
      {showSimulation && analysisResult && (
        <SimulationModal
          simulation={analysisResult.simulation}
          riskReport={analysisResult.risk_report}
          onClose={() => setShowSimulation(false)}
        />
      )}

      {/* Summary Dialog */}
      {showSummary && analysisResult && (
        <SummaryDialog
          open={showSummary}
          summary={analysisResult.summary}
          onClose={() => setShowSummary(false)}
        />
      )}

      {/* Debug Panel - Press Ctrl+Shift+D to toggle */}
      <DebugPanel 
        isVisible={showDebug}
        analysisResult={analysisResult}
        error={error}
        isLoading={isLoading}
        onClose={() => setShowDebug(false)}
      />

      {/* Debug Toggle Button */}
      <button
        onClick={() => setShowDebug(!showDebug)}
        className="fixed bottom-4 left-4 p-2 bg-gray-800 text-white rounded-full shadow-lg hover:bg-gray-700 transition-colors z-50"
        title="Toggle Debug Panel (Ctrl+Shift+D)"
      >
        🔍
      </button>
    </div>
  );
};

export default App;
