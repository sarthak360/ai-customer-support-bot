document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    let sessionId = null;

    const startChat = () => {
        fetch('http://127.0.0.1:5000/start')
            .then(response => response.json())
            .then(data => {
                sessionId = data.session_id;
                addMessage('Hi! I am your AI support assistant. How can I help you today?', 'bot');
            })
            .catch(err => console.error("Error starting session:", err));
    };

    const sendMessage = () => {
        const message = userInput.value.trim();
        if (!message || !sessionId) return;

        addMessage(message, 'user');
        userInput.value = '';

        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: message }),
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot');
        })
        .catch(err => {
            console.error("Error sending message:", err);
            addMessage("I'm having trouble connecting. Please ensure the backend server is running.", 'bot');
        });
    };

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `${sender}-msg`;
        msgDiv.textContent = text;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    startChat();
});