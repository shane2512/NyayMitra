import React from 'react';
import { Github, Twitter, Linkedin, Mail, Scale, Shield, FileText, BarChart3 } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="relative bg-gradient-to-b from-midnight via-charcoal/50 to-midnight border-t border-border-dark/50">
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-midnight via-transparent to-transparent opacity-50" />
      
      <div className="relative max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <div className="p-2 bg-gradient-premium rounded-xl">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-2xl font-heading font-bold">
                <span className="gradient-text">Nyay</span>
                <span className="text-light-gray">Mitra</span>
              </h2>
            </div>
            <p className="text-muted-gray text-sm leading-relaxed mb-6 max-w-md">
              AI-powered legal-tech SaaS platform for contract analysis, risk visualization, 
              and intelligent legal guidance. Empowering businesses with smart contract insights.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="p-2 bg-charcoal/50 rounded-lg text-muted-gray hover:text-azure hover:bg-azure/10 transition-all duration-300">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="p-2 bg-charcoal/50 rounded-lg text-muted-gray hover:text-azure hover:bg-azure/10 transition-all duration-300">
                <Linkedin className="w-5 h-5" />
              </a>
              <a href="#" className="p-2 bg-charcoal/50 rounded-lg text-muted-gray hover:text-azure hover:bg-azure/10 transition-all duration-300">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="p-2 bg-charcoal/50 rounded-lg text-muted-gray hover:text-azure hover:bg-azure/10 transition-all duration-300">
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h3 className="text-light-gray font-heading font-semibold mb-4 flex items-center">
              <FileText className="w-4 h-4 mr-2 text-azure" />
              Product
            </h3>
            <ul className="space-y-3">
              <li><Link to="/dashboard" className="text-muted-gray hover:text-azure text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-azure rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Dashboard
              </Link></li>
              <li><Link to="/pricing" className="text-muted-gray hover:text-azure text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-azure rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Pricing
              </Link></li>
              <li><Link to="/features" className="text-muted-gray hover:text-azure text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-azure rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Features
              </Link></li>
              <li><Link to="/api" className="text-muted-gray hover:text-azure text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-azure rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                API Docs
              </Link></li>
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h3 className="text-light-gray font-heading font-semibold mb-4 flex items-center">
              <Shield className="w-4 h-4 mr-2 text-teal" />
              Legal
            </h3>
            <ul className="space-y-3">
              <li><Link to="/privacy" className="text-muted-gray hover:text-teal text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-teal rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Privacy Policy
              </Link></li>
              <li><Link to="/terms" className="text-muted-gray hover:text-teal text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-teal rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Terms of Service
              </Link></li>
              <li><Link to="/legal/security" className="text-muted-gray hover:text-teal text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-teal rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Security
              </Link></li>
              <li><Link to="/legal/compliance" className="text-muted-gray hover:text-teal text-sm transition-colors flex items-center group">
                <span className="w-1 h-1 bg-teal rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                Compliance
              </Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-border-dark/50">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-muted-gray text-sm">
              © 2024 NyayMitra. All rights reserved.
            </p>
            <div className="flex items-center space-x-2 mt-4 md:mt-0">
              <span className="text-muted-gray text-sm">Built with</span>
              <span className="text-danger animate-pulse">❤️</span>
              <span className="text-muted-gray text-sm">for the legal community</span>
            </div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-azure/10 rounded-full blur-3xl -translate-x-1/2 translate-y-1/2" />
        <div className="absolute bottom-0 right-0 w-32 h-32 bg-teal/10 rounded-full blur-3xl translate-x-1/2 translate-y-1/2" />
      </div>
    </footer>
  );
};

export default Footer;
