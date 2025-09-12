import React, { useEffect, useState } from 'react';
import FileUploader from '../components/FileUploader';
import RiskSummary from '../components/RiskSummary';
import SimulationCharts from '../components/SimulationCharts';

const Dashboard = () => {
    const [riskReport, setRiskReport] = useState(null);
    const [summary, setSummary] = useState(null);
    const [simulationResults, setSimulationResults] = useState(null);

    const handleFileUpload = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            setRiskReport(data.risk_report);
            setSummary(data.summary);
            setSimulationResults(data.simulation);
        } else {
            console.error('Error analyzing the contract');
        }
    };

    return (
        <div className="dashboard">
            <h1 className="text-2xl font-bold mb-4">Contract Analysis Dashboard</h1>
            <FileUploader onFileUpload={handleFileUpload} />
            {riskReport && (
                <div className="results">
                    <RiskSummary report={riskReport} />
                    <SimulationCharts results={simulationResults} />
                </div>
            )}
        </div>
    );
};

export default Dashboard;