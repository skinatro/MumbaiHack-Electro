from app.llm.client import get_default_llm

def llm_healthcheck() -> dict:
    """
    Run a tiny LLM call to verify that LangChain + Ollama infra works.
    Returns a dict with fields:
      - ok: bool
      - model: str
      - error: str | None
      - sample_reply: str | None (short)
    """
    llm = get_default_llm()
    try:
        # Keep prompt extremely short and deterministic
        prompt = "Respond ONLY with the word: OK"
        res = llm.invoke(prompt)
        text = str(res.content).strip() if hasattr(res, "content") else str(res).strip()

        ok = (text.upper() == "OK")
        return {
            "ok": ok,
            "model": getattr(llm, "model", "unknown"),
            "error": None if ok else f"Unexpected reply: {text}",
            "sample_reply": text,
        }
    except Exception as e:
        return {
            "ok": False,
            "model": getattr(llm, "model", "unknown"),
            "error": str(e),
            "sample_reply": None,
        }
