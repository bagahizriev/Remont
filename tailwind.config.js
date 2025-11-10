/** @type {import('tailwindcss').Config} */

module.exports = {
    content: ["./**/*.html"],

    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                "background-secondary": "var(--background-secondary)",
                foreground: "var(--foreground)",
                secondary: "var(--secondary)",
                card: "var(--card)",
                "card-secondary": "var(--card-secondary)",
                "border-300": "var(--border-300)",
                "border-100": "var(--border-100)",
            },
        },
    },

    plugins: [],
};
