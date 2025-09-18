import React from 'react';

const Card = ({ 
  children, 
  variant = 'default', 
  className = '', 
  hover = false,
  glow = false,
  ...props 
}) => {
  const baseClasses = 'rounded-2xl transition-all duration-300 relative overflow-hidden';
  
  const variants = {
    default: 'bg-charcoal border border-border-dark shadow-xl',
    glass: 'glass shadow-2xl',
    gradient: 'bg-gradient-to-br from-charcoal via-charcoal/90 to-midnight border border-border-dark shadow-xl',
    elevated: 'bg-charcoal border border-border-dark shadow-2xl hover:shadow-[0_20px_60px_rgba(0,0,0,0.8)]',
    premium: 'bg-gradient-to-br from-charcoal to-midnight border border-azure/20 shadow-[0_0_40px_rgba(79,157,255,0.1)]'
  };
  
  const hoverEffects = hover ? 'card-hover hover:border-azure/30 cursor-pointer group' : '';
  const glowEffects = glow ? 'hover:shadow-[0_0_40px_rgba(79,157,255,0.3)]' : '';
  
  return (
    <div
      className={`${baseClasses} ${variants[variant]} ${hoverEffects} ${glowEffects} ${className}`}
      {...props}
    >
      {/* Premium gradient border effect */}
      {variant === 'premium' && (
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-azure via-teal to-azure opacity-20 blur-xl -z-10" />
      )}
      {children}
    </div>
  );
};

const CardHeader = ({ children, className = '', icon = null }) => (
  <div className={`p-6 pb-4 border-b border-border-dark/50 ${className}`}>
    {icon && (
      <div className="flex items-center space-x-4">
        <div className="p-3 bg-azure/10 rounded-xl">
          {icon}
        </div>
        <div className="flex-1">
          {children}
        </div>
      </div>
    )}
    {!icon && children}
  </div>
);

const CardContent = ({ children, className = '' }) => (
  <div className={`p-6 ${className}`}>
    {children}
  </div>
);

const CardFooter = ({ children, className = '' }) => (
  <div className={`p-6 pt-4 border-t border-border-dark/50 ${className}`}>
    {children}
  </div>
);

Card.Header = CardHeader;
Card.Content = CardContent;
Card.Footer = CardFooter;

export default Card;
