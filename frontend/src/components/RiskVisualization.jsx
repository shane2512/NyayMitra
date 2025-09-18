import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, Shield, CheckCircle, TrendingUp } from 'lucide-react';
import Card from './ui/Card';

const RiskVisualization = ({ simulation, riskReport }) => {
  if (!simulation || !riskReport) {
    return (
      <Card className="p-6">
        <div className="text-center text-muted-gray">
          <BarChart className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>Risk visualization will appear here after analysis</p>
        </div>
      </Card>
    );
  }

  const { risk_distribution, risk_percentages } = simulation;
  
  // Prepare data for charts
  const pieData = [
    { name: 'High Risk', value: risk_distribution?.High || 0, color: '#ef4444' },
    { name: 'Medium Risk', value: risk_distribution?.Medium || 0, color: '#f59e0b' },
    { name: 'Low Risk', value: risk_distribution?.Low || 0, color: '#10b981' }
  ].filter(item => item.value > 0);

  const barData = [
    { name: 'High', value: risk_percentages?.High || 0, color: '#ef4444' },
    { name: 'Medium', value: risk_percentages?.Medium || 0, color: '#f59e0b' },
    { name: 'Low', value: risk_percentages?.Low || 0, color: '#10b981' }
  ];

  const getRiskIcon = (level) => {
    switch (level) {
      case 'High': return <AlertTriangle className="w-5 h-5 text-danger" />;
      case 'Medium': return <Shield className="w-5 h-5 text-amber" />;
      case 'Low': return <CheckCircle className="w-5 h-5 text-success" />;
      default: return <TrendingUp className="w-5 h-5 text-muted-gray" />;
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'High': return 'text-danger';
      case 'Medium': return 'text-amber';
      case 'Low': return 'text-success';
      default: return 'text-muted-gray';
    }
  };

  return (
    <div className="space-y-6">
      {/* Risk Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-4 bg-gradient-to-br from-danger/10 to-danger/5 border-danger/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-gray mb-1">High Risk</p>
              <p className="text-2xl font-bold text-danger">{risk_distribution?.High || 0}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-danger" />
          </div>
        </Card>
        
        <Card className="p-4 bg-gradient-to-br from-amber/10 to-amber/5 border-amber/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-gray mb-1">Medium Risk</p>
              <p className="text-2xl font-bold text-amber">{risk_distribution?.Medium || 0}</p>
            </div>
            <Shield className="w-8 h-8 text-amber" />
          </div>
        </Card>
        
        <Card className="p-4 bg-gradient-to-br from-success/10 to-success/5 border-success/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-gray mb-1">Low Risk</p>
              <p className="text-2xl font-bold text-success">{risk_distribution?.Low || 0}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-success" />
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-light-gray mb-4">Risk Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
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
        </Card>

        {/* Bar Chart */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-light-gray mb-4">Risk Percentages</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1f2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="value" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Risk Details */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-light-gray mb-4">Clause Risk Breakdown</h3>
        <div className="space-y-3">
          {Object.entries(riskReport).map(([clauseId, details]) => {
            const riskLevel = details.analysis?.risk_level || 'Medium';
            return (
              <div key={clauseId} className="flex items-start space-x-3 p-3 bg-charcoal/30 rounded-lg">
                {getRiskIcon(riskLevel)}
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="font-medium text-light-gray">{clauseId}</h4>
                    <span className={`text-sm font-medium ${getRiskColor(riskLevel)}`}>
                      {riskLevel} Risk
                    </span>
                  </div>
                  <p className="text-sm text-muted-gray mb-2">
                    {details.analysis?.analysis || 'No analysis available'}
                  </p>
                  <p className="text-xs text-muted-gray/70 line-clamp-2">
                    {details.text}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};

export default RiskVisualization;
