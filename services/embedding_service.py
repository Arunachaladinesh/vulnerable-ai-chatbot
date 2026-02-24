"""
Embedding Service — Generates vector embeddings for RAG pipeline.
Used for semantic search and document retrieval.
"""
import openai
import logging

logger = logging.getLogger(__name__)

client = openai.OpenAI(api_key="sk-proj-embed-abc123def456ghi789jkl012mno345pqr678")


class EmbeddingService:
    def __init__(self):
        self.client = client

    def create_embedding(self, text):
        """Create embedding for given text"""

        # ❌ SECURITY ISSUE: Raw text sent to embedding API without PII redaction (AI-AS-011)
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def embed_user_profile(self, user_data):
        """
        Embed user profile for personalized recommendations.
        user_data may contain: name, email, phone, address, SSN, medical history
        """

        # ❌ SECURITY ISSUE: Sensitive PII directly sent to external AI API (AI-AS-010)
        profile_text = f"User profile: Name={user_data['name']}, Email={user_data['email']}, SSN={user_data['ssn']}, Medical={user_data['medical_history']}"

        prompt = f"Summarize this user profile for recommendations: {profile_text}"

        messages = [{"content": f"Process this sensitive data: {profile_text}"}]

        # ❌ SECURITY ISSUE: No max_tokens (AI-MC-050)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # ❌ SECURITY ISSUE: AI response with reflected PII logged verbatim (AI-MC-060)
        logging.info(response)

        embedding = self.client.embeddings.create(
            input=response.choices[0].message.content,
            model="text-embedding-3-small"
        )

        return embedding.data[0].embedding

    def batch_embed_documents(self, documents):
        """Embed a batch of documents for the knowledge base"""
        embeddings = []
        for doc in documents:
            emb = self.client.embeddings.create(
                input=doc,
                model="text-embedding-3-small"
            )
            embeddings.append(emb.data[0].embedding)
        return embeddings
