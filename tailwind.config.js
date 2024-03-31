/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  safelist: [
    "bg-squareblack",
    "bg-squarewhite",
    "text-squareblack",
    "text-squarewhite",
  ],
  theme: {
    extend: {
      colors: {
        squareblack: "#769656",
        squarewhite: "#eeeed2",
        lightgreen: "#baca44",
        primary: "#ffffff",
        secondary: "#000000",
      },
      fontFamily: {
        primary: ["Montserrat", "sans-serif"],
      },
    },
  },
  plugins: [],
};
