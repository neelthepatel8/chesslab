/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        darkgreen: "#769656",
        offwhite: "#eeeed2",
        lightgreen: "#baca44",
        primary: "#ffffff",
        secondary: "#000000",
      },
    },
  },
  plugins: [],
};
