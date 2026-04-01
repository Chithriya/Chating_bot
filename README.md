# NIELIT Chennai Chatbot (FREE - Powered by Groq)

100% FREE chatbot using Groq API. No credit card needed.

---

## How It Works

1. User types a question in the chatbot
2. Frontend sends it to Flask backend (`/chat` endpoint)
3. Backend calls Groq AI using the **LLaMA 3.3 70B** model
4. Groq AI processes the question using the built-in NIELIT knowledge
5. Groq returns a clear, accurate answer in under 2 seconds
6. Answer is displayed in the chat window

---

## Setup Steps

### Step 1 - Get FREE Groq API Key
1. Go to https://console.groq.com
2. Sign up with Google (free)
3. Click "API Keys" → "Create API Key"
4. Copy the key (starts with gsk_...)

### Step 2 - Install dependencies
Open PowerShell in the nielit_chatbot folder and run:
```
pip install groq flask flask-cors
```

### Step 3 - Set API key (PowerShell)
```
$env:GROQ_API_KEY="gsk_your-key-here"
```

### Step 4 - Start server
```
python app.py
```
Or if that doesn't work:
```
C:\Users\hp\AppData\Local\Programs\Python\Python312\python.exe app.py
```

### Step 5 - Open browser
Go to: http://127.0.0.1:5000

---

## Files
- index.html  → Chatbot UI
- style.css   → Styling
- script.js   → Frontend logic
- app.py      → Backend (Groq AI)
- requirements.txt → Dependencies

---

## Free Limits (Groq)
- 14,400 requests per day
- Completely free, no credit card
- Very fast responses (faster than paid APIs)

---

## Contact NIELIT Chennai
- Website: https://nielit.gov.in
- Email: nielit-che@nielit.gov.in

I'll break down this code section by section with clean, clear explanations.

---

## 📁 File Overview
This is a **Flask web server** that powers a chatbot for NIELIT Chennai, using the **Groq AI API** to generate responses.

---

## 1️⃣ Imports

```python
import os
from groq import Groq
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
```

| Import | Purpose |
|--------|---------|
| `os` | Built-in Python module to read environment variables (like API keys) |
| `Groq` | Groq's official Python library to talk to their AI models |
| `Flask` | Web framework to create the server and handle routes |
| `request` | Reads incoming HTTP request data (what the user sends) |
| `jsonify` | Converts Python dictionaries into JSON responses |
| `send_from_directory` | Serves static files like HTML from a folder |
| `CORS` | Allows the frontend (browser) to call this backend from a different port/domain |

---

## 2️⃣ App Setup

```python
app = Flask(__name__, static_folder='.')
CORS(app)
```

- `Flask(__name__)` — Creates the Flask app. `__name__` tells Flask the current file's location.
- `static_folder='.'` — Sets the current directory (`.`) as the folder for serving static files.
- `CORS(app)` — Enables **Cross-Origin Resource Sharing**, so a browser on `localhost:3000` can call `localhost:5000` without being blocked.

---

## 3️⃣ Groq Client Initialization

```python
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
```

- `os.environ.get("GROQ_API_KEY")` — Reads the API key from your system's **environment variables** (safer than hardcoding keys in code).
- `Groq(api_key=...)` — Creates a Groq client object that will be used to send prompts to the AI model.

---

## 4️⃣ System Prompt

```python
SYSTEM_PROMPT = """You are the official AI Assistant for NIELIT Chennai..."""
```

- This is a **multi-line string** (text block) that acts as the AI's instruction manual.
- It tells the AI **who it is**, **what it knows**, and **how to behave**.
- This is sent with every chat request so the AI always stays in the NIELIT context.
- Think of it as the AI's "job description" given before every conversation.

---

## 5️⃣ The `/chat` Route (Main Logic)

```python
@app.route('/chat', methods=['POST'])
def chat():
```

- `@app.route('/chat', methods=['POST'])` — A **decorator** that tells Flask: *"When someone sends a POST request to `/chat`, run this function."*
- POST is used because the user is **sending data** (their message) to the server.

