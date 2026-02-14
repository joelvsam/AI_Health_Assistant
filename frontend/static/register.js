document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirm-password").value;

            if (password !== confirmPassword) {
                alert("Passwords do not match.");
                return;
            }

            try {
                const response = await fetch("http://localhost:8000/api/auth/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ name, email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    console.log("Registration successful:", data);
                    // Store the token and redirect to the dashboard
                    localStorage.setItem("accessToken", data.access_token);
                    window.location.href = "dashboard.html";
                } else {
                    console.error("Registration failed:", data);
                    alert("Registration failed: " + data.detail);
                }
            } catch (error) {
                console.error("Error during registration:", error);
                alert("An error occurred during registration.");
            }
        });
    }
});
