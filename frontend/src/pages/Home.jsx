import React from 'react';
import FileUploader from '../components/FileUploader';
import RiskSummary from '../components/RiskSummary';
import SimulationCharts from '../components/SimulationCharts';

const Home = () => {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">NyayMitra - Legal Contract Analyzer</h1>
            <FileUploader />
            <div className="mt-8">
                <RiskSummary />
                <SimulationCharts />
            </div>
        </div>
    );
};

export default Home;