"""
Conventional Commits Generator
Generates messages following https://www.conventionalcommits.org
"""

from src.analyzers.diff_analyzer import COMMIT_TYPES


TEMPLATES = {
    "feat": [
        "feat{scope}: add {keyword} functionality",
        "feat{scope}: implement {keyword} feature",
        "feat{scope}: introduce {keyword} support",
        "feat{scope}: add {keyword} to {domain}",
        "feat{scope}: create {keyword} module",
    ],
    "fix": [
        "fix{scope}: resolve {keyword} issue",
        "fix{scope}: fix {keyword} bug",
        "fix{scope}: correct {keyword} behavior",
        "fix{scope}: handle {keyword} edge case",
        "fix{scope}: repair broken {keyword}",
    ],
    "refactor": [
        "refactor{scope}: simplify {keyword} logic",
        "refactor{scope}: restructure {keyword} module",
        "refactor{scope}: clean up {keyword} code",
        "refactor{scope}: extract {keyword} helper",
        "refactor{scope}: reorganize {keyword} structure",
    ],
    "docs": [
        "docs{scope}: update {keyword} documentation",
        "docs{scope}: add {keyword} examples",
        "docs{scope}: improve {keyword} README",
        "docs{scope}: document {keyword} API",
        "docs{scope}: fix {keyword} typos",
    ],
    "test": [
        "test{scope}: add {keyword} unit tests",
        "test{scope}: improve {keyword} test coverage",
        "test{scope}: add integration tests for {keyword}",
        "test{scope}: fix failing {keyword} tests",
        "test{scope}: add {keyword} edge case tests",
    ],
    "style": [
        "style{scope}: format {keyword} code",
        "style{scope}: fix linting issues in {keyword}",
        "style{scope}: apply prettier to {keyword}",
        "style: enforce consistent code style",
        "style{scope}: fix whitespace and formatting",
    ],
    "chore": [
        "chore{scope}: update {keyword} dependencies",
        "chore{scope}: bump {keyword} version",
        "chore{scope}: update {keyword} config",
        "chore{scope}: clean up {keyword}",
        "chore: maintenance and housekeeping",
    ],
    "ci": [
        "ci{scope}: update {keyword} workflow",
        "ci{scope}: add {keyword} pipeline step",
        "ci{scope}: fix {keyword} CI configuration",
        "ci: improve build process",
        "ci{scope}: add {keyword} automation",
    ],
    "perf": [
        "perf{scope}: optimize {keyword} performance",
        "perf{scope}: improve {keyword} speed",
        "perf{scope}: cache {keyword} results",
        "perf{scope}: reduce {keyword} memory usage",
        "perf{scope}: lazy load {keyword}",
    ],
}

DOMAIN_KEYWORDS = {
    "frontend": ["UI", "component", "view", "page", "layout"],
    "backend": ["API", "service", "handler", "controller", "middleware"],
    "database": ["query", "schema", "migration", "model", "index"],
    "tests": ["coverage", "assertion", "mock", "fixture", "suite"],
    "styles": ["theme", "layout", "responsive", "animation", "variable"],
    "config": ["settings", "environment", "options", "configuration"],
    "devops": ["deployment", "container", "pipeline", "workflow"],
    "docs": ["documentation", "guide", "example", "reference"],
}


class ConventionalGenerator:

    def generate(self, analysis: dict, count: int = 3) -> list:
        """Generate conventional commit messages."""
        commit_type = analysis.get("commit_type", "feat")
        scope = self._format_scope(analysis.get("scope", ""))
        keywords = analysis.get("keywords", [])
        domains = analysis.get("domains", [])
        breaking = analysis.get("breaking", False)

        # Get primary keyword
        primary_kw = keywords[0] if keywords else self._domain_keyword(domains)
        secondary_kw = keywords[1] if len(keywords) > 1 else primary_kw
        domain_name = domains[0] if domains else "code"

        templates = TEMPLATES.get(commit_type, TEMPLATES["feat"])
        suggestions = []

        for i, template in enumerate(templates[:count]):
            msg = template.format(
                scope=scope,
                keyword=primary_kw if i % 2 == 0 else secondary_kw,
                domain=domain_name,
            )

            # Add breaking change indicator
            if breaking and i == 0:
                msg = msg.replace(":", "!:", 1)

            suggestions.append({
                "message": msg,
                "type": commit_type,
                "breaking": breaking and i == 0,
                "confidence": max(0.95 - (i * 0.1), 0.5),
            })

        # Add a generic fallback
        if len(suggestions) < count:
            stats = analysis.get("stats", {})
            added = stats.get("lines_added", 0)
            removed = stats.get("lines_removed", 0)
            files = analysis.get("file_count", 0)
            suggestions.append({
                "message": f"{commit_type}{scope}: update {domain_name} ({files} files, +{added}/-{removed} lines)",
                "type": commit_type,
                "breaking": False,
                "confidence": 0.4,
            })

        return suggestions[:count]

    def _format_scope(self, scope: str) -> str:
        if not scope or scope in (".", "src", "lib"):
            return ""
        # Clean scope
        scope = scope.replace("-", "_").lower()
        if len(scope) > 20:
            scope = scope[:20]
        return f"({scope})"

    def _domain_keyword(self, domains: list) -> str:
        for domain in domains:
            keywords = DOMAIN_KEYWORDS.get(domain, [])
            if keywords:
                return keywords[0].lower()
        return "changes"
