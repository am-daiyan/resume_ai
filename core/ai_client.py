import os
import requests
from django.conf import settings
import json

OPENROUTER_URL="https://openrouter.ai/api/v1/chat/completions"
API_KEY = getattr(settings, "OPENROUTER_API_KEY", None)

def call_openrouter(messages, model="google/gemini-2.5-pro-exp-03-25",
                    temperature=0.2, max_tokens=800, timeout=20):
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set in settings")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError("Unexpected OpenRouter response format: " + json.dumps(data)) from e