---

### 🔹 Step 1 — Parse the incoming request

```python
data = request.get_json()
if not data:
    return jsonify({'reply': 'Invalid request.'})
```

- `request.get_json()` — Reads the JSON body from the HTTP request (e.g., `{"message": "What is CCC?"}`).
- If no data is received (empty or malformed request), it immediately returns an error response.

---

### 🔹 Step 2 — Extract the user message

```python
user_message = data.get('message', '').strip()
if not user_message:
    return jsonify({'reply': 'Please send a message.'})
```

- `data.get('message', '')` — Extracts the `"message"` field. If not found, defaults to an empty string `''`.
- `.strip()` — Removes leading/trailing spaces.
- If the message is empty after stripping, it returns a polite prompt to the user.

---

### 🔹 Step 3 — Call the Groq AI API

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    max_tokens=1024,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
)
```

| Parameter | Meaning |
|-----------|---------|
| `model` | Which AI model to use — here it's **LLaMA 3.3 70B** (a large, powerful model) |
| `max_tokens` | Limits the AI's reply to **1024 tokens** (~750 words) to control cost and speed |
| `messages` | A list of messages sent to the AI — first the system instructions, then the user's question |

The `role` field tells the AI who is speaking:
- `"system"` → Background instructions (NIELIT context)
- `"user"` → The student's actual question

---

### 🔹 Step 4 — Extract and return the reply

```python
reply_text = response.choices[0].message.content

if not reply_text.strip():
    reply_text = "I couldn't find specific information. Please check https://nielit.gov.in..., else contact Nielit Office"

return jsonify({'reply': reply_text.strip()})
```

- `response.choices[0].message.content` — The AI can return multiple response choices; `[0]` picks the first (and usually only) one, then `.content` gets the actual text.
- If the reply is somehow empty, a **fallback message** is used instead.
- `jsonify({'reply': ...})` — Wraps the reply in JSON format and sends it back to the frontend.

---

### 🔹 Step 5 — Error Handling

```python
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    return jsonify({'reply': f'Error: {str(e)}'}), 500
```

- Catches **any error** (network failure, invalid API key, etc.).
- Prints the error to the terminal for debugging.
- Returns a `500` HTTP status code (Internal Server Error) along with the error message.

---

## 6️⃣ Static File Routes

```python
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)
```

- The first route serves `index.html` when someone visits `http://localhost:5000/` — this is the chatbot's frontend webpage.
- The second route handles **any other file request** (e.g., CSS, JS, images) from the same directory.
- `<path:filename>` is a **dynamic URL parameter** that captures whatever filename is in the URL.

---

## 7️⃣ App Entry Point

```python
if __name__ == '__main__':
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n⚠️  WARNING: GROQ_API_KEY not set!")
    else:
        print(f"\n✅ Groq API Key found: {api_key[:12]}...\n")

    app.run(debug=True, host='127.0.0.1', port=5000)
```

- `if __name__ == '__main__'` — This block only runs when you **directly execute** this file (`python app.py`), not when it's imported as a module.
- Checks if the API key exists and prints a warning or confirmation.
- `api_key[:12]` — Shows only the first 12 characters of the key for security (never print the full key).
- `app.run(debug=True, host='127.0.0.1', port=5000)` — Starts the server:
  - `debug=True` → Auto-restarts on code changes, shows detailed errors
  - `host='127.0.0.1'` → Only accessible on your **local machine** (localhost)
  - `port=5000` → Listens on port 5000

---

## 🔄 Full Request Flow Summary

```
Browser (user types question)
       ↓  POST /chat  {"message": "What is CCC?"}
Flask server receives request
       ↓
Extracts message → Sends to Groq API (LLaMA model)
       ↓
AI generates answer using SYSTEM_PROMPT context
       ↓
Flask returns {"reply": "CCC is a course..."} 
       ↓
Browser displays the answer
```
