// Select elements
const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-header nav");
const themeToggle = document.querySelector(".theme-toggle");

// Toggle mobile navigation menu
menuToggle.addEventListener("click", () => {
    siteNav.classList.toggle("active");

    if (siteNav.classList.contains("active")) {
        menuToggle.textContent = "\u00d7";
    } else {
        menuToggle.textContent = "\u2630";
    }
});

// Load saved theme
const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    themeToggle.textContent = "Light";
} else {
    themeToggle.textContent = "Dark";
}

// Toggle dark mode
themeToggle.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";

    if (isDark) {
        document.documentElement.removeAttribute("data-theme");
        themeToggle.textContent = "Dark";
        localStorage.setItem("theme", "light");
    } else {
        document.documentElement.setAttribute("data-theme", "dark");
        themeToggle.textContent = "Light";
        localStorage.setItem("theme", "dark");
    }
});