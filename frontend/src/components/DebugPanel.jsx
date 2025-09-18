import React, { useState, useEffect } from 'react';

const DebugPanel = ({ isVisible, analysisResult, error, isLoading, onClose }) => {
  const [backendStatus, setBackendStatus] = useState(null);
  
  useEffect(() => {
    // Test backend connectivity
    const testBackend = async () => {
      try {
        const response = await fetch('http://localhost:5000/health');
        const data = await response.json();
        setBackendStatus({ status: 'connected', data });
      } catch (err) {
        setBackendStatus({ status: 'error', error: err.message });
      }
    };
    
    if (isVisible) {
      testBackend();
    }
  }, [isVisible]);
  
  if (!isVisible) return null;
  
  return (
    <div className="fixed bottom-4 right-4 bg-gray-900 text-white p-4 rounded-lg shadow-lg max-w-md z-50">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-bold">🔍 Debug Panel</h3>
        <button 
          onClick={onClose}
          className="text-gray-400 hover:text-white text-xl leading-none"
        >
          ×
        </button>
      </div>
      
      <div className="space-y-2 text-sm">
        <div>
          <strong>Backend Status:</strong>{' '}
          {backendStatus ? (
            backendStatus.status === 'connected' ? (
              <span className="text-green-400">✅ Connected</span>
            ) : (
              <span className="text-red-400">❌ {backendStatus.error}</span>
            )
          ) : (
            <span className="text-yellow-400">⏳ Testing...</span>
          )}
        </div>
        
        <div>
          <strong>Loading State:</strong>{' '}
          <span className={isLoading ? 'text-yellow-400' : 'text-gray-400'}>
            {isLoading ? '⏳ Analyzing...' : '✅ Idle'}
          </span>
        </div>
        
        <div>
          <strong>Error State:</strong>{' '}
          {error ? (
            <div className="text-red-400">
              <div>❌ {error}</div>
              {typeof error === 'object' && (
                <div className="text-xs mt-1 p-2 bg-red-900/20 rounded">
                  <pre>{JSON.stringify(error, null, 2)}</pre>
                </div>
              )}
            </div>
          ) : (
            <span className="text-green-400">✅ No errors</span>
          )}
        </div>
        
        <div>
          <strong>Analysis Result:</strong>{' '}
          {analysisResult ? (
            <span className="text-green-400">
              ✅ Present ({analysisResult.status})
            </span>
          ) : (
            <span className="text-gray-400">⭕ None</span>
          )}
        </div>
        
        {analysisResult && (
          <div className="mt-2 p-2 bg-gray-800 rounded text-xs">
            <div>Status: {analysisResult.status}</div>
            <div>Summary: {analysisResult.summary ? `${analysisResult.summary.length} chars` : 'None'}</div>
            <div>Risk Report: {analysisResult.risk_report ? `${Object.keys(analysisResult.risk_report).length} entries` : 'None'}</div>
            <div>Processing Time: {analysisResult.processing_time || 'Unknown'}s</div>
          </div>
        )}
      </div>
      
      <button 
        onClick={() => console.log('Current State:', { analysisResult, error, isLoading })}
        className="mt-2 px-2 py-1 bg-blue-600 text-white rounded text-xs"
      >
        Log State to Console
      </button>
    </div>
  );
};

export default DebugPanel;
