import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["https://database-zuma.github.io", "http://localhost:*"])
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# System prompt untuk ZUMA AI Assistant
SYSTEM_PROMPT = """Kamu adalah ZUMA AI Assistant, asisten cerdas untuk PT ZUMA yang membantu analisis stock dan sales.

KEMAMPUAN KAMU:
1. **Stock Monitor** - Menganalisis stock, identifikasi stock critical, rekomendasi restock
2. **Sales Analyst** - Menganalisis penjualan, trend, performance toko dan SPG
3. **Report Generator** - Membuat ringkasan laporan stock dan sales
4. **General Assistant** - Menjawab pertanyaan umum tentang bisnis ZUMA

KONTEKS BISNIS ZUMA:
- ZUMA adalah brand sandal dengan beberapa warehouse: WH Pusat (Jatim), WH Bali, WH Jakarta
- Memiliki banyak retail store di berbagai area: Bali, Jakarta, Jawa Timur, Batam, Sulawesi, Sumatera, Lombok
- Produk dikategorikan berdasarkan Gender (Men, Ladies, Baby, Boys, Girls, Junior) dan Tier (1-5)
- Metrics penting: TW (Turnover Weeks) = Stock WH / Avg Sales, TO (Turnover) = Stock Toko / Avg Sales

CARA MERESPONS:
- Gunakan bahasa Indonesia yang friendly dan profesional
- Berikan analisis yang actionable dan praktis
- Jika ditanya data spesifik yang tidak kamu punya, minta user untuk share datanya
- Format jawaban dengan bullet points atau tabel jika membantu

Selalu siap membantu tim ZUMA!"""

# Conversation history storage (in-memory, reset on restart)
conversations = {}

def get_ai_response(user_message, session_id="default"):
    """Get response from OpenRouter API using Claude"""

    if not OPENROUTER_API_KEY:
        return "Error: API Key belum di-set. Silakan set OPENROUTER_API_KEY di environment variables."

    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []

    # Add user message to history
    conversations[session_id].append({
        "role": "user",
        "content": user_message
    })

    # Keep only last 20 messages to avoid token limits
    if len(conversations[session_id]) > 20:
        conversations[session_id] = conversations[session_id][-20:]

    # Prepare messages with system prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + conversations[session_id]

    try:
        response = requests.post(
            OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://zuma-ai-agent.railway.app",
                "X-Title": "ZUMA AI Assistant"
            },
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": messages,
                "max_tokens": 2048,
                "temperature": 0.7
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']

            # Add assistant response to history
            conversations[session_id].append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message
        else:
            return f"Error: API returned status {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        return "Error: Request timeout. Coba lagi."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    """Render main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')

    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    response = get_ai_response(user_message, session_id)

    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    data = request.json
    session_id = data.get('session_id', 'default')

    if session_id in conversations:
        conversations[session_id] = []

    return jsonify({'status': 'cleared'})

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_configured': bool(OPENROUTER_API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


