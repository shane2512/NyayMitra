import React, { useState } from 'react';
import { Globe, Copy, Download, Languages, CheckCircle, AlertTriangle } from 'lucide-react';
import Card from './ui/Card';
import Button from './ui/Button';

const TranslatedSummary = ({ translatedSummary, language, interests }) => {
  const [copied, setCopied] = useState(false);

  if (!translatedSummary) {
    return null; // Don't render if no translated summary
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(translatedSummary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([translatedSummary], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `contract-summary-${language}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getLanguageName = (code) => {
    const languages = {
      'en': 'English',
      'hi': 'Hindi',
      'es': 'Spanish',
      'fr': 'French',
      'de': 'German',
      'zh': 'Chinese',
      'ja': 'Japanese',
      'ko': 'Korean',
      'ar': 'Arabic',
      'pt': 'Portuguese',
      'ru': 'Russian',
      'it': 'Italian'
    };
    return languages[code] || code.toUpperCase();
  };

  const getInterestName = (interest) => {
    const interestNames = {
      'financial': 'Financial Obligations',
      'termination': 'Termination Clauses',
      'liability': 'Liability & Risk',
      'intellectual_property': 'Intellectual Property',
      'confidentiality': 'Confidentiality',
      'dispute_resolution': 'Dispute Resolution',
      'compliance': 'Compliance & Regulatory',
      'payment_terms': 'Payment Terms',
      'delivery_schedule': 'Delivery & Performance',
      'warranties': 'Warranties & Guarantees',
      'indemnification': 'Indemnification',
      'force_majeure': 'Force Majeure'
    };
    return interestNames[interest] || interest.replace('_', ' ').toUpperCase();
  };

  return (
    <Card className="p-6 border-teal/20 bg-gradient-to-br from-teal/5 to-teal/10">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-teal/20 rounded-lg">
            <Globe className="w-5 h-5 text-teal" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-light-gray">
              Translated Summary
            </h3>
            <div className="flex items-center space-x-2 text-sm text-muted-gray">
              <Languages className="w-4 h-4" />
              <span>{getLanguageName(language)}</span>
              {interests && interests.length > 0 && (
                <>
                  <span>•</span>
                  <span>{interests.length} focus area{interests.length > 1 ? 's' : ''}</span>
                </>
              )}
            </div>
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

      {/* Focus Areas */}
      {interests && interests.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-medium text-light-gray mb-3">Focus Areas:</h4>
          <div className="flex flex-wrap gap-2">
            {interests.map((interest, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-teal/20 text-teal text-xs rounded-full border border-teal/30"
              >
                {getInterestName(interest)}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Translated Content */}
      <div className="prose prose-invert max-w-none">
        <div className="text-light-gray leading-relaxed whitespace-pre-wrap">
          {translatedSummary}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-border-dark/50">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="w-4 h-4 text-amber mt-0.5 flex-shrink-0" />
          <p className="text-xs text-muted-gray">
            This is an AI-generated translation focused on your selected interests. 
            For legal accuracy, please consult with a qualified legal professional 
            who speaks {getLanguageName(language)}.
          </p>
        </div>
      </div>
    </Card>
  );
};

export default TranslatedSummary;
