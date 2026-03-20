"""
Emoji Commit Generator — Gitmoji style
https://gitmoji.dev
"""

EMOJI_MAP = {
    "feat":     ("✨", "Introduce new features"),
    "fix":      ("🐛", "Fix a bug"),
    "docs":     ("📝", "Add or update documentation"),
    "style":    ("💄", "Add or update UI and style files"),
    "refactor": ("♻️",  "Refactor code"),
    "perf":     ("⚡️", "Improve performance"),
    "test":     ("✅", "Add, update or pass tests"),
    "chore":    ("🔧", "Add or update configuration files"),
    "ci":       ("👷", "Add or update CI build system"),
    "revert":   ("⏪️", "Revert changes"),
    "security": ("🔒️", "Fix security issues"),
    "deps":     ("⬆️",  "Upgrade dependencies"),
    "breaking": ("💥", "Introduce breaking changes"),
    "init":     ("🎉", "Begin a project"),
    "deploy":   ("🚀", "Deploy stuff"),
    "remove":   ("🔥", "Remove code or files"),
    "hotfix":   ("🚑️", "Critical hotfix"),
}

EMOJI_TEMPLATES = {
    "feat":     [
        "{emoji} add {keyword} feature",
        "{emoji} implement {keyword}",
        "{emoji} introduce {keyword} support",
    ],
    "fix":      [
        "{emoji} fix {keyword} bug",
        "{emoji} resolve {keyword} issue",
        "{emoji} patch {keyword} error",
    ],
    "refactor": [
        "{emoji} refactor {keyword}",
        "{emoji} clean up {keyword}",
        "{emoji} simplify {keyword} logic",
    ],
    "docs":     [
        "{emoji} update {keyword} docs",
        "{emoji} add {keyword} documentation",
        "{emoji} improve README",
    ],
    "test":     [
        "{emoji} add {keyword} tests",
        "{emoji} improve test coverage",
        "{emoji} add {keyword} unit tests",
    ],
    "chore":    [
        "{emoji} update {keyword} config",
        "{emoji} maintenance and cleanup",
        "{emoji} bump {keyword} version",
    ],
    "ci":       [
        "{emoji} update CI workflow",
        "{emoji} fix {keyword} pipeline",
        "{emoji} add {keyword} automation",
    ],
    "perf":     [
        "{emoji} optimize {keyword}",
        "{emoji} improve {keyword} performance",
        "{emoji} speed up {keyword}",
    ],
}


class EmojiGenerator:

    def generate(self, analysis: dict, count: int = 3) -> list:
        commit_type = analysis.get("commit_type", "feat")
        keywords = analysis.get("keywords", ["code"])
        breaking = analysis.get("breaking", False)

        emoji_key = "breaking" if breaking else commit_type
        emoji, _ = EMOJI_MAP.get(emoji_key, EMOJI_MAP["feat"])
        primary_kw = keywords[0] if keywords else "code"

        templates = EMOJI_TEMPLATES.get(commit_type, EMOJI_TEMPLATES["feat"])
        suggestions = []

        for i, template in enumerate(templates[:count]):
            msg = template.format(emoji=emoji, keyword=primary_kw)
            suggestions.append({
                "message": msg,
                "type": commit_type,
                "breaking": breaking,
                "confidence": max(0.9 - (i * 0.1), 0.5),
            })

        return suggestions[:count]
