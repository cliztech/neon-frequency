/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                neon: {
                    cyan: "#00f3ff",
                    pink: "#ff00ff",
                    purple: "#bc13fe",
                    green: "#0aff00",
                },
                dark: {
                    bg: "#050510",
                    surface: "#0a0a1f",
                    deep: "#020205",
                }
            },
            fontFamily: {
                sans: ['Outfit', 'sans-serif'],
                mono: ['Rajdhani', 'monospace'],
            },
            animation: {
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'spin-slow': 'spin 12s linear infinite',
            },
            backgroundImage: {
                'grid-pattern': "linear-gradient(to right, #ffffff05 1px, transparent 1px), linear-gradient(to bottom, #ffffff05 1px, transparent 1px)",
            }
        },
    },
    plugins: [],
}
