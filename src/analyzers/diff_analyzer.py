"""
Diff Analyzer — Understand what changed in the code
"""

import re
from pathlib import Path
from collections import Counter


# File type → domain mapping
FILE_DOMAINS = {
    # Frontend
    ".js": "frontend", ".ts": "frontend", ".jsx": "frontend",
    ".tsx": "frontend", ".vue": "frontend", ".svelte": "frontend",
    ".css": "styles", ".scss": "styles", ".less": "styles",
    ".html": "frontend", ".htm": "frontend",

    # Backend
    ".py": "backend", ".rb": "backend", ".php": "backend",
    ".go": "backend", ".java": "backend", ".cs": "backend",
    ".rs": "backend", ".swift": "backend", ".kt": "backend",

    # Data
    ".sql": "database", ".prisma": "database", ".graphql": "api",

    # Config
    ".json": "config", ".yaml": "config", ".yml": "config",
    ".toml": "config", ".ini": "config", ".env": "config",
    ".dockerfile": "devops", ".tf": "devops",

    # Docs
    ".md": "docs", ".txt": "docs", ".rst": "docs",

    # Tests
    "_test.py": "tests", ".test.js": "tests", ".spec.ts": "tests",
}

# Change patterns → action mapping
CHANGE_PATTERNS = [
    (r"def\s+(\w+)|function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(", "add function"),
    (r"class\s+(\w+)", "add class"),
    (r"import\s+|require\(|from\s+\w+\s+import", "add import"),
    (r"test\s*\(|it\s*\(|describe\s*\(|def\s+test_", "add tests"),
    (r"TODO|FIXME|HACK|NOTE:", "add comment"),
    (r"password|secret|token|api_key|auth", "add auth"),
    (r"SELECT|INSERT|UPDATE|DELETE|CREATE TABLE", "update database"),
    (r"router\.|app\.get|app\.post|@app\.route|endpoint", "add endpoint"),
    (r"migrate|migration|schema", "add migration"),
    (r"fix|bug|error|exception|crash|issue", "fix bug"),
    (r"refactor|cleanup|clean up|reorganize", "refactor"),
    (r"style|format|lint|prettier|eslint", "style"),
    (r"version|changelog|release|bump", "release"),
    (r"README|documentation|docs|docstring", "docs"),
    (r"docker|kubernetes|k8s|helm|compose", "devops"),
    (r"performance|optimize|cache|speed|slow", "perf"),
    (r"security|vulnerability|CVE|sanitize|validate", "security"),
    (r"dependency|package|requirements|npm|pip", "deps"),
]

COMMIT_TYPES = {
    "add function": "feat",
    "add class": "feat",
    "add import": "feat",
    "add tests": "test",
    "add comment": "docs",
    "add auth": "feat",
    "update database": "feat",
    "add endpoint": "feat",
    "add migration": "feat",
    "fix bug": "fix",
    "refactor": "refactor",
    "style": "style",
    "release": "chore",
    "docs": "docs",
    "devops": "ci",
    "perf": "perf",
    "security": "fix",
    "deps": "chore",
}


class DiffAnalyzer:

    def analyze(self, diff: str, files: list) -> dict:
        """Analyze a git diff and return structured information."""

        if not diff and not files:
            return self._empty_analysis()

        analysis = {
            "files": files or [],
            "file_count": len(files) if files else 0,
            "domains": self._detect_domains(files or []),
            "changes": self._detect_changes(diff or ""),
            "stats": self._get_stats(diff or ""),
            "scope": self._detect_scope(files or []),
            "breaking": self._detect_breaking(diff or ""),
            "keywords": self._extract_keywords(diff or ""),
        }

        # Determine primary commit type
        analysis["commit_type"] = self._determine_type(analysis)
        analysis["is_fix"] = analysis["commit_type"] == "fix"
        analysis["is_feat"] = analysis["commit_type"] == "feat"

        return analysis

    def _detect_domains(self, files: list) -> list:
        """Detect which domains are affected."""
        domains = set()
        for f in files:
            path = Path(f)
            # Check for test files
            if "test" in path.name.lower() or "spec" in path.name.lower():
                domains.add("tests")
                continue
            # Check extension
            ext = path.suffix.lower()
            domain = FILE_DOMAINS.get(ext, "code")
            domains.add(domain)
        return list(domains)

    def _detect_changes(self, diff: str) -> list:
        """Detect what kind of changes were made."""
        detected = []
        added_lines = "\n".join(
            line[1:] for line in diff.split("\n") if line.startswith("+")
        )
        for pattern, action in CHANGE_PATTERNS:
            if re.search(pattern, added_lines, re.IGNORECASE):
                if action not in detected:
                    detected.append(action)
        return detected[:5]

    def _get_stats(self, diff: str) -> dict:
        """Get basic diff statistics."""
        lines = diff.split("\n")
        added = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
        removed = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
        return {
            "lines_added": added,
            "lines_removed": removed,
            "net_change": added - removed,
        }

    def _detect_scope(self, files: list) -> str:
        """Detect the scope from file paths."""
        if not files:
            return ""

        # Find common directory
        if len(files) == 1:
            parts = Path(files[0]).parts
            if len(parts) > 1:
                return parts[-2]  # Parent directory
            return Path(files[0]).stem

        # Multiple files — find common parent
        try:
            paths = [Path(f).parts for f in files]
            common = []
            for parts in zip(*paths):
                if len(set(parts)) == 1:
                    common.append(parts[0])
                else:
                    break
            if common and common[-1] not in (".", "src", "lib", "app"):
                return common[-1]
        except Exception:
            pass

        return ""

    def _detect_breaking(self, diff: str) -> bool:
        """Detect if changes might be breaking."""
        breaking_patterns = [
            r"BREAKING CHANGE",
            r"breaking change",
            r"renamed.*function|function.*renamed",
            r"removed.*parameter|parameter.*removed",
            r"changed.*signature|signature.*changed",
        ]
        return any(re.search(p, diff, re.IGNORECASE) for p in breaking_patterns)

    def _extract_keywords(self, diff: str) -> list:
        """Extract meaningful keywords from the diff."""
        added = " ".join(
            line[1:] for line in diff.split("\n")
            if line.startswith("+") and not line.startswith("+++")
        )
        # Extract identifiers
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_]{3,}\b', added)
        # Filter common noise words
        noise = {"self", "true", "false", "null", "none", "return",
                 "const", "function", "import", "from", "class"}
        meaningful = [w for w in words if w.lower() not in noise]
        counts = Counter(meaningful)
        return [w for w, _ in counts.most_common(5)]

    def _determine_type(self, analysis: dict) -> str:
        """Determine the primary commit type."""
        changes = analysis.get("changes", [])
        domains = analysis.get("domains", [])

        if "tests" in domains and changes == ["add tests"]:
            return "test"
        if "docs" in domains and not any(d in domains for d in ["backend", "frontend"]):
            return "docs"

        for change in changes:
            if change in COMMIT_TYPES:
                return COMMIT_TYPES[change]

        stats = analysis.get("stats", {})
        if stats.get("lines_removed", 0) > stats.get("lines_added", 0) * 2:
            return "refactor"

        return "feat"

    def _empty_analysis(self) -> dict:
        return {
            "files": [], "file_count": 0, "domains": [],
            "changes": [], "stats": {}, "scope": "",
            "breaking": False, "keywords": [], "commit_type": "chore",
            "is_fix": False, "is_feat": False,
        }
