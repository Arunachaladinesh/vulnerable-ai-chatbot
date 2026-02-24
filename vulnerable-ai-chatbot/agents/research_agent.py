"""
Research Agent — LangChain-powered autonomous agent for research tasks.
Uses tools and RAG for information retrieval.
"""
from langchain import LLMChain
from langchain_openai import ChatOpenAI
from langchain_community import document_loaders
from langchain_core import prompts
import os

# ❌ SECURITY ISSUE: API key hardcoded (AI-MC-032)
os.environ["OPENAI_API_KEY"] = "sk-proj-research-abc123def456ghi789jkl012mno345pqr"
GOOGLE_API_KEY = "AIzaSyD-abc123def456ghi789jkl012mno345pqr"


class ResearchAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.3
        )

    def research_topic(self, user_query, uploaded_documents=None):
        """
        Research a topic using AI with user-uploaded documents.
        """

        # ❌ SECURITY ISSUE: User input directly in prompt (AI-AS-003)
        research_prompt = f"Research the following topic thoroughly. Use any tools available. Query: {user_query}"

        if uploaded_documents:
            doc_content = "\n".join([doc.page_content for doc in uploaded_documents])
            # User-uploaded document content injected without sanitization
            research_prompt = f"Based on these documents:\n{doc_content}\n\nAnswer: {user_query}"

        response = self.llm.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": research_prompt}
            ]
        )

        return response.choices[0].message.content

    def analyze_competitive_intel(self, company_name, internal_data):
        """Analyze competitive intelligence — may expose proprietary data"""

        # ❌ SECURITY ISSUE: Sensitive business data sent to external AI (AI-AS-010)
        prompt = f"Analyze competitive positioning for {company_name}. Internal data: Revenue={internal_data['revenue']}, Customers={internal_data['customer_count']}, Strategy={internal_data['strategy']}"

        messages = [{"content": f"Confidential analysis: {prompt}"}]

        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
