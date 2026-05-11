/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*/templates/**/*.html',
    './*/static/**/*.{js,jsx,tsx}',
    './static/**/*.{js,jsx,tsx}',
    './src/**/*.{js,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Surface colors
        'surface': 'hsl(93, 53%, 97%)',
        'surface-dim': 'hsl(100, 11%, 85%)',
        'surface-bright': 'hsl(93, 53%, 97%)',
        'surface-container-lowest': 'hsl(0, 0%, 100%)',
        'surface-container-low': 'hsl(93, 31%, 94%)',
        'surface-container': 'hsl(93, 22%, 92%)',
        'surface-container-high': 'hsl(100, 18%, 90%)',
        'surface-container-highest': 'hsl(93, 14%, 88%)',
        'surface-variant': 'hsl(93, 14%, 88%)',
        'surface-tint': 'hsl(146, 100%, 21%)',

        // Primary colors
        'primary': 'hsl(146, 100%, 20%)',
        'on-primary': 'hsl(0, 0%, 100%)',
        'primary-container': 'hsl(142, 72%, 29%)',
        'on-primary-container': 'hsl(123, 100%, 91%)',
        'inverse-primary': 'hsl(132, 58%, 67%)',
        'primary-fixed': 'hsl(131, 88%, 78%)',
        'primary-fixed-dim': 'hsl(132, 58%, 67%)',
        'on-primary-fixed': 'hsl(138, 100%, 6%)',
        'on-primary-fixed-variant': 'hsl(145, 100%, 16%)',

        // Secondary colors
        'secondary': 'hsl(129, 21%, 33%)',
        'on-secondary': 'hsl(0, 0%, 100%)',
        'secondary-container': 'hsl(123, 53%, 85%)',
        'on-secondary-container': 'hsl(127, 20%, 36%)',
        'secondary-fixed': 'hsl(123, 53%, 85%)',
        'secondary-fixed-dim': 'hsl(123, 29%, 74%)',
        'on-secondary-fixed': 'hsl(138, 100%, 6%)',
        'on-secondary-fixed-variant': 'hsl(131, 28%, 24%)',

        // Tertiary colors
        'tertiary': 'hsl(43, 85%, 35%)',
        'on-tertiary': 'hsl(0, 0%, 100%)',
        'tertiary-container': 'hsl(43, 90%, 88%)',
        'on-tertiary-container': 'hsl(43, 85%, 20%)',
        'tertiary-fixed': 'hsl(43, 90%, 88%)',
        'tertiary-fixed-dim': 'hsl(43, 85%, 75%)',
        'on-tertiary-fixed': 'hsl(43, 100%, 10%)',
        'on-tertiary-fixed-variant': 'hsl(43, 85%, 25%)',

        // Background colors
        'background': 'hsl(93, 53%, 97%)',
        'on-background': 'hsl(110, 12%, 10%)',

        // Text/surface colors
        'on-surface': 'hsl(110, 12%, 10%)',
        'on-surface-variant': 'hsl(120, 7%, 27%)',
        'inverse-surface': 'hsl(120, 6%, 18%)',
        'inverse-on-surface': 'hsl(93, 26%, 93%)',

        // Outline colors
        'outline': 'hsl(115, 5%, 45%)',
        'outline-variant': 'hsl(111, 12%, 76%)',

        // Error colors
        'error': 'hsl(0, 75%, 42%)',
        'on-error': 'hsl(0, 0%, 100%)',
        'error-container': 'hsl(6, 100%, 92%)',
        'on-error-container': 'hsl(356, 100%, 29%)',
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
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

