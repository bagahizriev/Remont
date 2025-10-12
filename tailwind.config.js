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
                border: "var(--border)",
            },
        },
    },

    plugins: [],
};
