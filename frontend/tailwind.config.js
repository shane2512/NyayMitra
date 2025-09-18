/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // NyayMitra Professional Dark Mode Palette
        'midnight': '#0B0F19',        // Primary Background
        'charcoal': '#1C2230',        // Secondary Background
        'azure': '#4F9DFF',           // Primary Accent (CTAs, buttons)
        'teal': '#00C896',            // Secondary Accent (positive)
        'amber': '#F5A524',           // Warning/Alert
        'danger': '#F65A5A',          // High Risk/Errors
        'light-gray': '#E5E7EB',     // Primary Text
        'muted-gray': '#9CA3AF',      // Secondary Text
        'border-dark': '#2C3440',     // Borders/Dividers
        
        // Enhanced semantic colors
        'background': {
          'primary': '#0B0F19',
          'secondary': '#1C2230',
          'tertiary': '#2C3440',
        },
        'accent': {
          'primary': '#4F9DFF',
          'secondary': '#00C896',
        },
        'text': {
          'primary': '#E5E7EB',
          'secondary': '#9CA3AF',
          'muted': '#6B7280',
        },
        'status': {
          'success': '#00C896',
          'warning': '#F5A524',
          'error': '#F65A5A',
          'info': '#4F9DFF',
        }
      },
      fontFamily: {
        'heading': ['Inter', 'sans-serif'],           // SaaS UI headings
        'legal': ['Neuton', 'serif'],                 // Legal/contract contexts
        'body': ['IBM Plex Sans', 'sans-serif'],      // Body text
        'mono': ['JetBrains Mono', 'monospace'],      // Code/clauses
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-glow': 'pulseGlow 2s infinite',
        'gradient-shift': 'gradientShift 3s ease infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(79, 157, 255, 0.5)' },
          '50%': { boxShadow: '0 0 40px rgba(79, 157, 255, 0.8)' },
        },
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      backdropBlur: {
        'xs': '2px',
        'glass': '12px',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-premium': 'linear-gradient(135deg, #4F9DFF 0%, #00C896 100%)',
        'gradient-dark': 'linear-gradient(180deg, #0B0F19 0%, #1C2230 100%)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}