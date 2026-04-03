import json
import os
import urllib.request


def _post_json(url: str, payload: dict, headers: dict[str, str]) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


class CloudLLMClient:
    def __init__(self, provider: str, model: str, api_key: str):
        self.provider = provider.lower().strip()
        self.model = model
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("Missing API key for cloud mode.")

        if self.provider == "groq":
            body = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
            out = _post_json(
                "https://api.groq.com/openai/v1/chat/completions",
                body,
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            return out["choices"][0]["message"]["content"]

        if self.provider == "together":
            body = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
            out = _post_json(
                "https://api.together.xyz/v1/chat/completions",
                body,
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            return out["choices"][0]["message"]["content"]

        if self.provider in {"huggingface", "hf"}:
            url = f"https://router.huggingface.co/v1/chat/completions"
            body = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
            out = _post_json(
                url,
                body,
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            return out["choices"][0]["message"]["content"]

        raise RuntimeError(
            "Unsupported provider. Use one of: groq, together, huggingface."
        )


class MockCloudFallbackClient:
    def generate(self, prompt: str) -> str:
        return (
            "[Fallback cloud response] API provider is unavailable. "
            "Your pipeline still executed retrieval and prompt assembly correctly."
        )
