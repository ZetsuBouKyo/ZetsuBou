const defaultTheme = require("tailwindcss/defaultTheme");
const plugin = require("tailwindcss/plugin");

/** @type {import("@types/tailwindcss/tailwind-config").TailwindConfig } */
module.exports = {
  mode: "jit",
  purge: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        "fade-in": "fade-in 1.2s cubic-bezier(0.390, 0.575, 0.565, 1.000) both",
        "slide-in": "slide-in 0.5s forwards",
        "shake-horizontal": "shake-horizontal 0.4s cubic-bezier(0.455, 0.030, 0.515, 0.955) both",
        "scale-in-center": "scale-in-center 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both",
      },
      keyframes: {
        "fade-in": {
          "0%": {
            opacity: "0",
          },
          to: {
            opacity: "1",
          },
        },
        "slide-in": {
          "0%": {
            transform: "translateX(-100%)",
          },
          "100%": {
            transform: "translateX(0)",
          },
        },
        "shake-horizontal": {
          "0%,to": {
            transform: "translateX(0)",
          },
          "10%,30%,50%,70%": {
            transform: "translateX(-4px)",
          },
          "20%,40%,60%": {
            transform: "translateX(4px)",
          },
          "80%": {
            transform: "translateX(2px)",
          },
          "90%": {
            transform: "translateX(-2px)",
          },
        },
        "scale-in-center": {
          "0%": {
            transform: "scale(0)",
            opacity: "0",
          },
          to: {
            transform: "scale(1)",
            opacity: "1",
          },
        },
      },
      fontSize: {
        xxs: ["0.5rem", "0.75rem"],
      },
      fontFamily: {
        sans: ['"Inter var"', ...defaultTheme.fontFamily.sans],
      },
      margin: {
        "2px": "2px",
        "4px": "4px",
      },
      width: {
        "10v": "10vw",
        "20v": "20vw",
        "30v": "30vw",
        "40v": "40vw",
        "50v": "50vw",
        "60v": "60vw",
        "70v": "70vw",
        "80v": "80vw",
        "90v": "90vw",
        "100v": "100vh",
        "app-tagger": "calc(100vw - 4rem)",
        "1/10": "10%",
      },
      height: {
        "10v": "10vh",
        "20v": "20vh",
        "30v": "30vh",
        "40v": "40vh",
        "50v": "50vh",
        "60v": "60vh",
        "70v": "70vh",
        "80v": "80vh",
        "90v": "90vh",
        "100v": "100vh",
        app: "calc(100vh - 5rem)",
        table: "calc(100vh - 10rem)",
        120: "30rem",
      },
      minHeight: {
        14: "3.5rem",
        app: "calc(100vh - 5rem)",
      },
      maxHeight: {
        "1/2": "50%",
        "80v": "80vh",
      },
      maxWidth: {
        "1/4": "25%",
        "1/2": "50%",
        48: "12rem",
        72: "18rem",
        80: "20rem",
        96: "24rem",
      },
      boxShadow: {
        black: "0 4px 14px 0 rgba(0, 0, 0, 1)",
        "gray-900": "0 4px 14px 0 rgba(17, 24, 39, 1)",
      },
      screens: {
        "3xl": "2690px",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    plugin(function ({ addUtilities }) {
      const scrollbar = {
        ".zetsubou-scrollbar": {
          "&::-webkit-scrollbar": {
            "border-radius": "10px",
            width: "12px",
            height: "100%",
            "background-color": "rgb(240,240,240)",
          },
          "&::-webkit-scrollbar-thumb": {
            "background-color": "rgb(172,172,172)",
            "border-radius": "10px",
          },
          "&::-webkit-scrollbar-thumb:hover": {
            "background-color": "rgb(122,122,122)",
          },
        },
      };
      addUtilities(scrollbar);
    }),
    plugin(function ({ addUtilities }) {
      const ripple = {
        "span.zetsubou-ripple": {
          position: "absolute",
          "border-radius": "50%",
          transform: "scale(0)",
          animation: "ripple 600ms linear",
          "background-color": "rgba(255, 255, 255, 0.7)",
        },
        "@keyframes ripple": {
          to: {
            transform: "scale(4)",
            opacity: "0",
          },
        },
      };

      addUtilities(ripple);
    }),
  ],
};
