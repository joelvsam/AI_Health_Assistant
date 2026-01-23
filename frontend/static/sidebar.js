document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menu-btn");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");

    if (menuBtn && sidebar && mainContent) {
        // Start with the sidebar closed on page load for responsiveness
        sidebar.classList.remove("open");
        mainContent.classList.remove("shifted");

        menuBtn.addEventListener("click", function () {
            sidebar.classList.toggle("open");
            mainContent.classList.toggle("shifted");
        });
    }

    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault(); // Prevent default anchor behavior
            localStorage.removeItem("accessToken");
            window.location.href = "patient_signin.html";
        });
    }
});
