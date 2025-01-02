import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2e2066', // Deep Purple
          hover: '#3a2980',
          light: '#4a3990',
          ultralight: '#efeeff', // New ultralight purple
          faded: '#f5f3ff', // New faded purple
        },
        accent: {
          DEFAULT: '#bf3abb', // Vibrant Pink
          hover: '#d042cc',
          light: '#d66ed2',
          ultralight: '#fdf1ff', // New ultralight pink
          faded: '#fcf5fe', // New faded pink
        },
        background: {
          dark: '#0c0c1c', // Midnight Blue
          light: '#f4f4f4',
          glass: 'rgba(12, 12, 28, 0.8)',
          'glass-light': 'rgba(12, 12, 28, 0.6)',
        },
        secondary: {
          DEFAULT: '#7c71d8', // Soft Lavender
          light: '#9a91e6',
          dark: '#6258c4',
          ultralight: '#f3f1ff', // New ultralight lavender
          faded: '#f8f7ff', // New faded lavender
        },
        peach: {
          DEFAULT: '#ffadc0', // Pinkish-peach highlight
          hover: '#ffa5b8',
          light: '#ffc7d3',
          ultralight: '#ffeef2',
          faded: '#fff6f8',
        },
        neutral: {
          100: '#f4f4f4',
          200: '#e4e4e7',
          300: '#d1d1d1',
          400: '#a1a1aa',
          500: '#999999',
          600: '#52525b',
          700: '#666666',
          800: '#27272a',
          900: '#333333',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display-lg': ['64px', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
        'display': ['48px', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
        'h1': ['40px', { lineHeight: '1.2', letterSpacing: '-0.01em' }],
        'h2': ['32px', { lineHeight: '1.3' }],
        'h3': ['24px', { lineHeight: '1.4' }],
        'body-lg': ['18px', { lineHeight: '1.6' }],
        'body': ['16px', { lineHeight: '1.6' }],
        'small': ['14px', { lineHeight: '1.5' }],
      },
      spacing: {
        container: '2rem',
        'section-y': '5rem',
        'header': '4rem', // 64px
        'hero': '90vh',
      },
      height: {
        header: 'var(--header-height)',
        hero: 'var(--hero-height)',
      },
      minHeight: {
        hero: 'var(--hero-height)',
      },
      borderRadius: {
        DEFAULT: '4px',
        'lg': '8px',
        'xl': '12px',
        '2xl': '16px',
      },
      boxShadow: {
        'card': '0 2px 4px rgba(0,0,0,0.1)',
        'card-hover': '0 4px 8px rgba(0,0,0,0.15)',
        'header': '0 4px 6px rgba(0,0,0,0.05)',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #2e2066 0%, #bf3abb 100%)',
        'gradient-dark': 'linear-gradient(180deg, rgba(12, 12, 28, 0.8) 0%, rgba(12, 12, 28, 0.95) 100%)',
        'gradient-hero': 'radial-gradient(circle at top, var(--tw-gradient-stops))',
        'gradient-glow': 'radial-gradient(circle at center, var(--tw-gradient-stops))',
        'gradient-neuromosaic': 'radial-gradient(circle, #2e2066 0%, #7c71d8 30%, #bf3abb 60%, #ffadc0 85%, #ffeef2 100%)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
    },
  },
  plugins: [],
};

export default config;
