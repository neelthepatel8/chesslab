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
    "bg-squarewhite-selected",
    "bg-squareblack-selected",
  ],
  theme: {
    extend: {
      colors: {
        "squareblack-selected": "#baca44",
        squareblack: "#769656",
        squarewhite: "#eeeed2",
        "squarewhite-selected": "#FFFF8A",
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
