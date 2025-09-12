import React from 'react';
import { X, TrendingUp, BarChart3, PieChart, Target, ArrowUp, ArrowDown } from 'lucide-react';
import { PieChart as RechartsPieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const SimulationModal = ({ simulation, riskReport, onClose }) => {
  if (!simulation) return null;

  const pieData = [
    { name: 'High Risk', value: simulation.risk_distribution?.High || 0, color: '#ef4444' },
    { name: 'Medium Risk', value: simulation.risk_distribution?.Medium || 0, color: '#f59e0b' },
    { name: 'Low Risk', value: simulation.risk_distribution?.Low || 0, color: '#10b981' }
  ].filter(item => item.value > 0);

  const barData = [
    { name: 'High', count: simulation.risk_distribution?.High || 0, percentage: simulation.risk_percentages?.High || 0 },
    { name: 'Medium', count: simulation.risk_distribution?.Medium || 0, percentage: simulation.risk_percentages?.Medium || 0 },
    { name: 'Low', count: simulation.risk_distribution?.Low || 0, percentage: simulation.risk_percentages?.Low || 0 }
  ];

  // Mock negotiation scenarios data
  const scenarioData = [
    { scenario: 'Current State', score: 45, risks: simulation.risk_distribution?.High || 0 },
    { scenario: 'Minor Changes', score: 65, risks: Math.max(0, (simulation.risk_distribution?.High || 0) - 1) },
    { scenario: 'Major Revision', score: 85, risks: Math.max(0, Math.floor((simulation.risk_distribution?.High || 0) / 2)) },
    { scenario: 'Complete Rewrite', score: 95, risks: 0 }
  ];

  const timelineData = [
    { month: 'Month 1', currentRisk: 85, improvedRisk: 60 },
    { month: 'Month 3', currentRisk: 85, improvedRisk: 45 },
    { month: 'Month 6', currentRisk: 85, improvedRisk: 30 },
    { month: 'Month 12', currentRisk: 85, improvedRisk: 15 },
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BarChart3 className="w-6 h-6" />
              <div>
                <h2 className="text-xl font-bold">Contract Risk Simulation</h2>
                <p className="text-blue-100 text-sm">Advanced analytics and negotiation scenarios</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-blue-800 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-80px)]">
          {/* Overview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-red-600 text-sm font-medium">High Risk Clauses</p>
                  <p className="text-2xl font-bold text-red-700">{simulation.risk_distribution?.High || 0}</p>
                </div>
                <ArrowDown className="w-8 h-8 text-red-500" />
              </div>
              <p className="text-xs text-red-600 mt-2">Requires immediate attention</p>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-yellow-600 text-sm font-medium">Medium Risk</p>
                  <p className="text-2xl font-bold text-yellow-700">{simulation.risk_distribution?.Medium || 0}</p>
                </div>
                <Target className="w-8 h-8 text-yellow-500" />
              </div>
              <p className="text-xs text-yellow-600 mt-2">Monitor and review</p>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-600 text-sm font-medium">Low Risk</p>
                  <p className="text-2xl font-bold text-green-700">{simulation.risk_distribution?.Low || 0}</p>
                </div>
                <ArrowUp className="w-8 h-8 text-green-500" />
              </div>
              <p className="text-xs text-green-600 mt-2">Generally acceptable</p>
            </div>

            <div className={`border rounded-lg p-4 ${
              simulation.safety_index === 'High Risk' ? 'bg-red-50 border-red-200' :
              simulation.safety_index === 'Low Risk' ? 'bg-green-50 border-green-200' :
              'bg-yellow-50 border-yellow-200'
            }`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-sm font-medium ${
                    simulation.safety_index === 'High Risk' ? 'text-red-600' :
                    simulation.safety_index === 'Low Risk' ? 'text-green-600' :
                    'text-yellow-600'
                  }`}>Safety Index</p>
                  <p className={`text-2xl font-bold ${
                    simulation.safety_index === 'High Risk' ? 'text-red-700' :
                    simulation.safety_index === 'Low Risk' ? 'text-green-700' :
                    'text-yellow-700'
                  }`}>{simulation.safety_index}</p>
                </div>
                <TrendingUp className={`w-8 h-8 ${
                  simulation.safety_index === 'High Risk' ? 'text-red-500' :
                  simulation.safety_index === 'Low Risk' ? 'text-green-500' :
                  'text-yellow-500'
                }`} />
              </div>
              <p className={`text-xs mt-2 ${
                simulation.safety_index === 'High Risk' ? 'text-red-600' :
                simulation.safety_index === 'Low Risk' ? 'text-green-600' :
                'text-yellow-600'
              }`}>Overall contract safety</p>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Risk Distribution Pie Chart */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">Risk Distribution</h3>
              {pieData.length > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <RechartsPieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      dataKey="value"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RechartsPieChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-64 flex items-center justify-center text-gray-500">
                  No risk data available
                </div>
              )}
            </div>

            {/* Risk Breakdown Bar Chart */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">Risk Breakdown</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={barData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Negotiation Scenarios */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">Negotiation Scenarios</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={scenarioData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="scenario" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="score" fill="#10b981" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Risk Improvement Timeline */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-900">Risk Improvement Timeline</h3>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={timelineData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="currentRisk" stroke="#ef4444" strokeWidth={2} name="Current Risk" />
                  <Line type="monotone" dataKey="improvedRisk" stroke="#10b981" strokeWidth={2} name="Improved Risk" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Simulation Results */}
          {simulation.simulation && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold mb-3 text-blue-900 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2" />
                AI Simulation Results
              </h3>
              <div className="text-blue-800 whitespace-pre-wrap text-sm leading-relaxed">
                {simulation.simulation}
              </div>
            </div>
          )}

          {/* Recommendations */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Recommendations</h3>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-red-600 text-xs font-bold">1</span>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Address High-Risk Clauses</p>
                  <p className="text-gray-600 text-sm">Focus on renegotiating the {simulation.risk_distribution?.High || 0} high-risk clauses first, as they pose the greatest legal and financial exposure.</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-yellow-600 text-xs font-bold">2</span>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Review Medium-Risk Items</p>
                  <p className="text-gray-600 text-sm">Monitor the {simulation.risk_distribution?.Medium || 0} medium-risk clauses for potential improvements during contract review cycles.</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-green-600 text-xs font-bold">3</span>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Leverage Low-Risk Areas</p>
                  <p className="text-gray-600 text-sm">Use the {simulation.risk_distribution?.Low || 0} well-balanced clauses as templates for improving other sections of the contract.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimulationModal;
