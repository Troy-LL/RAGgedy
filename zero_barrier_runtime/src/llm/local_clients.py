import json
import urllib.request


class OllamaClient:
    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2},
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url=f"{self.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            out = json.loads(resp.read().decode("utf-8"))
        return out.get("response", "")


class MockLocalFallbackClient:
    def generate(self, prompt: str) -> str:
        return (
            "[Fallback local response] Could not reach local runtime. "
            "Check if Ollama is running and model is pulled."
        )
