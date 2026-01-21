document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatMessages = document.getElementById("chat-messages");
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

        fetch("http://localhost:8000/ai/explain", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({ text: messageText }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.explanation) {
                appendMessage(data.explanation, "ai-message");
            } else {
                appendMessage("Sorry, I couldn't process that.", "ai-message");
            }
        })
        .catch(error => {
            console.error("Error with AI explanation:", error);
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
