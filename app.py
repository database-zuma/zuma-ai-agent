import os
  import requests
  from flask import Flask, render_template, request, jsonify
  from flask_cors import CORS
  from datetime import datetime

  app = Flask(__name__)
  CORS(app, origins=["https://database-zuma.github.io", "http://localhost:*"])

  OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
  OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

  SYSTEM_PROMPT = """Kamu adalah ZUMA AI Assistant untuk PT ZUMA (brand sandal).

  ATURAN:
  - JAWAB SINGKAT, maksimal 2-3 kalimat
  - Langsung ke poin, tidak basa-basi
  - Jika user kirim [KONTEKS DATA DASHBOARD], gunakan data itu untuk menjawab
  - Jika ditanya stock/sales, jawab berdasarkan data yang dikirim

  KONTEKS ZUMA:
  - Warehouse: WH Pusat, WH Bali, WH Jakarta
  - Area: Bali, Jakarta, Jatim, Batam, Sulawesi, Sumatera, Lombok
  - Metrics: TW = Stock WH / Avg Sales, TO = Stock Toko / Avg Sales"""

  conversations = {}

  def get_ai_response(user_message, session_id="default"):
      if not OPENROUTER_API_KEY:
          return "Error: API Key belum di-set."

      if session_id not in conversations:
          conversations[session_id] = []

      conversations[session_id].append({"role": "user", "content": user_message})

      if len(conversations[session_id]) > 20:
          conversations[session_id] = conversations[session_id][-20:]

      messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversations[session_id]

      try:
          response = requests.post(
              OPENROUTER_BASE_URL,
              headers={
                  "Authorization": "Bearer " + OPENROUTER_API_KEY,
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
              conversations[session_id].append({"role": "assistant", "content": assistant_message})
              return assistant_message
          else:
              return "Error: " + str(response.status_code)
      except Exception as e:
          return "Error: Coba lagi."

  @app.route('/')
  def index():
      return render_template('index.html')

  @app.route('/chat', methods=['POST'])
  def chat():
      data = request.json
      user_message = data.get('message', '')
      session_id = data.get('session_id', 'default')
      if not user_message:
          return jsonify({'error': 'Message required'}), 400
      response = get_ai_response(user_message, session_id)
      return jsonify({'response': response, 'timestamp': datetime.now().isoformat()})

  @app.route('/clear', methods=['POST'])
  def clear_conversation():
      data = request.json
      session_id = data.get('session_id', 'default')
      if session_id in conversations:
          conversations[session_id] = []
      return jsonify({'status': 'cleared'})

  @app.route('/health')
  def health():
      return jsonify({'status': 'healthy', 'api_configured': bool(OPENROUTER_API_KEY)})

  if __name__ == '__main__':
      port = int(os.environ.get('PORT', 5000))
      app.run(host='0.0.0.0', port=port, debug=False)
