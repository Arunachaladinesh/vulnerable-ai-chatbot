"""
Chat Service — Handles AI conversations with multiple providers.
Supports OpenAI and Anthropic backends.
"""
import openai
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)

# ❌ SECURITY ISSUE: Hardcoded Anthropic API key (AI-MC-031)
ANTHROPIC_API_KEY = "sk-ant-api03-abc123def456ghi789jkl012mno345pqr678stu901vwxyz"
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)


class ChatService:
    def __init__(self):
        # ❌ SECURITY ISSUE: Hardcoded OpenAI key (AI-MC-030)
        self.openai_client = openai.OpenAI(
            api_key="sk-svcacct-abc123def456ghi789jkl012mno345pqr678stu901vwx"
        )

    def generate_response_openai(self, user_input, system_context=""):
        """Generate response using OpenAI GPT-4"""

        # ❌ SECURITY ISSUE: Unsanitized user input interpolated into prompt (AI-AS-003)
        prompt = f"Answer based on this context: {system_context}\n\nQuestion: {user_input}"

        # ❌ SECURITY ISSUE: No max_tokens set (AI-MC-050)
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        # ❌ SECURITY ISSUE: Full response logged without filtering PII (AI-MC-060)
        logging.info(response)

        return response.choices[0].message.content

    def generate_response_anthropic(self, user_input):
        """Generate response using Anthropic Claude"""
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return message.content[0].text

    def generate_dynamic_system_prompt(self, user_role, user_permissions):
        """Dynamically build system prompt based on user role"""

        # ❌ SECURITY ISSUE: User-controlled data in system prompt (AI-AS-004)
        system_msg = {"role": "system", "content": f"User has role: {user_role} with permissions: {user_permissions}. Act accordingly."}

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[system_msg, {"role": "user", "content": "What can I access?"}]
        )

        return response.choices[0].message.content
