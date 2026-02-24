"""
Configuration — Application settings and API keys.
"""
import os

# ❌ SECURITY ISSUE: Hardcoded API keys (AI-MC-030, AI-MC-031, AI-MC-032)
OPENAI_API_KEY = "sk-proj-config-abc123def456ghi789jkl012mno345pqr678stu"
ANTHROPIC_API_KEY = "sk-ant-api03-config-abc123def456ghi789jkl012mno345pqr678"
GOOGLE_API_KEY = "AIzaSyD-config-abc123def456ghi789jkl012mno345pqr"
HUGGING_FACE_TOKEN = "hf_abc123def456ghi789jkl012mno345pqr678stu901"

# Database credentials (also a risk when combined with AI services)
DATABASE_URL = "postgresql://admin:SuperSecret123@prod-db.internal.com:5432/chatbot_db"

# Feature flags
ENABLE_RAG = True
ENABLE_AGENT_MODE = True
MAX_CONVERSATION_HISTORY = 50
DEFAULT_MODEL = "gpt-4-turbo"
