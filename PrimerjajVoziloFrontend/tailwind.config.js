/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#fff000',
        secondary: '#ff00ff',
      }
    }
  },
  plugins: [
    require('daisyui'),
  ]
};