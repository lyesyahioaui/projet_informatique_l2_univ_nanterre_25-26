document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages');
    const chatForm = document.getElementById('chatForm');
    const questionInput = document.getElementById('question');

    // Auto-resize textarea
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question) return;

        // Clear empty state
        const emptyState = messagesContainer.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.innerHTML = `<div class="message-content">${escapeHtml(question)}</div>`;
        messagesContainer.appendChild(userMessage);

        // Clear input
        questionInput.value = '';
        questionInput.style.height = 'auto';

        // Show typing indicator
        const typingMessage = document.createElement('div');
        typingMessage.className = 'message ai';
        typingMessage.id = 'typing';
        typingMessage.innerHTML = `
            <div class="ai-icon">🤖</div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        messagesContainer.appendChild(typingMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Send request
        try {
            const formData = new FormData();
            formData.append('question', question);

            const response = await fetch('', {
                method: 'POST',
                body: formData
            });

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const responseElement = doc.querySelector('[data-response]');
            const reponse = responseElement ? responseElement.textContent : 'Erreur lors de la récupération';

            // Remove typing indicator
            document.getElementById('typing').remove();

            // Add AI response
            const aiMessage = document.createElement('div');
            aiMessage.className = 'message ai';
            aiMessage.innerHTML = `
                <div class="ai-icon">🤖</div>
                <div class="message-content">${escapeHtml(reponse)}</div>
            `;
            messagesContainer.appendChild(aiMessage);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

        } catch (error) {
            document.getElementById('typing').remove();
            const errorMessage = document.createElement('div');
            errorMessage.className = 'message ai';
            errorMessage.innerHTML = `
                <div class="ai-icon">⚠️</div>
                <div class="message-content">Erreur : ${escapeHtml(error.message)}</div>
            `;
            messagesContainer.appendChild(errorMessage);
        }
    });

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
