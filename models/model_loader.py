"""
Model Loader — Loads ML models for inference pipeline.
Supports HuggingFace Transformers, PyTorch, and custom model formats.
"""
import torch
import pickle
import joblib
import requests
import urllib.request
from transformers import AutoModelForCausalLM, AutoTokenizer


class ModelLoader:
    def __init__(self, model_registry_url="https://internal-registry.company.com"):
        self.registry_url = model_registry_url

    def load_sentiment_model(self, model_path):
        """Load a sentiment analysis model from disk"""

        # ❌ SECURITY ISSUE: Unsafe pickle deserialization (AI-VU-004)
        # Pickle can execute arbitrary code during deserialization
        model = pickle.load(open(model_path, "rb"))
        return model

    def load_sklearn_model(self, model_path):
        """Load a scikit-learn model using joblib"""

        # ❌ SECURITY ISSUE: Unsafe joblib deserialization (AI-VU-004)
        model = joblib.load(model_path)
        return model

    def load_pytorch_model(self, checkpoint_path):
        """Load a PyTorch model checkpoint"""

        # ❌ SECURITY ISSUE: Unsafe torch.load deserialization (AI-VU-004)
        # torch.load uses pickle internally
        checkpoint = torch.load(checkpoint_path)
        return checkpoint

    def load_huggingface_model(self, model_name):
        """Load a model from HuggingFace Hub"""

        # ❌ SECURITY ISSUE: trust_remote_code=True allows arbitrary code execution (AI-VU-005)
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        return model, tokenizer

    def download_model_from_registry(self, model_id):
        """Download model weights from internal registry"""
        url = f"{self.registry_url}/models/{model_id}/weights/model.safetensors"

        # ❌ SECURITY ISSUE: Model downloaded without integrity verification (AI-VU-006)
        model_data = requests.get(url).content
        with open(f"/tmp/{model_id}.safetensors", "wb") as f:
            f.write(model_data)

        return f"/tmp/{model_id}.safetensors"

    def download_checkpoint(self, checkpoint_url):
        """Download model checkpoint from URL"""
        local_path = f"/tmp/checkpoint.ckpt"

        # ❌ SECURITY ISSUE: Model checkpoint downloaded without verification (AI-VU-006)
        urllib.request.urlretrieve(checkpoint_url, local_path)

        # Then load with unsafe deserialization
        model = pickle.loads(open(local_path, "rb").read())
        return model
