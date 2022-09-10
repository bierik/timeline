const config = {
  theme: {
    container: {
      center: true,
      screens: {
        sm: '600px',
        md: '728px',
        lg: '984px',
        xl: '984px',
        '2xl': '984px',
      },
      padding: '1rem',
    },
    extend: {
      fontFamily: {
        dymo: 'Courier Prime',
      },
      colors: {
        primary: {
          DEFAULT: 'var(--color-primary-DEFAULT)',
          50: 'var(--color-primary-50)',
          100: 'var(--color-primary-100)',
          200: 'var(--color-primary-200)',
          300: 'var(--color-primary-300)',
          400: 'var(--color-primary-400)',
          500: 'var(--color-primary-500)',
          600: 'var(--color-primary-600)',
          700: 'var(--color-primary-700)',
          800: 'var(--color-primary-800)',
          900: 'var(--color-primary-900)',
        },
      },
      boxShadow: {
        flat: `0 0 0 6px var(--color-primary-200)`,
        'flat-lg': `0 0 0 10px var(--color-primary-200)`,
      },
    },
  },
}

module.exports = config
