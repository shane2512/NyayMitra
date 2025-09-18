import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Check, X, Zap, Crown, Building, Users, 
  FileText, MessageSquare, Globe, Shield,
  BarChart3, Headphones, Star
} from 'lucide-react';
import Button from '../ui/Button';
import Card from '../ui/Card';

const PricingPage = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');

  const plans = [
    {
      name: "Starter",
      description: "Perfect for individuals and small businesses",
      icon: <Zap className="w-6 h-6" />,
      price: {
        monthly: 999,
        yearly: 9990
      },
      originalPrice: {
        monthly: 1499,
        yearly: 14990
      },
      features: [
        "5 contract analyses per month",
        "Basic risk assessment",
        "Plain language summaries",
        "PDF export",
        "Email support",
        "Multi-language support (5 languages)"
      ],
      limitations: [
        "No API access",
        "No team collaboration",
        "No advanced analytics"
      ],
      popular: false,
      cta: "Start Free Trial"
    },
    {
      name: "Professional",
      description: "Ideal for legal professionals and growing teams",
      icon: <Crown className="w-6 h-6" />,
      price: {
        monthly: 2999,
        yearly: 29990
      },
      originalPrice: {
        monthly: 4499,
        yearly: 44990
      },
      features: [
        "50 contract analyses per month",
        "Advanced risk assessment",
        "AI legal assistant chat",
        "Negotiation simulation",
        "Team collaboration (up to 5 users)",
        "Priority email support",
        "All 12 languages supported",
        "Custom risk categories",
        "Advanced analytics dashboard",
        "API access (100 calls/month)"
      ],
      limitations: [
        "Limited API calls",
        "No white-label options"
      ],
      popular: true,
      cta: "Start Free Trial"
    },
    {
      name: "Enterprise",
      description: "For large organizations with custom needs",
      icon: <Building className="w-6 h-6" />,
      price: {
        monthly: "Custom",
        yearly: "Custom"
      },
      features: [
        "Unlimited contract analyses",
        "Full AI legal assistant suite",
        "Advanced negotiation tools",
        "Unlimited team members",
        "24/7 phone & chat support",
        "All languages + custom translations",
        "Custom integrations",
        "White-label options",
        "Advanced security & compliance",
        "Unlimited API access",
        "Custom AI model training",
        "Dedicated account manager"
      ],
      limitations: [],
      popular: false,
      cta: "Contact Sales"
    }
  ];

  const faqs = [
    {
      question: "How accurate is the AI analysis?",
      answer: "Our AI has been trained on millions of legal documents and achieves 95%+ accuracy in risk identification. However, we always recommend having important contracts reviewed by qualified legal professionals."
    },
    {
      question: "What file formats do you support?",
      answer: "We currently support PDF files up to 50MB in size. We're working on adding support for Word documents and other formats."
    },
    {
      question: "Is my data secure?",
      answer: "Yes, we use enterprise-grade encryption and follow strict data protection protocols. Your contracts are processed securely and never stored permanently on our servers."
    },
    {
      question: "Can I cancel anytime?",
      answer: "Absolutely! You can cancel your subscription at any time. There are no long-term contracts or cancellation fees."
    },
    {
      question: "Do you offer refunds?",
      answer: "We offer a 30-day money-back guarantee for all paid plans. If you're not satisfied, we'll provide a full refund."
    },
    {
      question: "What languages are supported?",
      answer: "We support 12 major languages including English, Hindi, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Portuguese, Russian, and Italian."
    }
  ];

  const formatPrice = (price) => {
    if (typeof price === 'string') return price;
    return `₹${price.toLocaleString()}`;
  };

  const getMonthlyPrice = (plan) => {
    if (typeof plan.price.monthly === 'string') return plan.price.monthly;
    return billingCycle === 'yearly' 
      ? Math.round(plan.price.yearly / 12)
      : plan.price.monthly;
  };

  return (
    <div className="min-h-screen bg-midnight py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl lg:text-6xl font-heading font-bold text-light-gray mb-6">
              Simple, Transparent Pricing
            </h1>
            <p className="text-xl text-muted-gray max-w-3xl mx-auto mb-8">
              Choose the perfect plan for your legal analysis needs. All plans include our core AI features.
            </p>

            {/* Billing Toggle */}
            <div className="inline-flex items-center bg-charcoal rounded-xl p-1 border border-border-dark">
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
                <span className="ml-2 px-2 py-1 bg-teal text-xs rounded-full text-white">
                  Save 33%
                </span>
              </button>
            </div>
          </motion.div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-20">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-14 left-0 w-full flex justify-center">
                  <div className="bg-gradient-premium text-white px-8 py-4 rounded-full text-sm font-semibold flex items-center shadow-lg">
                    <Star className="w-4 h-4 mr-1" />
                    Most Popular
                  </div>
                </div>
              )}
              
              <Card 
                variant="glass" 
                className={`p-8 h-full ${plan.popular ? 'border-azure/50 shadow-xl shadow-azure/10' : ''}`}
              >
                <div className="text-center mb-8">
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-xl mb-4 ${
                    plan.popular ? 'bg-gradient-premium' : 'bg-charcoal'
                  }`}>
                    {plan.icon}
                  </div>
                  
                  <h3 className="text-2xl font-heading font-bold text-light-gray mb-2">
                    {plan.name}
                  </h3>
                  <p className="text-muted-gray mb-6">
                    {plan.description}
                  </p>
                  
                  <div className="mb-6">
                    <div className="flex items-baseline justify-center">
                      <span className="text-4xl font-heading font-bold text-light-gray">
                        {formatPrice(getMonthlyPrice(plan))}
                      </span>
                      {typeof plan.price.monthly !== 'string' && (
                        <span className="text-muted-gray ml-2">/month</span>
                      )}
                    </div>
                    
                    {billingCycle === 'yearly' && typeof plan.price.yearly !== 'string' && (
                      <div className="text-sm text-muted-gray mt-2">
                        Billed annually: {formatPrice(plan.price.yearly)}
                      </div>
                    )}
                    
                    {plan.originalPrice && typeof plan.originalPrice.monthly !== 'string' && (
                      <div className="text-sm text-muted-gray line-through mt-1">
                        Regular: {formatPrice(billingCycle === 'yearly' ? Math.round(plan.originalPrice.yearly / 12) : plan.originalPrice.monthly)}/month
                      </div>
                    )}
                  </div>
                </div>

                <div className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <div key={featureIndex} className="flex items-start">
                      <Check className="w-5 h-5 text-teal flex-shrink-0 mt-0.5 mr-3" />
                      <span className="text-light-gray">{feature}</span>
                    </div>
                  ))}
                  
                  {plan.limitations.map((limitation, limitIndex) => (
                    <div key={limitIndex} className="flex items-start opacity-60">
                      <X className="w-5 h-5 text-muted-gray flex-shrink-0 mt-0.5 mr-3" />
                      <span className="text-muted-gray">{limitation}</span>
                    </div>
                  ))}
                </div>

                <Button
                  variant={plan.popular ? "gradient" : "outline"}
                  size="lg"
                  className="w-full"
                >
                  {plan.cta}
                </Button>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Feature Comparison */}
        <div className="mb-20">
          <h2 className="text-3xl font-heading font-bold text-light-gray text-center mb-12">
            Feature Comparison
          </h2>
          
          <Card variant="glass" className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border-dark">
                    <th className="text-left py-4 px-6 text-light-gray font-semibold">Features</th>
                    <th className="text-center py-4 px-6 text-light-gray font-semibold">Starter</th>
                    <th className="text-center py-4 px-6 text-light-gray font-semibold">Professional</th>
                    <th className="text-center py-4 px-6 text-light-gray font-semibold">Enterprise</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { feature: "Contract Analyses", starter: "5/month", pro: "50/month", enterprise: "Unlimited" },
                    { feature: "AI Legal Assistant", starter: false, pro: true, enterprise: true },
                    { feature: "Team Collaboration", starter: false, pro: "5 users", enterprise: "Unlimited" },
                    { feature: "API Access", starter: false, pro: "100 calls/month", enterprise: "Unlimited" },
                    { feature: "Languages Supported", starter: "5", pro: "12", enterprise: "12 + Custom" },
                    { feature: "Priority Support", starter: false, pro: true, enterprise: true },
                    { feature: "Custom Integrations", starter: false, pro: false, enterprise: true },
                    { feature: "White-label Options", starter: false, pro: false, enterprise: true }
                  ].map((row, index) => (
                    <tr key={index} className="border-b border-border-dark/50">
                      <td className="py-4 px-6 text-light-gray">{row.feature}</td>
                      <td className="py-4 px-6 text-center">
                        {typeof row.starter === 'boolean' ? (
                          row.starter ? <Check className="w-5 h-5 text-teal mx-auto" /> : <X className="w-5 h-5 text-muted-gray mx-auto" />
                        ) : (
                          <span className="text-light-gray">{row.starter}</span>
                        )}
                      </td>
                      <td className="py-4 px-6 text-center">
                        {typeof row.pro === 'boolean' ? (
                          row.pro ? <Check className="w-5 h-5 text-teal mx-auto" /> : <X className="w-5 h-5 text-muted-gray mx-auto" />
                        ) : (
                          <span className="text-light-gray">{row.pro}</span>
                        )}
                      </td>
                      <td className="py-4 px-6 text-center">
                        {typeof row.enterprise === 'boolean' ? (
                          row.enterprise ? <Check className="w-5 h-5 text-teal mx-auto" /> : <X className="w-5 h-5 text-muted-gray mx-auto" />
                        ) : (
                          <span className="text-light-gray">{row.enterprise}</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        {/* FAQ Section */}
        <div className="mb-20">
          <h2 className="text-3xl font-heading font-bold text-light-gray text-center mb-12">
            Frequently Asked Questions
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card variant="glass" className="p-6">
                  <h3 className="text-lg font-heading font-semibold text-light-gray mb-3">
                    {faq.question}
                  </h3>
                  <p className="text-muted-gray leading-relaxed">
                    {faq.answer}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Contact Section */}
        <div className="text-center">
          <Card variant="glass" className="p-12">
            <h2 className="text-3xl font-heading font-bold text-light-gray mb-4">
              Need a Custom Solution?
            </h2>
            <p className="text-xl text-muted-gray mb-8 max-w-2xl mx-auto">
              We work with large organizations to create tailored solutions. 
              Contact our sales team to discuss your specific requirements.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="gradient" size="lg">
                <Headphones className="w-5 h-5 mr-2" />
                Contact Sales
              </Button>
              <Button variant="outline" size="lg" className="text-light-gray border-border-dark">
                <MessageSquare className="w-5 h-5 mr-2" />
                Schedule Demo
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;
