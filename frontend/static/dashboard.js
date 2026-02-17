document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("accessToken");
    const apiBase = "http://localhost:8000/api";

    if (!token) {
        window.location.href = "patient_signin.html";
        return;
    }

    await loadPatientInfo(token, apiBase);
    setupDocumentUpload(token, apiBase);
    setupDocumentChat(token, apiBase);
});

async function loadPatientInfo(token, apiBase) {
    try {
        const response = await fetch(`${apiBase}/auth/users/me`, {
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
            if (response.status === 401) {
                window.location.href = "patient_signin.html";
            }
        }
    } catch (error) {
        console.error("Error fetching user info:", error);
    }
}

function setupDocumentUpload(token, apiBase) {
    const uploadForm = document.getElementById("upload-form");
    const resultDiv = document.getElementById("upload-result");

    if (!uploadForm || !resultDiv) {
        return;
    }

    uploadForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const fileInput = document.getElementById("file-input");
        const file = fileInput.files[0];

        if (!file) {
            resultDiv.innerHTML = "<p class='text-error'>Please select a file.</p>";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        resultDiv.innerHTML = "<p>Uploading and analyzing...</p>";

        try {
            const response = await fetch(`${apiBase}/documents/upload`, {
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
                    resultHTML += "<p class='text-success'>Document content is now available for chat.</p>";
                }

                resultDiv.innerHTML = resultHTML;
            } else {
                resultDiv.innerHTML = `<p class='text-error'>Error: ${data.detail || "An unknown error occurred."}</p>`;
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            resultDiv.innerHTML = "<p class='text-error'>An error occurred while uploading the file.</p>";
        }
    });
}

function setupDocumentChat(token, apiBase) {
    const chatForm = document.getElementById("doc-chat-form");
    const chatInput = document.getElementById("doc-chat-input");
    const chatWindow = document.getElementById("doc-chat-window");

    if (!chatForm || !chatInput || !chatWindow) {
        return;
    }

    chatForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const message = chatInput.value.trim();

        if (!message) {
            return;
        }

        addMessage(chatWindow, message, "user-message");
        chatInput.value = "";

        try {
            const response = await fetch(`${apiBase}/chat/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ query: message }),
            });

            const data = await response.json();

            if (response.ok) {
                addMessage(chatWindow, data.answer, "ai-message");
            } else {
                addMessage(chatWindow, `Error: ${data.detail || "Unknown error"}`, "ai-message");
            }
        } catch (error) {
            console.error("Chat error:", error);
            addMessage(chatWindow, "An error occurred while chatting.", "ai-message");
        }
    });
}

function addMessage(chatWindow, message, senderClass) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("chat-message", senderClass);
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
