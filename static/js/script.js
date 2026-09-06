const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-header nav");
const themeToggle = document.querySelector(".theme-toggle");

menuToggle.addEventListener("click", () => {
    siteNav.classList.toggle("active");

    if (siteNav.classList.contains("active")) {
        menuToggle.textContent = "\u00d7";
    } else {
        menuToggle.textContent = "\u2630";
    }
});

themeToggle.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";

    if (isDark) {
        document.documentElement.removeAttribute("data-theme");
        themeToggle.textContent = "Dark";
    } else {
        document.documentElement.setAttribute("data-theme", "dark");
        themeToggle.textContent = "Light";
    }
});