document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("http://localhost:8000/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    console.log("Login successful:", data);
                    localStorage.setItem("accessToken", data.access_token);
                    window.location.href = "dashboard.html";
                } else {
                    console.error("Login failed:", data);
                    alert("Login failed: " + data.detail);
                }
            } catch (error) {
                console.error("Error during login:", error);
            }
        });
    }
});
