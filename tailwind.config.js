/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      maxWidth: {
        '4/5': '80%',
      },
      height: {
        'screen/60': '60vh',
      },
    },
  },
  plugins: [],
}

