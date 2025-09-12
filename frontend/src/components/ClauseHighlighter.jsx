import React from 'react';
import { FileText, Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const ClauseHighlighter = ({ contract, riskReport }) => {
  if (!riskReport || Object.keys(riskReport).length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-6 h-full">
        <div className="flex items-center space-x-3 mb-6">
          <FileText className="w-6 h-6 text-blue-600" />
          <h3 className="text-lg font-bold text-gray-900">Contract Analysis</h3>
        </div>
        <div className="text-center py-8">
          <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 text-lg mb-2">No contract uploaded yet</p>
          <p className="text-gray-400 text-sm">Upload a PDF contract to view detailed clause analysis with risk highlighting</p>
        </div>
      </div>
    );
  }

  // Helper function to determine color based on risk level
  const getRiskColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return 'bg-red-50 border-red-200 hover:bg-red-100';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 hover:bg-yellow-100';
      case 'low':
        return 'bg-green-50 border-green-200 hover:bg-green-100';
      default:
        return 'bg-gray-50 border-gray-200 hover:bg-gray-100';
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-red-600" />;
      case 'medium':
        return <Shield className="w-4 h-4 text-yellow-600" />;
      case 'low':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      default:
        return <Shield className="w-4 h-4 text-gray-600" />;
    }
  };

  const getRiskBadge = (riskLevel) => {
    const baseClasses = "px-2 py-1 rounded-full text-xs font-medium";
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return `${baseClasses} bg-red-100 text-red-700 border border-red-200`;
      case 'medium':
        return `${baseClasses} bg-yellow-100 text-yellow-700 border border-yellow-200`;
      case 'low':
        return `${baseClasses} bg-green-100 text-green-700 border border-green-200`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-700 border border-gray-200`;
    }
  };

  return (
    <div className="space-y-4">
      {Object.entries(riskReport).map(([clauseId, clauseData], index) => {
        const riskLevel = clauseData.analysis?.risk_level || 'Medium';
        const analysisText = clauseData.analysis?.analysis || 'No analysis available';
        const clauseText = clauseData.text || '';
        
        return (
          <div
            key={clauseId}
            className={`border rounded-lg p-4 transition-all duration-200 ${getRiskColor(riskLevel)}`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-2">
                {getRiskIcon(riskLevel)}
                <h4 className="font-semibold text-gray-900 text-sm">
                  {clauseId}
                </h4>
              </div>
              <span className={getRiskBadge(riskLevel)}>
                {riskLevel}
              </span>
            </div>
            
            <div className="bg-white bg-opacity-50 rounded-md p-3 mb-3 cursor-pointer hover:bg-opacity-75 transition-all duration-200">
              <p className="text-gray-800 text-sm leading-relaxed">
                {clauseText.length > 300 ? `${clauseText.substring(0, 300)}...` : clauseText}
              </p>
              {clauseText.length > 300 && (
                <button className="text-blue-600 hover:text-blue-800 text-xs mt-2 font-medium">
                  Show full text →
                </button>
              )}
            </div>
            
            <div className="bg-white bg-opacity-75 rounded-md p-3 border-l-4 border-gray-300">
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-1.5 flex-shrink-0"></div>
                <div>
                  <p className="text-gray-700 text-xs font-medium mb-1">AI Analysis</p>
                  <p className="text-gray-600 text-xs leading-relaxed">
                    {analysisText}
                  </p>
                </div>
              </div>
            </div>
          </div>
        );
      })}
      
      {Object.keys(riskReport).length === 0 && (
        <div className="text-center py-8">
          <AlertTriangle className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">No clauses found for analysis</p>
          <p className="text-gray-400 text-sm mt-1">The contract may be empty or unreadable</p>
        </div>
      )}
    </div>
  );
};

export default ClauseHighlighter;