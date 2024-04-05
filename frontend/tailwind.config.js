/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  safelist: [
    "bg-secondary",
    "bg-squareblack",
    "bg-squarewhite",
    "text-squareblack",
    "text-squarewhite",
    "bg-squarewhite-selected",
    "bg-squareblack-selected",
    "bg-squareblack-check",
    "bg-squarewhite-check",
  ],
  theme: {
    extend: {
      colors: {
        "squareblack-selected": "#baca44",
        squareblack: "#769656",
        squarewhite: "#eeeed2",
        "squarewhite-selected": "#FFFF8A",
        primary: "#ffffff",
        secondary: "#302e2b",
        "squareblack-check": "#E2553E",
        "squarewhite-check": "#EB896F",
      },
      fontFamily: {
        primary: ["Montserrat", "sans-serif"],
      },
    },
  },
  plugins: [],
};
