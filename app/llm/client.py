import os
from langchain_ollama import ChatOllama

def get_default_llm():
    """
    Returns the default LLM client configured via environment variables.
    """
    model = os.getenv("OLLAMA_MODEL", "llama3")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return ChatOllama(
        model=model,
        base_url=base_url,
        temperature=0.1 # Low temperature for deterministic output
    )
