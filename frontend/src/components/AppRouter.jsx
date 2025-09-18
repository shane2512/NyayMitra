import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import NavigationBar from './ui/NavigationBar';
import Footer from './ui/Footer';
import LandingPage from './pages/LandingPage';
import PricingPage from './pages/PricingPage';
import PrivacyPage from './pages/PrivacyPage';
import TermsPage from './pages/TermsPage';
import ChatInterface from './ChatInterface';

// Import the existing dashboard component (App.jsx content)
import Dashboard from '../App';

const AppRouter = () => {
  const [showChat, setShowChat] = useState(false);

  const handleGetStarted = () => {
    // Navigate to dashboard or show file upload
    window.location.href = '/dashboard';
  };

  return (
    <Router>
      <div className="min-h-screen bg-midnight">
        <NavigationBar onChatOpen={() => setShowChat(true)} />
        
        <Routes>
          <Route 
            path="/" 
            element={<LandingPage onGetStarted={handleGetStarted} />} 
          />
          <Route 
            path="/dashboard" 
            element={<Dashboard />} 
          />
          <Route 
            path="/pricing" 
            element={<PricingPage />} 
          />
          <Route 
            path="/privacy" 
            element={<PrivacyPage />} 
          />
          <Route 
            path="/terms" 
            element={<TermsPage />} 
          />
          <Route 
            path="/features" 
            element={<Navigate to="/#features" replace />} 
          />
          {/* Redirect old routes */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Global Chat Interface */}
        {showChat && (
          <ChatInterface
            isOpen={showChat}
            onClose={() => setShowChat(false)}
            contractContext={null}
          />
        )}

        <Footer />
      </div>
    </Router>
  );
};

export default AppRouter;
