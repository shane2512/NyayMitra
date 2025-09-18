import React from 'react';
import { Shield, Lock, Key, Server, Cloud, AlertCircle, CheckCircle, Zap } from 'lucide-react';
import NavigationBar from '../components/ui/NavigationBar';
import Footer from '../components/ui/Footer';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

const SecurityPage = () => {
  const securityFeatures = [
    {
      icon: <Lock className="w-6 h-6" />,
      title: "End-to-End Encryption",
      description: "AES-256 encryption for all data in transit and at rest"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "SOC 2 Type II Certified",
      description: "Annual third-party security audits and compliance verification"
    },
    {
      icon: <Key className="w-6 h-6" />,
      title: "Multi-Factor Authentication",
      description: "Additional security layer for account access"
    },
    {
      icon: <Server className="w-6 h-6" />,
      title: "Secure Infrastructure",
      description: "Hosted on AWS with enterprise-grade security controls"
    },
    {
      icon: <Cloud className="w-6 h-6" />,
      title: "Regular Backups",
      description: "Automated encrypted backups with point-in-time recovery"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "DDoS Protection",
      description: "Advanced threat detection and mitigation systems"
    }
  ];

  const complianceStandards = [
    { name: "GDPR", description: "General Data Protection Regulation compliant" },
    { name: "CCPA", description: "California Consumer Privacy Act compliant" },
    { name: "HIPAA", description: "Health Insurance Portability and Accountability Act ready" },
    { name: "ISO 27001", description: "Information security management certified" },
    { name: "PCI DSS", description: "Payment Card Industry Data Security Standard" },
    { name: "NIST", description: "National Institute of Standards and Technology framework" }
  ];

  const securityPractices = [
    "Regular penetration testing by independent security firms",
    "24/7 security monitoring and incident response team",
    "Employee security training and background checks",
    "Strict access controls and principle of least privilege",
    "Secure software development lifecycle (SSDLC)",
    "Regular security updates and patch management"
  ];

  return (
    <div className="min-h-screen bg-midnight">
      <NavigationBar />
      
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-0 right-1/3 w-96 h-96 bg-teal/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-1/3 w-96 h-96 bg-azure/10 rounded-full blur-3xl" />
        </div>
        
        <div className="relative max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-premium rounded-2xl mb-6">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-heading font-bold text-light-gray mb-6">
              Security & Compliance
            </h1>
            <p className="text-xl text-muted-gray max-w-3xl mx-auto">
              Enterprise-grade security to protect your most sensitive legal documents
            </p>
          </div>
        </div>
      </section>

      {/* Security Features */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-heading font-bold text-light-gray mb-4">
              Security Features
            </h2>
            <p className="text-muted-gray">
              Multiple layers of protection for your data
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {securityFeatures.map((feature, index) => (
              <Card key={index} variant="glass" hover className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-teal/20 rounded-xl">
                    <div className="text-teal">
                      {feature.icon}
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-heading font-semibold text-light-gray mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-muted-gray text-sm leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Compliance Standards */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-charcoal/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-heading font-bold text-light-gray mb-4">
              Compliance Standards
            </h2>
            <p className="text-muted-gray">
              Meeting and exceeding industry standards
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {complianceStandards.map((standard, index) => (
              <Card key={index} variant="glass" className="p-6">
                <div className="flex items-center space-x-3 mb-3">
                  <CheckCircle className="w-5 h-5 text-teal" />
                  <h3 className="text-xl font-heading font-bold gradient-text">
                    {standard.name}
                  </h3>
                </div>
                <p className="text-muted-gray text-sm">
                  {standard.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Security Practices */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <Card variant="premium" className="p-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-heading font-bold text-light-gray mb-4">
                Our Security Practices
              </h2>
              <p className="text-muted-gray">
                Continuous improvement and vigilance
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {securityPractices.map((practice, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <CheckCircle className="w-5 h-5 text-teal flex-shrink-0 mt-0.5" />
                  <span className="text-light-gray">{practice}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </section>

      {/* Security Report */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <Card variant="glass" className="p-8 text-center">
            <AlertCircle className="w-12 h-12 text-azure mx-auto mb-6" />
            <h2 className="text-2xl font-heading font-bold text-light-gray mb-4">
              Request Our Security Report
            </h2>
            <p className="text-muted-gray mb-8 max-w-2xl mx-auto">
              Get detailed information about our security measures, compliance certifications, 
              and technical safeguards. Available for enterprise customers.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="primary" size="lg">
                Request Security Report
              </Button>
              <Button variant="outline" size="lg">
                Contact Security Team
              </Button>
            </div>
          </Card>
        </div>
      </section>

      {/* Trust Center */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-charcoal/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-heading font-bold text-light-gray mb-6">
            Your Trust is Our Priority
          </h2>
          <p className="text-xl text-muted-gray mb-8 leading-relaxed">
            We understand that you're trusting us with sensitive legal documents. 
            That's why security isn't just a feature – it's the foundation of everything we build.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center text-muted-gray">
            <div className="flex items-center justify-center space-x-2">
              <Shield className="w-5 h-5 text-teal" />
              <span>99.99% Uptime SLA</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <Lock className="w-5 h-5 text-azure" />
              <span>Zero Data Breaches</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <Zap className="w-5 h-5 text-amber" />
              <span>24/7 Monitoring</span>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default SecurityPage;
