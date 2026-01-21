<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZUMA AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .chat-container {
            width: 100%;
            max-width: 800px;
            height: 90vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.25);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .chat-header h1 {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }

        .chat-header p {
            font-size: 0.85rem;
            opacity: 0.9;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8fafc;
        }

        .message {
            margin-bottom: 16px;
            display: flex;
            flex-direction: column;
        }

        .message.user {
            align-items: flex-end;
        }

        .message.assistant {
            align-items: flex-start;
        }

        .message-bubble {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 16px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message.user .message-bubble {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message.assistant .message-bubble {
            background: white;
            color: #1f2937;
            border: 1px solid #e5e7eb;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .message-time {
            font-size: 0.7rem;
            color: #9ca3af;
            margin-top: 4px;
            padding: 0 8px;
        }

        .chat-input-container {
            padding: 16px 20px;
            background: white;
            border-top: 1px solid #e5e7eb;
        }

        .chat-input-wrapper {
            display: flex;
            gap: 12px;
            align-items: flex-end;
        }

        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            resize: none;
            min-height: 48px;
            max-height: 120px;
            font-family: inherit;
            transition: border-color 0.2s;
        }

        .chat-input:focus {
            outline: none;
            border-color: #6366f1;
        }

        .send-btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }

        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            border-bottom-left-radius: 4px;
            margin-bottom: 16px;
            width: fit-content;
        }

        .typing-indicator.show {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: #9ca3af;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }

        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 12px 20px;
            background: #f8fafc;
            border-top: 1px solid #e5e7eb;
        }

        .quick-btn {
            padding: 8px 14px;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #4b5563;
            cursor: pointer;
            transition: all 0.2s;
        }

        .quick-btn:hover {
            background: #6366f1;
            color: white;
            border-color: #6366f1;
        }

        .clear-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 8px 12px;
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 0.8rem;
            cursor: pointer;
            transition: background 0.2s;
        }

        .clear-btn:hover {
            background: rgba(255,255,255,0.3);
        }

        .chat-header {
            position: relative;
        }

        /* Markdown-like formatting */
        .message-bubble strong { font-weight: 600; }
        .message-bubble code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .chat-container {
                height: 100vh;
                border-radius: 0;
            }

            .message-bubble {
                max-width: 90%;
            }

            .quick-actions {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <button class="clear-btn" onclick="clearChat()">Clear Chat</button>
            <h1>ZUMA AI Assistant</h1>
            <p>Stock Monitor | Sales Analyst | Report Generator</p>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message assistant">
                <div class="message-bubble">
                    Halo! Saya ZUMA AI Assistant. Saya bisa membantu kamu dengan:

<strong>1. Stock Monitor</strong> - Analisis stock, identifikasi critical items
<strong>2. Sales Analyst</strong> - Analisis penjualan dan trend
<strong>3. Report Generator</strong> - Buat ringkasan laporan
<strong>4. General Questions</strong> - Pertanyaan umum tentang bisnis

Silakan tanya apa saja tentang stock atau sales ZUMA!
                </div>
                <span class="message-time">Just now</span>
            </div>
        </div>

        <div class="quick-actions">
            <button class="quick-btn" onclick="sendQuickMessage('Apa saja stock yang critical saat ini?')">Stock Critical</button>
            <button class="quick-btn" onclick="sendQuickMessage('Bagaimana performa sales bulan ini?')">Performa Sales</button>
            <button class="quick-btn" onclick="sendQuickMessage('Toko mana yang paling bagus performanya?')">Top Store</button>
            <button class="quick-btn" onclick="sendQuickMessage('Buatkan ringkasan laporan harian')">Laporan Harian</button>
            <button class="quick-btn" onclick="sendQuickMessage('Produk apa yang perlu restock?')">Rekomendasi Restock</button>
        </div>

        <div class="chat-input-container">
            <div class="chat-input-wrapper">
                <textarea
                    class="chat-input"
                    id="chatInput"
                    placeholder="Ketik pesan..."
                    rows="1"
                    onkeydown="handleKeyDown(event)"
                ></textarea>
                <button class="send-btn" id="sendBtn" onclick="sendMessage()">Kirim</button>
            </div>
        </div>
    </div>

    <script>
        const sessionId = 'session_' + Date.now();
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');

        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        function handleKeyDown(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        function formatTime(date) {
            return date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
        }

        function addMessage(content, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;

            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.textContent = content;

            const time = document.createElement('span');
            time.className = 'message-time';
            time.textContent = formatTime(new Date());

            messageDiv.appendChild(bubble);
            messageDiv.appendChild(time);
            chatMessages.appendChild(messageDiv);

            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showTyping() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator show';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideTyping() {
            const typing = document.getElementById('typingIndicator');
            if (typing) typing.remove();
        }

        async function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, true);
            chatInput.value = '';
            chatInput.style.height = 'auto';

            // Disable input
            sendBtn.disabled = true;
            chatInput.disabled = true;

            // Show typing indicator
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, session_id: sessionId })
                });

                const data = await response.json();
                hideTyping();

                if (data.response) {
                    addMessage(data.response, false);
                } else if (data.error) {
                    addMessage('Error: ' + data.error, false);
                }
            } catch (error) {
                hideTyping();
                addMessage('Error: Tidak dapat terhubung ke server. ' + error.message, false);
            }

            // Re-enable input
            sendBtn.disabled = false;
            chatInput.disabled = false;
            chatInput.focus();
        }

        function sendQuickMessage(message) {
            chatInput.value = message;
            sendMessage();
        }

        async function clearChat() {
            if (!confirm('Clear semua chat history?')) return;

            try {
                await fetch('/clear', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId })
                });

                // Clear UI
                chatMessages.innerHTML = `
                    <div class="message assistant">
                        <div class="message-bubble">
                            Chat history cleared. Silakan mulai percakapan baru!
                        </div>
                        <span class="message-time">${formatTime(new Date())}</span>
                    </div>
                `;
            } catch (error) {
                alert('Error clearing chat: ' + error.message);
            }
        }

        // Focus input on load
        chatInput.focus();
    </script>
</body>
</html>
