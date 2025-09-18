import React from 'react';
import { Shield, Lock, Eye, Database, Globe, Users, FileText, AlertCircle } from 'lucide-react';
import NavigationBar from '../components/ui/NavigationBar';
import Footer from '../components/ui/Footer';
import Card from '../components/ui/Card';

const PrivacyPage = () => {
  const sections = [
    {
      icon: <Database className="w-5 h-5" />,
      title: "Data Collection",
      content: "We collect only essential information needed to provide our services. This includes uploaded contracts (processed temporarily), user account information, and usage analytics to improve our platform."
    },
    {
      icon: <Lock className="w-5 h-5" />,
      title: "Data Security",
      content: "Your data is encrypted using AES-256 encryption both in transit and at rest. We employ bank-level security measures and regular security audits to ensure your information remains protected."
    },
    {
      icon: <Eye className="w-5 h-5" />,
      title: "Data Usage",
      content: "We use your data solely to provide and improve our contract analysis services. We never sell your data to third parties or use it for advertising purposes."
    },
    {
      icon: <Globe className="w-5 h-5" />,
      title: "Data Retention",
      content: "Contract data is temporarily processed and automatically deleted after analysis. Account data is retained as long as your account is active. You can request deletion at any time."
    },
    {
      icon: <Users className="w-5 h-5" />,
      title: "Third-Party Services",
      content: "We use trusted third-party services for payment processing and infrastructure. These partners are carefully vetted and bound by strict confidentiality agreements."
    },
    {
      icon: <FileText className="w-5 h-5" />,
      title: "Your Rights",
      content: "You have the right to access, correct, or delete your personal data. You can export your data or close your account at any time through your account settings."
    }
  ];

  return (
    <div className="min-h-screen bg-midnight">
      <NavigationBar />
      
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-0 right-0 w-96 h-96 bg-azure/10 rounded-full blur-3xl" />
        </div>
        
        <div className="relative max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-premium rounded-2xl mb-6">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-heading font-bold text-light-gray mb-6">
              Privacy Policy
            </h1>
            <p className="text-xl text-muted-gray">
              Your privacy is our priority. Learn how we protect and handle your data.
            </p>
            <p className="text-sm text-muted-gray mt-4">
              Last updated: January 2024
            </p>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Key Points */}
          <Card variant="glass" className="p-8 mb-12">
            <div className="flex items-start space-x-4">
              <AlertCircle className="w-6 h-6 text-teal flex-shrink-0 mt-1" />
              <div>
                <h2 className="text-xl font-heading font-semibold text-light-gray mb-3">
                  Key Privacy Commitments
                </h2>
                <ul className="space-y-2 text-muted-gray">
                  <li className="flex items-start">
                    <span className="text-teal mr-2">•</span>
                    We never sell or share your personal data with third parties
                  </li>
                  <li className="flex items-start">
                    <span className="text-teal mr-2">•</span>
                    Contracts are processed temporarily and deleted after analysis
                  </li>
                  <li className="flex items-start">
                    <span className="text-teal mr-2">•</span>
                    You maintain full ownership of your data
                  </li>
                  <li className="flex items-start">
                    <span className="text-teal mr-2">•</span>
                    We comply with GDPR, CCPA, and other privacy regulations
                  </li>
                </ul>
              </div>
            </div>
          </Card>

          {/* Detailed Sections */}
          <div className="space-y-8">
            {sections.map((section, index) => (
              <Card key={index} variant="glass" className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-azure/20 rounded-xl">
                    <div className="text-azure">
                      {section.icon}
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-heading font-semibold text-light-gray mb-3">
                      {section.title}
                    </h3>
                    <p className="text-muted-gray leading-relaxed">
                      {section.content}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Contact Section */}
          <Card variant="glass" className="p-8 mt-12 text-center">
            <h3 className="text-2xl font-heading font-semibold text-light-gray mb-4">
              Questions About Privacy?
            </h3>
            <p className="text-muted-gray mb-6">
              If you have any questions about our privacy practices or how we handle your data, 
              please don't hesitate to contact us.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="mailto:privacy@nyaymitra.com" className="text-azure hover:text-teal transition-colors">
                privacy@nyaymitra.com
              </a>
              <span className="text-muted-gray hidden sm:block">•</span>
              <a href="/contact" className="text-azure hover:text-teal transition-colors">
                Contact Support
              </a>
            </div>
          </Card>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default PrivacyPage;
