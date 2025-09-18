import React from 'react';
import { Loader2 } from 'lucide-react';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  loading = false, 
  disabled = false, 
  className = '', 
  glow = false,
  ...props 
}) => {
  const baseClasses = 'relative inline-flex items-center justify-center font-heading font-semibold tracking-wide uppercase transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-azure/50 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden';
  
  const variants = {
    primary: 'bg-gradient-premium text-white shadow-lg hover:shadow-[0_0_30px_rgba(79,157,255,0.5)] hover:scale-105 active:scale-100',
    secondary: 'bg-charcoal border border-border-dark text-light-gray hover:bg-charcoal/80 hover:border-azure/50',
    outline: 'border-2 border-azure text-azure hover:bg-azure hover:text-white',
    danger: 'bg-danger hover:bg-danger/90 text-white shadow-lg hover:shadow-danger/50',
    ghost: 'text-muted-gray hover:text-light-gray hover:bg-charcoal/50',
    gradient: 'bg-gradient-to-r from-azure via-teal to-azure bg-[length:200%_100%] text-white shadow-lg hover:shadow-[0_0_40px_rgba(79,157,255,0.6)] hover:scale-105 animate-gradient-shift'
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-xs rounded-lg',
    md: 'px-6 py-3 text-sm rounded-xl',
    lg: 'px-8 py-4 text-base rounded-xl',
    xl: 'px-10 py-5 text-lg rounded-2xl'
  };

  const glowEffect = glow ? 'btn-glow' : '';
  
  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${glowEffect} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {/* Shimmer effect for primary buttons */}
      {variant === 'primary' && (
        <div className="absolute inset-0 -top-[2px] bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000" />
      )}
      
      {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
      {children}
    </button>
  );
};

export default Button;
