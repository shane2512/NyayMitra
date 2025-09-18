import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Lock, Eye, Database, Users, Globe, AlertTriangle, CheckCircle } from 'lucide-react';
import Card from '../ui/Card';

const PrivacyPage = () => {
  const principles = [
    {
      icon: <Shield className="w-6 h-6 text-teal" />,
      title: "Data Protection",
      description: "We use enterprise-grade encryption and security measures to protect your sensitive legal documents."
    },
    {
      icon: <Lock className="w-6 h-6 text-azure" />,
      title: "Secure Processing",
      description: "All contract analysis happens in secure, isolated environments with no permanent storage of your documents."
    },
    {
      icon: <Eye className="w-6 h-6 text-amber" />,
      title: "Transparency",
      description: "We're completely transparent about what data we collect, how we use it, and who has access to it."
    },
    {
      icon: <Users className="w-6 h-6 text-teal" />,
      title: "User Control",
      description: "You maintain full control over your data with options to export, delete, or modify your information anytime."
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
            <Shield className="w-4 h-4 text-teal mr-2" />
            <span className="text-sm text-light-gray">Privacy Policy</span>
          </div>
          
          <h1 className="text-5xl font-legal font-bold text-light-gray mb-6">
            Your Privacy Matters
          </h1>
          
          <p className="text-xl text-muted-gray max-w-3xl mx-auto leading-relaxed">
            At NyayMitra, we're committed to protecting your privacy and ensuring the security 
            of your legal documents. This policy explains how we handle your data.
          </p>
          
          <div className="mt-6 text-sm text-muted-gray">
            Last updated: January 15, 2024
          </div>
        </motion.div>

        {/* Privacy Principles */}
        <section className="mb-16">
          <h2 className="text-3xl font-legal font-bold text-light-gray text-center mb-12">
            Our Privacy Principles
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {principles.map((principle, index) => (
              <motion.div
                key={principle.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card variant="glass" className="p-6 h-full">
                  <div className="flex items-center mb-4">
                    <div className="p-3 bg-charcoal rounded-xl mr-4">
                      {principle.icon}
                    </div>
                    <h3 className="text-xl font-legal font-semibold text-light-gray">
                      {principle.title}
                    </h3>
                  </div>
                  <p className="text-muted-gray leading-relaxed">
                    {principle.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Detailed Policy */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-12"
        >
          {/* Information We Collect */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              Information We Collect
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Documents You Upload
                  </h3>
                  <p className="text-muted-gray leading-relaxed mb-4">
                    When you upload contracts for analysis, we temporarily process these documents 
                    to provide our AI-powered insights. We do not permanently store your documents 
                    on our servers.
                  </p>
                  <div className="bg-teal/10 border border-teal/20 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm text-light-gray">
                          <strong>Important:</strong> Your contracts are processed in secure, isolated 
                          environments and are automatically deleted after analysis completion.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Account Information
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li>• Email address and name for account creation</li>
                    <li>• Billing information for paid subscriptions</li>
                    <li>• Usage analytics to improve our services</li>
                    <li>• Communication preferences and support interactions</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-3">
                    Technical Information
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li>• IP address and browser information</li>
                    <li>• Device type and operating system</li>
                    <li>• Usage patterns and feature interactions</li>
                    <li>• Error logs and performance metrics</li>
                  </ul>
                </div>
              </div>
            </Card>
          </section>

          {/* How We Use Information */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              How We Use Your Information
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Service Delivery
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li>• Analyze your contracts using AI</li>
                    <li>• Provide risk assessments and insights</li>
                    <li>• Generate plain-language summaries</li>
                    <li>• Enable AI chat functionality</li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Service Improvement
                  </h3>
                  <ul className="text-muted-gray space-y-2">
                    <li>• Improve AI model accuracy</li>
                    <li>• Enhance user experience</li>
                    <li>• Develop new features</li>
                    <li>• Provide customer support</li>
                  </ul>
                </div>
              </div>
            </Card>
          </section>

          {/* Data Security */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              Data Security & Protection
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-teal/20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Lock className="w-8 h-8 text-teal" />
                    </div>
                    <h4 className="font-legal font-semibold text-light-gray mb-2">
                      Encryption
                    </h4>
                    <p className="text-sm text-muted-gray">
                      End-to-end encryption for all data transmission and storage
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <div className="w-16 h-16 bg-azure/20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Database className="w-8 h-8 text-azure" />
                    </div>
                    <h4 className="font-legal font-semibold text-light-gray mb-2">
                      Secure Infrastructure
                    </h4>
                    <p className="text-sm text-muted-gray">
                      Enterprise-grade cloud infrastructure with regular security audits
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <div className="w-16 h-16 bg-amber/20 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Shield className="w-8 h-8 text-amber" />
                    </div>
                    <h4 className="font-legal font-semibold text-light-gray mb-2">
                      Access Control
                    </h4>
                    <p className="text-sm text-muted-gray">
                      Strict access controls and authentication protocols
                    </p>
                  </div>
                </div>
                
                <div className="bg-azure/10 border border-azure/20 rounded-lg p-6 mt-8">
                  <h4 className="font-legal font-semibold text-azure mb-3">
                    Industry Standards Compliance
                  </h4>
                  <p className="text-light-gray text-sm leading-relaxed">
                    We comply with international data protection standards including GDPR, 
                    SOC 2 Type II, and ISO 27001. Our security practices are regularly 
                    audited by third-party security firms.
                  </p>
                </div>
              </div>
            </Card>
          </section>

          {/* Your Rights */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              Your Rights & Controls
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Data Access & Control
                  </h3>
                  <ul className="text-muted-gray space-y-3">
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Access and download your personal data</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Correct inaccurate information</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Delete your account and data</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Opt-out of marketing communications</span>
                    </li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Data Portability
                  </h3>
                  <ul className="text-muted-gray space-y-3">
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Export your analysis history</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Transfer data to other services</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Receive data in standard formats</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span>Request data processing restrictions</span>
                    </li>
                  </ul>
                </div>
              </div>
            </Card>
          </section>

          {/* Contact Information */}
          <section>
            <h2 className="text-3xl font-legal font-bold text-light-gray mb-6">
              Contact Us About Privacy
            </h2>
            
            <Card variant="glass" className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Privacy Officer
                  </h3>
                  <div className="space-y-3 text-muted-gray">
                    <p><strong className="text-light-gray">Email:</strong> privacy@nyaymitra.com</p>
                    <p><strong className="text-light-gray">Phone:</strong> +91-22-1234-5678</p>
                    <p><strong className="text-light-gray">Address:</strong><br />
                    NyayMitra Technologies Pvt. Ltd.<br />
                    123 Legal Tech Park<br />
                    Mumbai, India 400001</p>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-xl font-legal font-semibold text-light-gray mb-4">
                    Response Times
                  </h3>
                  <div className="space-y-3 text-muted-gray">
                    <p>• <strong className="text-light-gray">Data requests:</strong> Within 30 days</p>
                    <p>• <strong className="text-light-gray">Privacy inquiries:</strong> Within 5 business days</p>
                    <p>• <strong className="text-light-gray">Security concerns:</strong> Within 24 hours</p>
                    <p>• <strong className="text-light-gray">Account deletion:</strong> Within 7 days</p>
                  </div>
                </div>
              </div>
            </Card>
          </section>

          {/* Updates */}
          <section>
            <Card variant="glass" className="p-8 border-amber/50">
              <div className="flex items-start space-x-4">
                <AlertTriangle className="w-6 h-6 text-amber flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-legal font-semibold text-amber mb-3">
                    Policy Updates
                  </h3>
                  <p className="text-light-gray leading-relaxed">
                    We may update this privacy policy periodically to reflect changes in our 
                    practices or legal requirements. We'll notify you of significant changes 
                    via email or through our platform at least 30 days before they take effect.
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

export default PrivacyPage;
