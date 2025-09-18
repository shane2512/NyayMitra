import React from 'react';
import { motion } from 'framer-motion';
import { Scale, FileText, AlertTriangle, CheckCircle, Users, Globe, Shield, Gavel } from 'lucide-react';
import Card from '../ui/Card';

const TermsPage = () => {
  const keyTerms = [
    {
      icon: <FileText className="w-6 h-6 text-azure" />,
      title: "Service Usage",
      description: "Guidelines for using our AI-powered contract analysis platform responsibly and effectively."
    },
    {
      icon: <Users className="w-6 h-6 text-teal" />,
      title: "User Responsibilities",
      description: "Your obligations when using NyayMitra, including data accuracy and compliance requirements."
    },
    {
      icon: <Scale className="w-6 h-6 text-amber" />,
      title: "Legal Limitations",
      description: "Important disclaimers about the scope and limitations of our AI legal assistance."
    },
    {
      icon: <CheckCircle className="w-6 h-6 text-teal" />,
      title: "Service Availability",
      description: "Our commitments regarding platform uptime, support, and service level agreements."
    }
  ];

  return (
    <div className="min-h-screen bg-midnight py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center px-4 py-2 bg-charcoal/50 rounded-full border border-border-dark mb-6">
            <Scale className="w-4 h-4 text-azure mr-2" />
            <span className="text-sm text-light-gray">Terms of Service</span>
          </div>
          
          <h1 className="text-5xl font-legal font-bold text-light-gray mb-6">
            Terms of Service
          </h1>
          
          <p className="text-xl text-muted-gray max-w-3xl mx-auto leading-relaxed">
            These terms govern your use of NyayMitra's AI-powered legal technology platform. 
            Please read them carefully before using our services.
          </p>
          
          <div className="mt-6 text-sm text-muted-gray">
            Last updated: January 15, 2024
          </div>
        </motion.div>

        {/* Key Terms Overview */}
        <section className="mb-16">
          <h2 className="text-3xl font-legal font-bold text-light-gray text-center mb-12">
            Key Terms Overview
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {keyTerms.map((term, index) => (
              <motion.div
                key={term.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card variant="glass" className="p-6 h-full">
                  <div className="flex items-center mb-4">
                    <div className="p-3 bg-charcoal rounded-xl mr-4">
                      {term.icon}
                    </div>
                    <h3 className="text-xl font-legal font-semibold text-light-gray">
                      {term.title}
                    </h3>
                  </div>
                  <p className="text-muted-gray leading-relaxed">
                    {term.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Detailed Terms */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-12"
        >
          {/* Acceptance of Terms */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              1. Acceptance of Terms
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-4 text-muted-gray leading-relaxed">
                <p>
                  By accessing or using NyayMitra's services, you agree to be bound by these 
                  Terms of Service and our Privacy Policy. If you do not agree to these terms, 
                  please do not use our services.
                </p>
                <p>
                  These terms constitute a legally binding agreement between you and NyayMitra 
                  Technologies Pvt. Ltd. ("NyayMitra," "we," "us," or "our").
                </p>
              </div>
            </Card>
          </section>

          {/* Service Description */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              2. Service Description
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-6">
                <div>
                  <p className="text-muted-gray leading-relaxed mb-4">
                    NyayMitra provides AI-powered legal technology services including:
                  </p>
                  <ul className="text-muted-gray space-y-2 ml-6">
                    <li>• Contract analysis and risk assessment</li>
                    <li>• AI legal assistant and chat functionality</li>
                    <li>• Multi-language contract translation and summarization</li>
                    <li>• Negotiation simulation and guidance</li>
                    <li>• Legal document management and collaboration tools</li>
                  </ul>
                </div>
                
                <div className="bg-amber/10 border border-amber/20 rounded-lg p-6">
                  <div className="flex items-start space-x-3">
                    <AlertTriangle className="w-6 h-6 text-amber flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-legal font-semibold text-amber mb-2">Important Disclaimer</h3>
                      <p className="text-light-gray text-sm leading-relaxed">
                        Our services provide AI-powered analysis and guidance but do not constitute 
                        legal advice. Always consult with qualified legal professionals for specific 
                        legal matters.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </section>

          {/* User Accounts */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              3. User Accounts and Registration
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Account Creation
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    To use our services, you must create an account and provide accurate, 
                    complete information. You are responsible for maintaining the security 
                    of your account credentials.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Eligibility
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    You must be at least 18 years old and have the legal capacity to enter 
                    into contracts. By using our services, you represent that you meet these 
                    requirements.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Account Responsibility
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Keep your login credentials secure and confidential</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Notify us immediately of any unauthorized access</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Accept responsibility for all activities under your account</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Provide accurate and up-to-date information</span>
                    </li>
                  </ul>
                </div>
              </div>
            </Card>
          </section>

          {/* Acceptable Use */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              4. Acceptable Use Policy
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-teal mb-4">
                    Permitted Uses
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-teal flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Analyze legitimate legal contracts and documents</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-teal flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Use AI assistance for legal research and guidance</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-teal flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Collaborate with team members on legal matters</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-teal flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Export and share analysis results as needed</span>
                    </li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-danger mb-4">
                    Prohibited Uses
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li className="flex items-start">
                      <AlertTriangle className="w-4 h-4 text-danger flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Upload illegal, fraudulent, or malicious content</span>
                    </li>
                    <li className="flex items-start">
                      <AlertTriangle className="w-4 h-4 text-danger flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Violate any applicable laws or regulations</span>
                    </li>
                    <li className="flex items-start">
                      <AlertTriangle className="w-4 h-4 text-danger flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Infringe on intellectual property rights</span>
                    </li>
                    <li className="flex items-start">
                      <AlertTriangle className="w-4 h-4 text-danger flex-shrink-0 mt-1 mr-2" />
                      <span className="text-sm">Attempt to reverse engineer or hack our systems</span>
                    </li>
                  </ul>
                </div>
              </div>
            </Card>
          </section>

          {/* Payment Terms */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              5. Payment and Billing
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Subscription Plans
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    Our services are offered through various subscription plans. Pricing 
                    and features are detailed on our pricing page and may change with notice.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Payment Terms
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li>• Payments are due in advance for each billing period</li>
                    <li>• All fees are non-refundable except as required by law</li>
                    <li>• We may suspend services for non-payment after notice</li>
                    <li>• You're responsible for all taxes and fees</li>
                  </ul>
                </div>
              </div>
            </Card>
          </section>

          {/* Disclaimers */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              6. Disclaimers and Limitations
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-6">
                <div className="bg-danger/10 border border-danger/20 rounded-lg p-6">
                  <div className="flex items-start space-x-3">
                    <Gavel className="w-6 h-6 text-danger flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="text-xl font-legal font-semibold text-danger mb-3">
                        Not Legal Advice
                      </h3>
                      <p className="text-light-gray leading-relaxed">
                        <strong>NyayMitra provides AI-powered analysis tools, not legal advice.</strong> 
                        Our services are designed to assist with document analysis and provide 
                        general information, but should not replace consultation with qualified 
                        legal professionals.
                      </p>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Service Availability
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    We strive for high availability but cannot guarantee uninterrupted service. 
                    We may perform maintenance, updates, or experience technical issues that 
                    temporarily affect service availability.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    AI Limitations
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    Our AI models are trained on large datasets but may not be perfect. 
                    Results should be reviewed by qualified professionals and may not be 
                    suitable for all legal contexts or jurisdictions.
                  </p>
                </div>
              </div>
            </Card>
          </section>

          {/* Contact Information */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              7. Contact Information
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Legal Department
                  </h3>
                  <div className="space-y-3 text-muted-gray">
                    <p><strong className="text-light-gray">Email:</strong> legal@nyaymitra.com</p>
                    <p><strong className="text-light-gray">Phone:</strong> +91-22-1234-5678</p>
                    <p><strong className="text-light-gray">Address:</strong><br />
                    NyayMitra Technologies Pvt. Ltd.<br />
                    123 Legal Tech Park<br />
                    Mumbai, India 400001</p>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Support Team
                  </h3>
                  <div className="space-y-3 text-muted-gray">
                    <p><strong className="text-light-gray">Email:</strong> support@nyaymitra.com</p>
                    <p><strong className="text-light-gray">Chat:</strong> Available 24/7 in-app</p>
                    <p><strong className="text-light-gray">Response Time:</strong> Within 24 hours</p>
                    <p><strong className="text-light-gray">Emergency:</strong> Within 2 hours</p>
                  </div>
                </div>
              </div>
            </Card>
          </section>

          {/* Updates */}
          <section>
            <Card variant="glass" className="p-8 border-azure/50">
              <div className="flex items-start space-x-4">
                <Scale className="w-6 h-6 text-azure flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-legal font-semibold text-azure mb-3">
                    Changes to Terms
                  </h3>
                  <p className="text-light-gray leading-relaxed">
                    We may update these terms periodically. Material changes will be 
                    communicated via email or platform notifications at least 30 days 
                    before taking effect. Continued use of our services after changes 
                    constitutes acceptance of the updated terms.
                  </p>
                </div>
              </div>
            </Card>
          </section>
        </motion.div>
      </div>
    </div>
  );
};

export default TermsPage;
