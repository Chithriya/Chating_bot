"""
NIELIT Chennai Chatbot Backend
Uses Groq API with llama-3.3-70b model to answer NIELIT-related queries.
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

SYSTEM_PROMPT = """You are the official AI Assistant for NIELIT Chennai (National Institute of Electronics & Information Technology, Chennai).
You help students, candidates, and visitors with questions about NIELIT courses, examinations, admissions, syllabi, fees, and related topics.

Your knowledge covers:

IT LITERACY COURSES:
- BCC (Basic Computer Course): 36 hours, for beginners, online exam 50 marks/50 questions/60 mins, no negative marking, fees approx Rs.500
- CCC (Course on Computer Concepts): 80 hours, intermediate level, 100 questions/90 mins, grades A/B/C/D/F, fees approx Rs.500
- ECC (Expert Course on Computer Concepts): Advanced level

NIELIT ACCREDITED COURSES:
- O Level:
  * Duration: 1 year (2 semesters)
  * Eligibility: 10th pass or ITI certificate
  * Subjects: M1-R5 (IT Tools & Business Systems), M2-R5 (Web Designing & Publishing), M3-R5 (Programming & Problem Solving through Python), M4.1-R5 (Application of .NET Technology), M4.2-R5 (Introduction to ICT Resources), PR-1 (Practical), PJ (Project)
  * Exam: Online CBT, 100 marks per theory paper, 100 marks practical
  * Fees: Approx Rs. 3000-4000
  * Certificate equivalent to foundation level IT course

- A Level:
  * Duration: 1 year (after O Level)
  * Eligibility: O Level certificate or BCA/B.Sc (IT/CS)
  * Subjects: Data Structures, OOP with C++, IT Tools, Web Technologies, Computer Hardware & Networking, Software Engineering, Programming in Java
  * Exam: Theory + Practical + Project
  * Fees: Approx Rs. 6000-8000
  * Certificate equivalent to Diploma in CS

- B Level:
  * Equivalent to MCA level
  * Eligibility: A Level or BCA/B.Sc CS

- C Level:
  * Highest level, equivalent to M.Tech in CS

ESDM COURSES (Electronics System Design & Manufacturing):
- L1-L2 Level: Installation & Maintenance of Photocopiers, Assembly of PCs, EPABX systems (Fees: Rs.5000)
- L3 Level: Electronic Product Testing, Power Supply repair, Medical equipment repair (Fees: Rs.10000)
- L4 Level: Consumer Electronics Diploma, Robotic Programming, Telecom Technician, Solar LED (Fees: Rs.12000)
- L5 Level: Embedded System Design, VLSI Design, Industrial Automation, Hospital Equipment (Fees: Rs.15000)

EXAM PATTERN:
- Theory papers: Part A (40 marks - MCQ/True-False/Match/Fill blanks) + Part B (60 marks - descriptive, attempt 4 out of 5)
- Total time: 3 hours
- Practical exams are separate
- Online CBT for BCC/CCC

ADMISSION PROCESS:
- Apply online at https://student.nielit.gov.in
- Submit documents: photo, signature, eligibility certificate
- Pay fees online
- Exam conducted twice a year (January and July cycles)

CONTACT NIELIT CHENNAI:
- Website: https://nielit.gov.in
- Chennai Email: nielit-che@nielit.gov.in

Guidelines:
1. Be helpful, accurate, and concise.
2. Use bullet points or numbered lists for multiple items.
3. Always direct users to https://nielit.gov.in for official verification.
4. Be warm and encouraging to students.
5. If unsure about something, say so honestly and direct them to the official website.
6. Answer in clear simple English suitable for students at all levels.
7. Keep answers focused and not too long."""


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
            reply_text = "I couldn't find specific information. Please check https://nielit.gov.in or contact nielit-che@nielit.gov.in"

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

    print("🚀 NIELIT Chatbot Server starting at http://127.0.0.1:5000\n")
    app.run(debug=True, host='127.0.0.1', port=5000)