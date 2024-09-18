/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#fff000',
        secondary: '#ff00ff',
      },
      gridTemplateColumns: {
        'vehicle-info': '1fr 2fr',
      },
      gridTemplateRows: {
        'vehicle-info': '1fr 2fr',
      }
    }
  },
  safelist: [
    'text-green-500',
    'text-blue-500',
    'text-yellow-500',
    'text-fuchsia-500',
  ],
  plugins: [
    require('daisyui'),
  ]
};