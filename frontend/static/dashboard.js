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
            document.getElementById("patient-name").textContent = data.name;
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

    const uploadForm = document.getElementById("upload-form");
    if (uploadForm) {
        uploadForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const fileInput = document.getElementById("file-input");
            const file = fileInput.files[0];
            const resultDiv = document.getElementById("upload-result");

            if (!file) {
                resultDiv.innerHTML = "<p style='color: red;'>Please select a file.</p>";
                return;
            }

            const formData = new FormData();
            formData.append("file", file);

            resultDiv.innerHTML = "<p>Uploading and analyzing...</p>";

            try {
                const response = await fetch("http://localhost:8000/documents/upload", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                    body: formData,
                });

                const data = await response.json();

                if (response.ok) {
                    let resultHTML = `
                        <h3>Analysis Complete</h3>
                        <p><strong>Filename:</strong> ${data.filename}</p>
                        <p><strong>Explanation:</strong> ${data.explanation}</p>
                    `;
                    if (data.indexed_for_rag) {
                        resultHTML += "<p style='color: green;'>Document content is now available for chat.</p>";
                    }
                    resultDiv.innerHTML = resultHTML;
                } else {
                    resultDiv.innerHTML = `<p style='color: red;'>Error: ${data.detail || "An unknown error occurred."}</p>`;
                }
            } catch (error) {
                console.error("Error uploading file:", error);
                resultDiv.innerHTML = "<p style='color: red;'>An error occurred while uploading the file.</p>";
            }
        });
    }
});
