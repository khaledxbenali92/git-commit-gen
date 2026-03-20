"""
AI-powered Generator — OpenAI & Ollama support
"""

import os
import json


AI_PROMPT = """You are an expert at writing Git commit messages following Conventional Commits specification.

Analyze this git diff and generate {count} commit message suggestions.

Rules:
- Format: type(scope): description
- Types: feat, fix, docs, style, refactor, test, chore, ci, perf
- Description: imperative mood, lowercase, no period, max 72 chars
- Be specific about what changed
- If breaking change, add ! before colon: feat!: description

Respond ONLY with a JSON array like:
[
  {{"message": "feat(auth): add JWT token refresh mechanism", "confidence": 0.95}},
  {{"message": "feat(auth): implement token expiry handling", "confidence": 0.85}}
]

Style: {style}
Language: {lang}

Git diff:
{diff}

Changed files: {files}
"""


class AIGenerator:

    def __init__(self, provider: str = "openai"):
        self.provider = provider

    def generate(self, analysis: dict, style: str,
                 count: int, lang: str) -> list:
        if self.provider == "openai":
            return self._openai(analysis, style, count, lang)
        elif self.provider == "ollama":
            return self._ollama(analysis, style, count, lang)
        return []

    def _openai(self, analysis: dict, style: str,
                count: int, lang: str) -> list:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt = AI_PROMPT.format(
                count=count, style=style, lang=lang,
                diff=analysis.get("diff_preview", "")[:3000],
                files=", ".join(analysis.get("files", []))
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7, max_tokens=500
            )

            content = response.choices[0].message.content
            data = json.loads(content)
            return [{"message": d["message"],
                     "type": "ai",
                     "confidence": d.get("confidence", 0.8),
                     "breaking": False}
                    for d in data]

        except Exception as e:
            print(f"OpenAI error: {e}")
            return []

    def _ollama(self, analysis: dict, style: str,
                count: int, lang: str) -> list:
        try:
            import requests
            prompt = AI_PROMPT.format(
                count=count, style=style, lang=lang,
                diff=analysis.get("diff_preview", "")[:3000],
                files=", ".join(analysis.get("files", []))
            )
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False},
                timeout=30
            )
            content = response.json().get("response", "")
            start = content.find("[")
            end = content.rfind("]") + 1
            if start >= 0 and end > start:
                data = json.loads(content[start:end])
                return [{"message": d["message"],
                         "type": "ai",
                         "confidence": d.get("confidence", 0.8),
                         "breaking": False}
                        for d in data]
        except Exception as e:
            print(f"Ollama error: {e}")
        return []
