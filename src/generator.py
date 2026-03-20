"""
⚡ Core Commit Message Generator
Supports: Rule-based (no API key), OpenAI, Ollama
"""

import re
from src.analyzers.diff_analyzer import DiffAnalyzer
from src.generators.conventional import ConventionalGenerator
from src.generators.emoji_style import EmojiGenerator
from src.generators.ai_generator import AIGenerator


class CommitGenerator:

    def __init__(self, provider: str = "rule-based"):
        self.provider = provider
        self.analyzer = DiffAnalyzer()

    def generate(self, diff: str, files: list,
                 style: str = "conventional",
                 count: int = 3,
                 lang: str = "en") -> list:
        """Generate commit message suggestions."""

        # Analyze the diff
        analysis = self.analyzer.analyze(diff, files)

        if self.provider == "openai":
            gen = AIGenerator(provider="openai")
            return gen.generate(analysis, style, count, lang)
        elif self.provider == "ollama":
            gen = AIGenerator(provider="ollama")
            return gen.generate(analysis, style, count, lang)
        else:
            # Rule-based — works without any API key
            return self._rule_based(analysis, style, count)

    def _rule_based(self, analysis: dict, style: str, count: int) -> list:
        """Generate messages using rule-based analysis."""
        if style == "emoji":
            gen = EmojiGenerator()
        else:
            gen = ConventionalGenerator()

        return gen.generate(analysis, count)
