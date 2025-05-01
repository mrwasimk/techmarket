document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const body = document.body;
    const icon = themeToggleButton.querySelector('i');

    // --- Helper Functions ---
    const setCookie = (name, value, days) => {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        // Set cookie to be available across the entire site
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    };

    const getCookie = (name) => {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    };

    const applyTheme = (theme) => {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            themeToggleButton.setAttribute('aria-label', 'Switch to light mode');
        } else {
            body.classList.remove('dark-mode');
            themeToggleButton.setAttribute('aria-label', 'Switch to dark mode');
        }
    };

    // --- Initialization ---
    // Get the current theme from cookie or default to 'light'
    let currentTheme = getCookie('theme') || 'light';
    applyTheme(currentTheme); // Apply theme on initial load

    // --- Event Listener ---
    themeToggleButton.addEventListener('click', () => {
        // Toggle theme
        currentTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';

        // Apply the new theme visually
        applyTheme(currentTheme);

        // Save the preference in a cookie for 365 days
        setCookie('theme', currentTheme, 365);
    });
});
