import React from 'react';
import { motion } from 'framer-motion';
import { 
  Scale, FileText, Brain, BarChart3, Shield, Zap, 
  CheckCircle, Star, ArrowRight, Users, Globe, 
  TrendingUp, Award, MessageSquare
} from 'lucide-react';
import Button from '../ui/Button';
import Card from '../ui/Card';

const LandingPage = ({ onGetStarted }) => {
  const features = [
    {
      icon: <Brain className="w-8 h-8 text-azure" />,
      title: "AI-Powered Analysis",
      description: "Advanced AI analyzes contracts in seconds, identifying risks and opportunities with precision."
    },
    {
      icon: <Shield className="w-8 h-8 text-teal" />,
      title: "Risk Assessment",
      description: "Comprehensive risk scoring with detailed explanations in plain language."
    },
    {
      icon: <Globe className="w-8 h-8 text-amber" />,
      title: "Multi-Language Support",
      description: "Analyze contracts in 12+ languages with culturally appropriate insights."
    },
    {
      icon: <BarChart3 className="w-8 h-8 text-azure" />,
      title: "Visual Analytics",
      description: "Interactive charts and graphs make complex legal data easy to understand."
    },
    {
      icon: <MessageSquare className="w-8 h-8 text-teal" />,
      title: "AI Legal Assistant",
      description: "Chat with our AI for instant answers about your contracts and legal questions."
    },
    {
      icon: <Zap className="w-8 h-8 text-amber" />,
      title: "Instant Results",
      description: "Get comprehensive analysis reports in under 30 seconds, not hours."
    }
  ];

  const steps = [
    {
      step: "01",
      title: "Upload Contract",
      description: "Simply drag and drop your PDF contract or select from your device.",
      icon: <FileText className="w-6 h-6 text-azure" />
    },
    {
      step: "02", 
      title: "AI Analysis",
      description: "Our advanced AI analyzes every clause, identifying risks and opportunities.",
      icon: <Brain className="w-6 h-6 text-teal" />
    },
    {
      step: "03",
      title: "Get Insights",
      description: "Receive detailed reports, risk scores, and actionable recommendations.",
      icon: <BarChart3 className="w-6 h-6 text-amber" />
    }
  ];

  const testimonials = [
    {
      name: "Priya Sharma",
      role: "Legal Counsel, TechCorp India",
      content: "NyayMitra has revolutionized how we review contracts. What used to take hours now takes minutes, with better accuracy.",
      rating: 5,
      avatar: "PS"
    },
    {
      name: "Rajesh Kumar",
      role: "Startup Founder",
      content: "As a non-lawyer, NyayMitra helps me understand complex contracts and negotiate better terms. Invaluable for any business.",
      rating: 5,
      avatar: "RK"
    },
    {
      name: "Anita Desai",
      role: "Corporate Lawyer",
      content: "The AI insights are remarkably accurate. It catches risks I might miss and explains them in plain language for clients.",
      rating: 5,
      avatar: "AD"
    }
  ];

  const stats = [
    { label: "Contracts Analyzed", value: "50,000+", icon: <FileText className="w-5 h-5" /> },
    { label: "Risk Issues Identified", value: "200,000+", icon: <Shield className="w-5 h-5" /> },
    { label: "Languages Supported", value: "12+", icon: <Globe className="w-5 h-5" /> },
    { label: "User Satisfaction", value: "98%", icon: <Star className="w-5 h-5" /> }
  ];

  return (
    <div className="min-h-screen bg-midnight">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-azure/10 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-teal/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="inline-flex items-center px-4 py-2 bg-charcoal/50 rounded-full border border-border-dark mb-8">
                <Scale className="w-4 h-4 text-azure mr-2" />
                <span className="text-sm text-light-gray">AI-Powered Legal Technology</span>
              </div>
              
              <h1 className="text-5xl lg:text-7xl font-heading font-bold text-light-gray mb-6 tracking-tight">
                Analyze Legal Contracts with{' '}
                <span className="gradient-text">AI Precision</span>
              </h1>
              
              <p className="text-xl lg:text-2xl text-muted-gray max-w-4xl mx-auto mb-12 leading-relaxed">
                Transform complex legal documents into clear insights. Get instant risk assessments, 
                plain-language summaries, and AI-powered guidance for better contract decisions.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Button
                  variant="gradient"
                  size="lg"
                  onClick={onGetStarted}
                  className="btn-glow"
                >
                  <Zap className="w-5 h-5 mr-2" />
                  Start Free Analysis
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  className="text-light-gray border-border-dark hover:bg-charcoal"
                >
                  <BarChart3 className="w-5 h-5 mr-2" />
                  View Demo
                </Button>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-charcoal/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="flex items-center justify-center w-12 h-12 bg-gradient-premium rounded-xl mx-auto mb-4">
                  {stat.icon}
                </div>
                <div className="text-3xl font-heading font-bold text-light-gray mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-gray">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-4xl lg:text-5xl font-heading font-bold text-light-gray mb-6">
                Powerful Features for Legal Professionals
              </h2>
              <p className="text-xl text-muted-gray max-w-3xl mx-auto">
                Everything you need to analyze, understand, and negotiate contracts with confidence
              </p>
            </motion.div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card variant="glass" hover className="p-8 h-full">
                  <div className="flex items-center mb-6">
                    <div className="p-3 bg-charcoal rounded-xl mr-4">
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-heading font-semibold text-light-gray">
                      {feature.title}
                    </h3>
                  </div>
                  <p className="text-muted-gray leading-relaxed">
                    {feature.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-charcoal/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-heading font-bold text-light-gray mb-6">
              How It Works
            </h2>
            <p className="text-xl text-muted-gray max-w-3xl mx-auto">
              Get professional contract analysis in three simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={step.step}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                className="relative"
              >
                <Card variant="glass" className="p-8 text-center">
                  <div className="text-6xl font-heading font-bold text-azure/20 mb-4">
                    {step.step}
                  </div>
                  <div className="w-16 h-16 bg-gradient-premium rounded-full flex items-center justify-center mx-auto mb-6">
                    {step.icon}
                  </div>
                  <h3 className="text-2xl font-heading font-semibold text-light-gray mb-4">
                    {step.title}
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    {step.description}
                  </p>
                </Card>
                
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <ArrowRight className="w-8 h-8 text-azure/50" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-heading font-bold text-light-gray mb-6">
              Trusted by Legal Professionals
            </h2>
            <p className="text-xl text-muted-gray max-w-3xl mx-auto">
              See what our users say about NyayMitra
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card variant="glass" className="p-8 h-full">
                  <div className="flex items-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 text-amber fill-current" />
                    ))}
                  </div>
                  <p className="text-light-gray mb-6 leading-relaxed italic">
                    "{testimonial.content}"
                  </p>
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-gradient-premium rounded-full flex items-center justify-center text-white font-semibold mr-4">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <div className="font-semibold text-light-gray">
                        {testimonial.name}
                      </div>
                      <div className="text-sm text-muted-gray">
                        {testimonial.role}
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-premium">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl lg:text-5xl font-heading font-bold text-white mb-6">
              Ready to Transform Your Contract Analysis?
            </h2>
            <p className="text-xl text-white/90 mb-8 leading-relaxed">
              Join thousands of legal professionals who trust NyayMitra for accurate, 
              fast, and reliable contract analysis.
            </p>
            <Button
              variant="secondary"
              size="lg"
              onClick={onGetStarted}
              className="bg-white text-azure hover:bg-gray-100"
            >
              <Zap className="w-5 h-5 mr-2" />
              Start Your Free Analysis
            </Button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
