// tailwind.config.ts
import type { Config } from "tailwindcss";
import defaultTheme from "tailwindcss/defaultTheme";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#000000",
          light: "#fbfafa",
        },
        secondary: {
          DEFAULT: "#FA5C12",
        },
        accent: {
          DEFAULT: "#FFE4E0",
        },
        success: {
          DEFAULT: "#2EE5AC",
        },
        neutral: {
          DEFAULT: "#8C8C8C",
          white: "#FFFFFF",
          light: "#E5E5E5",
        },
        cyan: {
          DEFAULT: "#78FAE1",
        },
        gray: {
          light: "#E1E1E1",
          dark: "#979797",
        },
        "orange-light": "#FA5C12",
        "orange-dark": "#983000",
      },
      fontFamily: {
        sans: ["var(--font-inter)", ...defaultTheme.fontFamily.sans],
        heading: ["var(--font-raleway)", ...defaultTheme.fontFamily.sans],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {},
      keyframes: {},
    },
  },
  plugins: [animate, require("tailwind-scrollbar")],
};

export default config;
