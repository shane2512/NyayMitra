import React, { useState, useEffect } from 'react';
import { Menu, X, MessageSquare, User, Sparkles, Scale } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from './Button';

const NavigationBar = ({ onChatOpen }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`sticky top-0 z-50 transition-all duration-300 ${
      scrolled ? 'glass shadow-2xl' : 'bg-midnight/80 backdrop-blur-sm'
    } border-b border-border-dark/50`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="p-2 bg-gradient-premium rounded-xl group-hover:shadow-[0_0_20px_rgba(79,157,255,0.5)] transition-all duration-300">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-2xl font-heading font-bold">
                <span className="gradient-text">Nyay</span>
                <span className="text-light-gray">Mitra</span>
              </h1>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-6">
              <Link to="/dashboard" className="text-muted-gray hover:text-azure px-3 py-2 text-sm font-medium transition-colors relative group">
                Dashboard
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-azure scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
              </Link>
              <Link to="/pricing" className="text-muted-gray hover:text-azure px-3 py-2 text-sm font-medium transition-colors relative group">
                Pricing
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-azure scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
              </Link>
              <Link to="/features" className="text-muted-gray hover:text-azure px-3 py-2 text-sm font-medium transition-colors relative group">
                Features
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-azure scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
              </Link>
            </div>
          </div>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={onChatOpen}
              className="!normal-case"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              AI Assistant
            </Button>
            <Button variant="primary" size="sm" glow>
              Get Started
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-light-gray hover:text-azure p-2 transition-colors"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden glass border-t border-border-dark animate-slide-up">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link to="/dashboard" className="text-light-gray hover:text-azure block px-3 py-2 rounded-lg hover:bg-charcoal/50 text-base font-medium transition-all">
              Dashboard
            </Link>
            <Link to="/pricing" className="text-light-gray hover:text-azure block px-3 py-2 rounded-lg hover:bg-charcoal/50 text-base font-medium transition-all">
              Pricing
            </Link>
            <Link to="/features" className="text-light-gray hover:text-azure block px-3 py-2 rounded-lg hover:bg-charcoal/50 text-base font-medium transition-all">
              Features
            </Link>
            <div className="pt-4 pb-3 border-t border-border-dark">
              <div className="space-y-2 px-3">
                <Button variant="ghost" size="sm" onClick={onChatOpen} className="w-full !normal-case">
                  <Sparkles className="w-4 h-4 mr-2" />
                  AI Assistant
                </Button>
                <Button variant="primary" size="sm" className="w-full" glow>
                  Get Started
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default NavigationBar;
