import React, { useState } from 'react';
import { FileText, Copy, Download, Eye, EyeOff, AlertTriangle, CheckCircle, Shield } from 'lucide-react';
import Card from './ui/Card';
import Button from './ui/Button';

const ContractSummary = ({ summary, riskReport, processingTime, totalClauses }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!summary) {
    return (
      <Card className="p-6">
        <div className="text-center text-muted-gray">
          <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>Contract summary will appear here after analysis</p>
        </div>
      </Card>
    );
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([summary], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contract-summary.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Calculate risk stats
  const riskStats = riskReport ? Object.values(riskReport).reduce((acc, clause) => {
    const level = clause.analysis?.risk_level || 'Medium';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {}) : {};

  const getRiskColor = (level) => {
    switch (level) {
      case 'High': return 'text-danger';
      case 'Medium': return 'text-amber';
      case 'Low': return 'text-success';
      default: return 'text-muted-gray';
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'High': return <AlertTriangle className="w-4 h-4" />;
      case 'Medium': return <Shield className="w-4 h-4" />;
      case 'Low': return <CheckCircle className="w-4 h-4" />;
      default: return null;
    }
  };

  const displaySummary = isExpanded ? summary : summary.substring(0, 500);
  const needsExpansion = summary.length > 500;

  return (
    <Card className="p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-azure/20 rounded-lg">
            <FileText className="w-5 h-5 text-azure" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-light-gray">Contract Summary</h3>
            <p className="text-sm text-muted-gray">
              {totalClauses} clauses analyzed in {processingTime}s
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="text-muted-gray hover:text-light-gray"
          >
            <Copy className="w-4 h-4 mr-2" />
            {copied ? 'Copied!' : 'Copy'}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleDownload}
            className="text-muted-gray hover:text-light-gray"
          >
            <Download className="w-4 h-4 mr-2" />
            Download
          </Button>
        </div>
      </div>

      {/* Risk Overview */}
      {Object.keys(riskStats).length > 0 && (
        <div className="grid grid-cols-3 gap-4 mb-6">
          {['High', 'Medium', 'Low'].map(level => (
            <div key={level} className="text-center p-3 bg-charcoal/30 rounded-lg">
              <div className={`flex items-center justify-center mb-2 ${getRiskColor(level)}`}>
                {getRiskIcon(level)}
                <span className="ml-2 font-semibold">{riskStats[level] || 0}</span>
              </div>
              <p className="text-xs text-muted-gray">{level} Risk</p>
            </div>
          ))}
        </div>
      )}

      {/* Summary Content */}
      <div className="prose prose-invert max-w-none">
        <div className="text-light-gray leading-relaxed whitespace-pre-wrap">
          {displaySummary}
          {needsExpansion && !isExpanded && (
            <span className="text-muted-gray">...</span>
          )}
        </div>
        
        {needsExpansion && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="mt-4 text-azure hover:text-azure/80"
          >
            {isExpanded ? (
              <>
                <EyeOff className="w-4 h-4 mr-2" />
                Show Less
              </>
            ) : (
              <>
                <Eye className="w-4 h-4 mr-2" />
                Show More
              </>
            )}
          </Button>
        )}
      </div>

      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-border-dark/50">
        <p className="text-xs text-muted-gray">
          This summary is generated by AI and should be reviewed by a legal professional for accuracy.
        </p>
      </div>
    </Card>
  );
};

export default ContractSummary;
