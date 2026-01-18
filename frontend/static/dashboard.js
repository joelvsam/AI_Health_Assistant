document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("accessToken");

    if (!token) {
        window.location.href = "patient_signin.html";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/auth/users/me", {
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("patient-name").textContent = data.email; // Assuming email is the name for now
            document.getElementById("patient-email").textContent = data.email;
        } else {
            console.error("Failed to fetch user info:", data);
            // Might need to redirect to login if token is invalid
            if (response.status === 401) {
                window.location.href = "patient_signin.html";
            }
        }
    } catch (error) {
        console.error("Error fetching user info:", error);
    }

    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("accessToken");
            window.location.href = "patient_signin.html";
        });
    }
});
