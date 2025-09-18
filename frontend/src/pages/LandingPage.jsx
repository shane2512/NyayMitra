import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Scale, Shield, FileText, Zap, BarChart3, MessageSquare, 
  CheckCircle, ArrowRight, Upload, Users, Star, Brain, 
  TrendingUp, Lock, Globe, Sparkles, ChevronRight,
  FileSearch, AlertTriangle, Target
} from 'lucide-react';
import NavigationBar from '../components/ui/NavigationBar';
import Footer from '../components/ui/Footer';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';

const LandingPage = () => {
  const features = [
    {
      icon: <FileSearch className="w-6 h-6" />,
      title: "Contract Analysis",
      description: "AI-powered deep analysis of legal documents with clause-by-clause breakdown"
    },
    {
      icon: <AlertTriangle className="w-6 h-6" />,
      title: "Risk Assessment",
      description: "Identify and categorize risks with color-coded severity levels"
    },
    {
      icon: <Brain className="w-6 h-6" />,
      title: "Plain Language",
      description: "Complex legal terms explained in simple, understandable language"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Negotiation Simulation",
      description: "Predict outcomes and optimize negotiation strategies"
    },
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: "AI Legal Assistant",
      description: "24/7 conversational AI for instant legal guidance"
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: "Multi-Language",
      description: "Support for 12+ languages with culturally appropriate translations"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Legal Director, TechCorp",
      content: "NyayMitra has revolutionized our contract review process. What used to take days now takes hours.",
      rating: 5,
      avatar: "SC"
    },
    {
      name: "Michael Rodriguez",
      role: "CEO, StartupHub",
      content: "The AI assistant is like having a legal team on demand. Incredible value for growing businesses.",
      rating: 5,
      avatar: "MR"
    },
    {
      name: "Priya Sharma",
      role: "Compliance Manager",
      content: "The risk visualization features help us make informed decisions quickly. Game-changing platform.",
      rating: 5,
      avatar: "PS"
    }
  ];

  const stats = [
    { value: "10K+", label: "Contracts Analyzed" },
    { value: "95%", label: "Accuracy Rate" },
    { value: "72hrs", label: "Saved Per Contract" },
    { value: "4.9★", label: "User Rating" }
  ];

  return (
    <div className="min-h-screen bg-midnight">
      <NavigationBar />
      
      {/* Hero Section */}
      <section className="relative pt-20 pb-32 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-azure/20 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-teal/20 rounded-full blur-3xl animate-pulse animation-delay-400" />
        </div>
        
        <div className="relative max-w-7xl mx-auto">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center px-4 py-2 bg-charcoal/80 backdrop-blur-sm border border-border-dark rounded-full mb-8 animate-fade-in">
              <Sparkles className="w-4 h-4 text-azure mr-2" />
              <span className="text-sm text-muted-gray font-medium">AI-Powered Legal Intelligence</span>
            </div>
            
            {/* Headline */}
            <h1 className="text-5xl md:text-7xl font-heading font-bold mb-8 leading-tight animate-fade-in animation-delay-200">
              <span className="block text-light-gray">Decode Contracts</span>
              <span className="block gradient-text text-6xl md:text-8xl">In Seconds</span>
            </h1>
            
            {/* Subheadline */}
            <p className="text-xl text-muted-gray max-w-3xl mx-auto mb-12 leading-relaxed animate-fade-in animation-delay-400">
              Transform complex legal documents into clear insights with AI-powered contract analysis. 
              Identify risks, understand terms, and negotiate with confidence.
            </p>
            
            {/* CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-20 animate-fade-in animation-delay-600">
              <Link to="/dashboard">
                <Button variant="primary" size="lg" glow>
                  <Upload className="w-5 h-5 mr-2" />
                  Upload a Contract
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </div>
            
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto animate-fade-in animation-delay-600">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-heading font-bold gradient-text mb-2">
                    {stat.value}
                  </div>
                  <div className="text-muted-gray text-sm font-medium">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-charcoal/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-bold mb-6 text-light-gray">
              Powerful Features for
              <span className="gradient-text"> Legal Excellence</span>
            </h2>
            <p className="text-xl text-muted-gray max-w-2xl mx-auto">
              Everything you need to understand and negotiate contracts effectively
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} variant="glass" hover className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-gradient-to-br from-azure/20 to-teal/20 rounded-xl">
                    <div className="text-azure">
                      {feature.icon}
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-heading font-semibold mb-2 text-light-gray">
                      {feature.title}
                    </h3>
                    <p className="text-muted-gray leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-bold mb-6 text-light-gray">
              How It Works
            </h2>
            <p className="text-xl text-muted-gray">Three simple steps to contract clarity</p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            {[
              { icon: Upload, title: "Upload Contract", desc: "Drag and drop your PDF contract or paste text directly" },
              { icon: Brain, title: "AI Analysis", desc: "Our AI instantly analyzes clauses, identifies risks, and simplifies language" },
              { icon: TrendingUp, title: "Get Insights", desc: "Receive comprehensive reports with actionable recommendations" }
            ].map((step, index) => (
              <div key={index} className="text-center group">
                <div className="relative mb-8">
                  <div className="w-20 h-20 bg-gradient-premium rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform shadow-lg">
                    <step.icon className="w-8 h-8 text-white" />
                  </div>
                  {index < 2 && (
                    <ChevronRight className="hidden md:block absolute top-1/2 -right-6 transform -translate-y-1/2 text-muted-gray w-8 h-8" />
                  )}
                </div>
                <h3 className="text-xl font-heading font-semibold mb-3 text-light-gray">{step.title}</h3>
                <p className="text-muted-gray leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20 px-4 sm:px-6 lg:px-8 bg-charcoal/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-bold mb-6 text-light-gray">
              Trusted by Legal Professionals
            </h2>
            <p className="text-xl text-muted-gray">See what our users are saying</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} variant="glass" className="p-6">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-gradient-premium rounded-full flex items-center justify-center text-white font-bold mr-4">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="font-heading font-semibold text-light-gray">{testimonial.name}</div>
                    <div className="text-sm text-muted-gray">{testimonial.role}</div>
                  </div>
                </div>
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-amber fill-current" />
                  ))}
                </div>
                <p className="text-muted-gray leading-relaxed italic">"{testimonial.content}"</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-premium opacity-10" />
        <div className="relative max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-heading font-bold mb-6 text-light-gray">
            Ready to Transform Your
            <span className="gradient-text"> Contract Review Process?</span>
          </h2>
          <p className="text-xl text-muted-gray mb-8 leading-relaxed">
            Join thousands of professionals who trust NyayMitra for contract analysis
          </p>
          <Link to="/dashboard">
            <Button variant="gradient" size="xl" glow>
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </Link>
          <p className="text-sm text-muted-gray mt-4">No credit card required • Free forever for basic use</p>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;
