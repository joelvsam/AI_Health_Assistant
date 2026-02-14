document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatMessages = document.getElementById("chat-messages");
    const loadingIndicator = document.getElementById("loading-indicator"); // Add this line
    const token = localStorage.getItem("accessToken");

    if (!token) {
        window.location.href = "patient_signin.html";
        return;
    }

    sendBtn.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText === "") {
            return;
        }

        appendMessage(messageText, "user-message");
        chatInput.value = "";
        loadingIndicator.style.display = "flex"; // Show loading indicator

        fetch("http://localhost:8000/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({ query: messageText }),
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = "none"; // Hide loading indicator
            if (data.answer) {
                appendMessage(data.answer, "ai-message");
            } else {
                appendMessage("Sorry, I couldn't process that.", "ai-message");
            }
        })
        .catch(error => {
            console.error("Error with AI explanation:", error);
            loadingIndicator.style.display = "none"; // Hide loading indicator
            appendMessage("An error occurred. Please try again later.", "ai-message");
        });
    }

    function appendMessage(text, className) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", className);
        messageElement.textContent = text;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
    }
});
