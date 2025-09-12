import React from 'react';
import { MessageSquare, Lightbulb, TrendingUp, AlertTriangle, CheckCircle2, Clock } from 'lucide-react';

const RiskSummary = ({ summary }) => {
  if (!summary) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-6 sticky top-4">
        <div className="flex items-center space-x-3 mb-6">
          <MessageSquare className="w-6 h-6 text-green-600" />
          <h3 className="text-lg font-bold text-gray-900">AI Summary</h3>
        </div>
        <div className="text-center py-8">
          <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 text-lg mb-2">No summary available</p>
          <p className="text-gray-400 text-sm">Upload and analyze a contract to get an AI-powered plain language summary</p>
        </div>
      </div>
    );
  }

  // Extract key insights from the summary
  const getSummaryInsights = (summaryText) => {
    const insights = [];
    
    if (summaryText.toLowerCase().includes('high risk')) {
      insights.push({
        type: 'warning',
        icon: <AlertTriangle className="w-4 h-4 text-red-600" />,
        title: 'High Risk Alert',
        description: 'Contract contains high-risk clauses requiring immediate attention'
      });
    }
    
    if (summaryText.toLowerCase().includes('generally acceptable') || summaryText.toLowerCase().includes('low risk')) {
      insights.push({
        type: 'success',
        icon: <CheckCircle2 className="w-4 h-4 text-green-600" />,
        title: 'Acceptable Terms',
        description: 'Most contract terms appear to be reasonable and balanced'
      });
    }
    
    if (summaryText.toLowerCase().includes('review') || summaryText.toLowerCase().includes('consider')) {
      insights.push({
        type: 'info',
        icon: <Clock className="w-4 h-4 text-blue-600" />,
        title: 'Review Recommended',
        description: 'Some clauses may benefit from further review or negotiation'
      });
    }
    
    return insights;
  };

  const insights = getSummaryInsights(summary);

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 sticky top-4">
      <div className="flex items-center space-x-3 mb-6">
        <MessageSquare className="w-6 h-6 text-green-600" />
        <h3 className="text-lg font-bold text-gray-900">AI Summary</h3>
        <div className="ml-auto">
          <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full border border-green-200">
            Plain Language
          </span>
        </div>
      </div>

      {/* Quick Insights */}
      {insights.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
            <TrendingUp className="w-4 h-4 mr-2" />
            Quick Insights
          </h4>
          <div className="space-y-2">
            {insights.map((insight, index) => (
              <div key={index} className={`flex items-start space-x-3 p-3 rounded-lg border ${
                insight.type === 'warning' ? 'bg-red-50 border-red-200' :
                insight.type === 'success' ? 'bg-green-50 border-green-200' :
                'bg-blue-50 border-blue-200'
              }`}>
                {insight.icon}
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-medium ${
                    insight.type === 'warning' ? 'text-red-900' :
                    insight.type === 'success' ? 'text-green-900' :
                    'text-blue-900'
                  }`}>
                    {insight.title}
                  </p>
                  <p className={`text-xs ${
                    insight.type === 'warning' ? 'text-red-700' :
                    insight.type === 'success' ? 'text-green-700' :
                    'text-blue-700'
                  }`}>
                    {insight.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Summary */}
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
          <Lightbulb className="w-4 h-4 mr-2" />
          Summary
        </h4>
        <div className="prose prose-sm max-w-none">
          <p className="text-gray-800 leading-relaxed text-sm whitespace-pre-wrap">
            {summary}
          </p>
        </div>
      </div>

      {/* Action Items */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h4 className="text-sm font-semibold text-gray-700 mb-3">Recommended Actions</h4>
        <div className="space-y-3">
          <button className="w-full flex items-center justify-between p-3 bg-red-50 hover:bg-red-100 border border-red-200 rounded-lg transition-colors group">
            <div className="flex items-center space-x-2 text-xs text-red-700">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
              <span className="font-medium">Address high-risk clauses immediately</span>
            </div>
            <AlertTriangle className="w-4 h-4 text-red-500 group-hover:scale-110 transition-transform" />
          </button>
          <button className="w-full flex items-center justify-between p-3 bg-yellow-50 hover:bg-yellow-100 border border-yellow-200 rounded-lg transition-colors group">
            <div className="flex items-center space-x-2 text-xs text-yellow-700">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="font-medium">Review medium-risk items during negotiations</span>
            </div>
            <Clock className="w-4 h-4 text-yellow-500 group-hover:scale-110 transition-transform" />
          </button>
          <button className="w-full flex items-center justify-between p-3 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg transition-colors group">
            <div className="flex items-center space-x-2 text-xs text-blue-700">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="font-medium">Consider legal counsel for complex terms</span>
            </div>
            <Lightbulb className="w-4 h-4 text-blue-500 group-hover:scale-110 transition-transform" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RiskSummary;