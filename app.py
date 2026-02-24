"""
Viper AI Chatbot — Main Application Entry Point
A customer support chatbot powered by OpenAI GPT-4 and LangChain.
"""
import openai
from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# ❌ SECURITY ISSUE: Hardcoded API Key (AI-MC-030, AI-MC-032)
OPENAI_API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    user_context = request.json.get("context", "")

    # ❌ SECURITY ISSUE: User input directly in prompt without sanitization (AI-AS-003)
    prompt = f"You are a helpful assistant. Context: {user_context}. User asks: {user_message}"

    # ❌ SECURITY ISSUE: No max_tokens limit — cost attack risk (AI-MC-050)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a customer support agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    # ❌ SECURITY ISSUE: Logging full AI response without sanitization (AI-MC-060)
    logging.info(response)

    return jsonify({
        "reply": response.choices[0].message.content,
        "tokens_used": response.usage.total_tokens
    })


@app.route("/admin/set-system-prompt", methods=["POST"])
def set_system_prompt():
    admin_input = request.json.get("system_prompt", "")

    # ❌ SECURITY ISSUE: User-controlled content in system prompt (AI-AS-004)
    messages = [
        {"role": "system", "content": f"You must follow these rules: {admin_input}"},
        {"role": "user", "content": "Hello"}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    return jsonify({"reply": response.choices[0].message.content})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
