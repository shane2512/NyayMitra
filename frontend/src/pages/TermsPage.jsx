import React from 'react';
import { FileText, Scale, Shield, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import NavigationBar from '../components/ui/NavigationBar';
import Footer from '../components/ui/Footer';
import Card from '../components/ui/Card';

const TermsPage = () => {
  const sections = [
    {
      title: "1. Acceptance of Terms",
      content: "By accessing and using NyayMitra, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services."
    },
    {
      title: "2. Service Description",
      content: "NyayMitra provides AI-powered contract analysis, risk assessment, and legal document processing services. Our platform offers automated insights and should not be considered as legal advice."
    },
    {
      title: "3. User Responsibilities",
      content: "You are responsible for maintaining the confidentiality of your account, ensuring the accuracy of uploaded documents, and using the service in compliance with applicable laws."
    },
    {
      title: "4. Intellectual Property",
      content: "All content, features, and functionality of NyayMitra are owned by us and are protected by international copyright, trademark, and other intellectual property laws."
    },
    {
      title: "5. Limitation of Liability",
      content: "NyayMitra provides analysis tools but is not a substitute for professional legal advice. We are not liable for decisions made based on our analysis. Always consult qualified legal professionals for important matters."
    },
    {
      title: "6. Data Processing",
      content: "We process your contracts temporarily for analysis purposes only. Documents are automatically deleted after processing unless you choose to save them in your account."
    },
    {
      title: "7. Payment Terms",
      content: "Subscription fees are billed in advance on a monthly or annual basis. All payments are non-refundable except as required by law or as explicitly stated in our refund policy."
    },
    {
      title: "8. Termination",
      content: "Either party may terminate the agreement at any time. Upon termination, your access to the service will cease, and any stored data will be deleted according to our data retention policy."
    }
  ];

  const importantNotes = [
    "NyayMitra is not a law firm and does not provide legal advice",
    "Our AI analysis is meant to assist, not replace, professional legal review",
    "You retain all rights to your uploaded documents",
    "We comply with GDPR, CCPA, and other data protection regulations"
  ];

  return (
    <div className="min-h-screen bg-midnight">
      <NavigationBar />
      
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-96 h-96 bg-azure/10 rounded-full blur-3xl" />
        </div>
        
        <div className="relative max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-premium rounded-2xl mb-6">
              <Scale className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-heading font-bold text-light-gray mb-6">
              Terms of Service
            </h1>
            <p className="text-xl text-muted-gray">
              Please read these terms carefully before using NyayMitra
            </p>
            <p className="text-sm text-muted-gray mt-4">
              Effective Date: January 1, 2024
            </p>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Important Notice */}
          <Card variant="glass" className="p-8 mb-12 border-amber/30">
            <div className="flex items-start space-x-4">
              <AlertTriangle className="w-6 h-6 text-amber flex-shrink-0 mt-1" />
              <div>
                <h2 className="text-xl font-heading font-semibold text-light-gray mb-3">
                  Important Legal Notice
                </h2>
                <ul className="space-y-2 text-muted-gray">
                  {importantNotes.map((note, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-teal mr-2 flex-shrink-0 mt-0.5" />
                      <span>{note}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </Card>

          {/* Terms Sections */}
          <div className="space-y-8">
            {sections.map((section, index) => (
              <Card key={index} variant="glass" className="p-6">
                <h3 className="text-xl font-heading font-semibold text-light-gray mb-4">
                  {section.title}
                </h3>
                <p className="text-muted-gray leading-relaxed">
                  {section.content}
                </p>
              </Card>
            ))}
          </div>

          {/* Additional Terms */}
          <Card variant="glass" className="p-8 mt-12">
            <div className="flex items-start space-x-4">
              <Info className="w-6 h-6 text-azure flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-xl font-heading font-semibold text-light-gray mb-4">
                  Additional Terms
                </h3>
                <div className="space-y-4 text-muted-gray">
                  <div>
                    <h4 className="font-semibold text-light-gray mb-2">Governing Law</h4>
                    <p>These terms are governed by the laws of the United States and the State of California.</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-light-gray mb-2">Changes to Terms</h4>
                    <p>We reserve the right to modify these terms at any time. Continued use after changes constitutes acceptance.</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-light-gray mb-2">Contact Information</h4>
                    <p>For questions about these terms, contact us at legal@nyaymitra.com</p>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default TermsPage;
