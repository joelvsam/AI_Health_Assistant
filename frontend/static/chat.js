document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("accessToken");
    
    function initializeChat(token) {
        const chatForm = document.getElementById("chat-form");
        const chatInput = document.getElementById("chat-input");
        const chatWindow = document.getElementById("chat-window");

        if (chatForm) {
            chatForm.addEventListener("submit", async function (e) {
                e.preventDefault();
                const message = chatInput.value.trim();

                if (!message) return;

                addMessage(message, "user");
                chatInput.value = "";

                try {
                    const response = await fetch("http://localhost:8000/api/chat/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`,
                        },
                        body: JSON.stringify({ query: message }),
                    });

                    const data = await response.json();

                    if (response.ok) {
                        addMessage(data.answer, "bot");
                    } else {
                        addMessage(`Error: ${data.detail || "Unknown error"}`, "bot");
                    }
                } catch (error) {
                    console.error("Chat error:", error);
                    addMessage("An error occurred while chatting.", "bot");
                }
            });
        }

        function addMessage(message, sender) {
            const messageElement = document.createElement("div");
            messageElement.classList.add("chat-message", `${sender}-message`);
            messageElement.textContent = message;
            chatWindow.appendChild(messageElement);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }

    initializeChat(token);
});
