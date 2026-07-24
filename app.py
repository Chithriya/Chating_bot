"""
Uses Groq API with llama-3.3-70b model to answer organization-related queries.
Sign up free at: https://console.groq.com
"""

import os
from groq import Groq
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

SYSTEM_PROMPT = "The rules you can set"
"set of instructions"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'reply': 'Invalid request.'})

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'reply': 'Please send a message.'})

        print(f"User: {user_message}")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        reply_text = response.choices[0].message.content

        if not reply_text.strip():
            reply_text = "I couldn't find specific information. Please check https://organization.gov.in or contact organization-che@organization.gov.in"

        print(f"Bot replied OK")
        return jsonify({'reply': reply_text.strip()})

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return jsonify({'reply': f'Error: {str(e)}'}), 500


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n⚠️  WARNING: GROQ_API_KEY not set!")
        print("   Get free key at: https://console.groq.com")
        print("   In PowerShell: $env:GROQ_API_KEY='your-key-here'\n")
    else:
        print(f"\n✅ Groq API Key found: {api_key[:12]}...\n")

    print("🚀 organization Chatbot Server starting at http://127.0.0.1:5000\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
