/**
 * Theme Toggle functionality for Hospital Management System
 * Handles switching between dark and light modes
 * Saves preference to localStorage
 */

(function() {
    'use strict';

    // Theme configuration
    const THEME_KEY = 'hms-theme-preference';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';
    const DEFAULT_THEME = THEME_DARK; // Default to dark mode

    // Get current theme from localStorage or default
    function getStoredTheme() {
        return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
    }

    // Save theme to localStorage
    function setStoredTheme(theme) {
        localStorage.setItem(THEME_KEY, theme);
    }

    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        updateToggleIcon(theme);
    }

    // Update toggle button icon based on current theme
    function updateToggleIcon(theme) {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        const icon = toggleBtn.querySelector('i');
        if (!icon) return;

        if (theme === THEME_DARK) {
            // Show sun icon (click to switch to light)
            icon.className = 'bi bi-sun-fill';
            toggleBtn.setAttribute('aria-label', 'Switch to light mode');
            toggleBtn.title = 'Switch to light mode';
        } else {
            // Show moon icon (click to switch to dark)
            icon.className = 'bi bi-moon-fill';
            toggleBtn.setAttribute('aria-label', 'Switch to dark mode');
            toggleBtn.title = 'Switch to dark mode';
        }
    }

    // Toggle between dark and light
    function toggleTheme() {
        const currentTheme = getStoredTheme();
        const newTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;

        applyTheme(newTheme);
        setStoredTheme(newTheme);
    }

    // Initialize theme on page load
    function initTheme() {
        const theme = getStoredTheme();
        applyTheme(theme);
    }

    // Setup toggle button event listener
    function setupToggleButton() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function(e) {
                e.preventDefault();
                toggleTheme();
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initTheme();
            setupToggleButton();
        });
    } else {
        // DOM already loaded
        initTheme();
        setupToggleButton();
    }
})();
