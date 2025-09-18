import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Check, X, Sparkles, Scale, Shield, Globe, 
  Zap, Users, Lock, ArrowRight, Star, Info
} from 'lucide-react';
import NavigationBar from '../components/ui/NavigationBar';
import Footer from '../components/ui/Footer';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';

const PricingPage = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [showChat, setShowChat] = useState(false);

  const plans = [
    {
      name: 'Free',
      price: { monthly: 0, yearly: 0 },
      description: 'Perfect for individuals and small projects',
      features: [
        { text: '5 contracts per month', included: true },
        { text: 'Basic risk analysis', included: true },
        { text: 'Plain language summaries', included: true },
        { text: 'Email support', included: true },
        { text: 'Multi-language support', included: false },
        { text: 'Advanced simulations', included: false },
        { text: 'API access', included: false },
        { text: 'Priority processing', included: false },
        { text: 'Custom integrations', included: false },
        { text: 'Dedicated support', included: false }
      ],
      cta: 'Get Started',
      variant: 'outline',
      popular: false
    },
    {
      name: 'Professional',
      price: { monthly: 49, yearly: 470 },
      description: 'Ideal for growing businesses and legal teams',
      features: [
        { text: '100 contracts per month', included: true },
        { text: 'Advanced risk analysis', included: true },
        { text: 'Plain language summaries', included: true },
        { text: 'Priority email support', included: true },
        { text: '12+ language support', included: true },
        { text: 'Negotiation simulations', included: true },
        { text: 'API access (1000 calls/mo)', included: true },
        { text: 'Priority processing', included: true },
        { text: 'Custom integrations', included: false },
        { text: 'Dedicated support', included: false }
      ],
      cta: 'Start Free Trial',
      variant: 'gradient',
      popular: true
    },
    {
      name: 'Enterprise',
      price: { monthly: 'Custom', yearly: 'Custom' },
      description: 'Tailored solutions for large organizations',
      features: [
        { text: 'Unlimited contracts', included: true },
        { text: 'Enterprise risk analysis', included: true },
        { text: 'Custom AI models', included: true },
        { text: '24/7 dedicated support', included: true },
        { text: 'All languages supported', included: true },
        { text: 'Advanced simulations & analytics', included: true },
        { text: 'Unlimited API access', included: true },
        { text: 'Instant processing', included: true },
        { text: 'Custom integrations', included: true },
        { text: 'On-premise deployment', included: true }
      ],
      cta: 'Contact Sales',
      variant: 'primary',
      popular: false
    }
  ];

  const faqs = [
    {
      question: 'Can I change my plan later?',
      answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect at the next billing cycle.'
    },
    {
      question: 'Is there a free trial for Professional plan?',
      answer: 'Yes, we offer a 14-day free trial for the Professional plan with full access to all features.'
    },
    {
      question: 'How secure is my contract data?',
      answer: 'We use bank-level encryption and never store your contracts permanently. All data is processed in secure, isolated environments.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards, PayPal, and wire transfers for Enterprise plans.'
    },
    {
      question: 'Can I get a refund?',
      answer: 'We offer a 30-day money-back guarantee for all paid plans. No questions asked.'
    }
  ];

  return (
    <div className="min-h-screen bg-midnight">
      <NavigationBar onChatOpen={() => setShowChat(true)} />
      
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-0 left-1/3 w-96 h-96 bg-azure/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-1/3 w-96 h-96 bg-teal/10 rounded-full blur-3xl" />
        </div>
        
        <div className="relative max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 bg-charcoal/80 backdrop-blur-sm border border-border-dark rounded-full mb-6">
            <Star className="w-4 h-4 text-amber mr-2" />
            <span className="text-sm text-muted-gray font-medium">Trusted by 10,000+ legal professionals</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-heading font-bold text-light-gray mb-6">
            Choose Your Plan
          </h1>
          <p className="text-xl text-muted-gray max-w-3xl mx-auto mb-12">
            Transparent pricing that scales with your business. No hidden fees, no surprises.
          </p>
          
          {/* Billing Toggle */}
          <div className="inline-flex items-center p-1 bg-charcoal rounded-xl border border-border-dark">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                billingCycle === 'monthly' 
                  ? 'bg-azure text-white' 
                  : 'text-muted-gray hover:text-light-gray'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                billingCycle === 'yearly' 
                  ? 'bg-azure text-white' 
                  : 'text-muted-gray hover:text-light-gray'
              }`}
            >
              Yearly
              <span className="ml-2 text-xs bg-teal/20 text-teal px-2 py-1 rounded">Save 20%</span>
            </button>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <div key={index} className="relative">
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                    <div className="px-4 py-1 bg-gradient-premium rounded-full text-white text-sm font-medium">
                      Most Popular
                    </div>
                  </div>
                )}
                
                <Card 
                  variant={plan.popular ? 'premium' : 'glass'} 
                  className={`h-full p-8 ${plan.popular ? 'scale-105' : ''}`}
                  hover
                >
                  <div className="text-center mb-8">
                    <h3 className="text-2xl font-heading font-bold text-light-gray mb-2">
                      {plan.name}
                    </h3>
                    <p className="text-muted-gray text-sm mb-6">{plan.description}</p>
                    
                    <div className="mb-6">
                      {typeof plan.price[billingCycle] === 'number' ? (
                        <>
                          <span className="text-5xl font-heading font-bold text-light-gray">
                            ${plan.price[billingCycle]}
                          </span>
                          <span className="text-muted-gray ml-2">/{billingCycle === 'monthly' ? 'mo' : 'yr'}</span>
                        </>
                      ) : (
                        <span className="text-4xl font-heading font-bold gradient-text">
                          {plan.price[billingCycle]}
                        </span>
                      )}
                    </div>
                    
                    <Link to={plan.name === 'Enterprise' ? '/contact' : '/dashboard'}>
                      <Button 
                        variant={plan.variant} 
                        size="lg" 
                        className="w-full"
                        glow={plan.popular}
                      >
                        {plan.cta}
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </Link>
                  </div>
                  
                  <div className="space-y-4">
                    {plan.features.map((feature, idx) => (
                      <div key={idx} className="flex items-start space-x-3">
                        {feature.included ? (
                          <Check className="w-5 h-5 text-teal flex-shrink-0 mt-0.5" />
                        ) : (
                          <X className="w-5 h-5 text-muted-gray/50 flex-shrink-0 mt-0.5" />
                        )}
                        <span className={`text-sm ${
                          feature.included ? 'text-light-gray' : 'text-muted-gray/50'
                        }`}>
                          {feature.text}
                        </span>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-charcoal/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-light-gray mb-4">
              Detailed Feature Comparison
            </h2>
            <p className="text-muted-gray">Everything you need to know about each plan</p>
          </div>
          
          <Card variant="glass" className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border-dark">
                    <th className="text-left p-6 text-light-gray font-heading">Features</th>
                    <th className="text-center p-6 text-light-gray font-heading">Free</th>
                    <th className="text-center p-6 text-light-gray font-heading">
                      <div className="flex items-center justify-center space-x-2">
                        <span>Professional</span>
                        <Sparkles className="w-4 h-4 text-azure" />
                      </div>
                    </th>
                    <th className="text-center p-6 text-light-gray font-heading">Enterprise</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-dark">
                  {[
                    { feature: 'Contracts per month', free: '5', pro: '100', enterprise: 'Unlimited' },
                    { feature: 'Risk analysis depth', free: 'Basic', pro: 'Advanced', enterprise: 'Enterprise' },
                    { feature: 'Languages supported', free: '1', pro: '12+', enterprise: 'All' },
                    { feature: 'API calls per month', free: '0', pro: '1,000', enterprise: 'Unlimited' },
                    { feature: 'Processing speed', free: 'Standard', pro: 'Priority', enterprise: 'Instant' },
                    { feature: 'Support response time', free: '48 hrs', pro: '12 hrs', enterprise: '< 1 hr' },
                    { feature: 'Data retention', free: '7 days', pro: '30 days', enterprise: 'Custom' },
                    { feature: 'Team members', free: '1', pro: '10', enterprise: 'Unlimited' }
                  ].map((row, idx) => (
                    <tr key={idx}>
                      <td className="p-6 text-muted-gray">{row.feature}</td>
                      <td className="p-6 text-center text-light-gray">{row.free}</td>
                      <td className="p-6 text-center text-light-gray bg-azure/5">{row.pro}</td>
                      <td className="p-6 text-center text-light-gray">{row.enterprise}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </section>

      {/* FAQs */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-light-gray mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-muted-gray">Got questions? We've got answers</p>
          </div>
          
          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <Card key={index} variant="glass" className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="p-2 bg-azure/20 rounded-lg">
                    <Info className="w-5 h-5 text-azure" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-heading font-semibold text-light-gray mb-2">
                      {faq.question}
                    </h3>
                    <p className="text-muted-gray leading-relaxed">
                      {faq.answer}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-premium opacity-10" />
        <div className="relative max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-heading font-bold text-light-gray mb-6">
            Ready to Transform Your Contract Review?
          </h2>
          <p className="text-xl text-muted-gray mb-8">
            Start your free trial today. No credit card required.
          </p>
          <Link to="/dashboard">
            <Button variant="gradient" size="xl" glow>
              Start Free Trial
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </Link>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default PricingPage;
