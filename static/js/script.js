const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-header nav");

menuToggle.addEventListener("click", () => {
    siteNav.classList.toggle("active");

    if (siteNav.classList.contains("active")) {
        menuToggle.textContent = "\u00d7";
    } else {
        menuToggle.textContent = "\u2630";
    }
});