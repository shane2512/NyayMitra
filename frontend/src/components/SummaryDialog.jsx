import React from 'react';

const SummaryDialog = ({ open, summary, onClose }) => {
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-40"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl shadow-2xl p-8 max-w-xl w-full relative animate-fade-in max-h-[80vh] overflow-y-auto"
        onClick={e => e.stopPropagation()}
      >
        <button
          className="absolute top-3 right-3 text-gray-400 hover:text-gray-700"
          onClick={onClose}
        >
          <span className="text-2xl font-bold">&times;</span>
        </button>
        <h2 className="text-xl font-bold mb-4 text-blue-800">Contract Summary</h2>
        <div className="prose max-w-none text-gray-800 whitespace-pre-wrap leading-relaxed max-h-[60vh] overflow-y-auto">
          {formatSummary(summary)}
        </div>
      </div>
    </div>
  );
};

function formatSummary(summary) {
  if (!summary) return <span className="text-gray-400">No summary available.</span>;
  // Basic formatting: bullet points for sections, highlight key phrases
  const lines = summary.split(/\n|\r/).filter(Boolean);
  return (
    <ul className="list-disc ml-6 space-y-2">
      {lines.map((line, idx) => (
        <li key={idx}>{line}</li>
      ))}
    </ul>
  );
}

export default SummaryDialog;
