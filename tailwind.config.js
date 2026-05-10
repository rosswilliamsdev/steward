/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*/templates/**/*.html',
    './*/static/**/*.{js,jsx,tsx}',
    './src/**/*.{js,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: 'hsl(142, 76%, 36%)',
          'primary-hover': 'hsl(142, 70%, 31%)',
          'primary-light': 'hsl(142, 76%, 85%)',
          'primary-dark': 'hsl(142, 76%, 20%)',
        },
        neutral: {
          50: 'hsl(0, 0%, 98%)',
          100: 'hsl(0, 0%, 96%)',
          200: 'hsl(0, 0%, 90%)',
          300: 'hsl(0, 0%, 83%)',
          400: 'hsl(0, 0%, 64%)',
          500: 'hsl(0, 0%, 45%)',
          600: 'hsl(0, 0%, 32%)',
          700: 'hsl(0, 0%, 25%)',
          800: 'hsl(0, 0%, 15%)',
          900: 'hsl(0, 0%, 9%)',
        },
        success: {
          DEFAULT: 'hsl(142, 76%, 36%)',
          light: 'hsl(142, 76%, 93%)',
        },
        error: {
          DEFAULT: 'hsl(0, 72%, 51%)',
          light: 'hsl(0, 93%, 94%)',
        },
        warning: {
          DEFAULT: 'hsl(38, 92%, 50%)',
          light: 'hsl(48, 96%, 89%)',
        },
        info: {
          DEFAULT: 'hsl(217, 91%, 60%)',
          light: 'hsl(214, 95%, 93%)',
        },
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      fontSize: {
        xs: ['12px', { lineHeight: '16px' }],
        sm: ['14px', { lineHeight: '20px' }],
        base: ['16px', { lineHeight: '24px' }],
        lg: ['18px', { lineHeight: '28px' }],
        xl: ['20px', { lineHeight: '28px' }],
        '2xl': ['24px', { lineHeight: '32px' }],
        '3xl': ['30px', { lineHeight: '36px' }],
      },
      spacing: {
        0: '0px',
        1: '8px',
        2: '16px',
        3: '24px',
        4: '32px',
        5: '40px',
        6: '48px',
        7: '64px',
        8: '80px',
      },
      borderRadius: {
        sm: '4px',
        DEFAULT: '6px',
        md: '8px',
        lg: '12px',
        full: '9999px',
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 2px 4px 0 rgba(0, 0, 0, 0.08)',
        md: '0 4px 8px 0 rgba(0, 0, 0, 0.12)',
        lg: '0 8px 16px 0 rgba(0, 0, 0, 0.16)',
      },
    },
  },
  plugins: [],
}

