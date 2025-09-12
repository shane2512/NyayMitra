import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const SimulationCharts = ({ simulation }) => {
  if (!simulation) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        <p>No simulation data available</p>
      </div>
    );
  }

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

  return (
    <div className="h-full overflow-y-auto space-y-6">
      <h2 className="text-xl font-bold text-gray-900 sticky top-0 bg-white pb-2">
        Risk Analysis
      </h2>
      
      {/* Safety Index Badge */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="text-center">
          <h3 className="text-lg font-semibold mb-2">Overall Safety</h3>
          <div className={`inline-block px-4 py-2 rounded-full text-sm font-medium ${
            simulation.safety_index === 'High Risk' ? 'bg-red-100 text-red-800' :
            simulation.safety_index === 'Low Risk' ? 'bg-green-100 text-green-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {simulation.safety_index}
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {simulation.total_clauses} total clauses analyzed
          </p>
        </div>
      </div>

      {/* Pie Chart */}
      {pieData.length > 0 && (
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-lg font-semibold mb-4 text-center">Risk Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Bar Chart */}
      <div className="bg-white p-4 rounded-lg border">
        <h3 className="text-lg font-semibold mb-4 text-center">Risk Breakdown</h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={barData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip formatter={(value, name) => [value, name === 'count' ? 'Clauses' : 'Percentage']} />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Risk Stats */}
      <div className="grid grid-cols-3 gap-2">
        <div className="bg-red-50 p-3 rounded-lg text-center border border-red-200">
          <div className="text-2xl font-bold text-red-600">
            {simulation.risk_distribution?.High || 0}
          </div>
          <div className="text-xs text-red-800">High Risk</div>
        </div>
        <div className="bg-yellow-50 p-3 rounded-lg text-center border border-yellow-200">
          <div className="text-2xl font-bold text-yellow-600">
            {simulation.risk_distribution?.Medium || 0}
          </div>
          <div className="text-xs text-yellow-800">Medium Risk</div>
        </div>
        <div className="bg-green-50 p-3 rounded-lg text-center border border-green-200">
          <div className="text-2xl font-bold text-green-600">
            {simulation.risk_distribution?.Low || 0}
          </div>
          <div className="text-xs text-green-800">Low Risk</div>
        </div>
      </div>
    </div>
  );
};

export default SimulationCharts;