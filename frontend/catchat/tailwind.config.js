/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/App.js', './src/components/**/*.js'],
  theme: {
    extend: {
      textColor: {
        'wcu-purple': '#592C88',
        'wcu-gold': '#C1A875',
      }
    },
  },
  plugins: [],
}