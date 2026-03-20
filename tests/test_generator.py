"""
Tests for git-commit-gen
"""

import pytest
from src.analyzers.diff_analyzer import DiffAnalyzer
from src.generators.conventional import ConventionalGenerator
from src.generators.emoji_style import EmojiGenerator
from src.generator import CommitGenerator


SAMPLE_DIFF = """
diff --git a/src/auth.py b/src/auth.py
+++ b/src/auth.py
@@ -0,0 +1,20 @@
+def authenticate_user(email, password):
+    user = User.query.filter_by(email=email).first()
+    if user and user.check_password(password):
+        return generate_jwt_token(user)
+    return None
"""

SAMPLE_FIX_DIFF = """
diff --git a/src/parser.py b/src/parser.py
+++ b/src/parser.py
@@ -10,6 +10,8 @@
-    return data
+    if data is None:
+        raise ValueError("Data cannot be None")
+    return data
"""


# ── Analyzer Tests ────────────────────────────────────────────

def test_analyzer_detects_feat():
    analyzer = DiffAnalyzer()
    result = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    assert result["commit_type"] in ["feat", "fix"]
    assert len(result["files"]) == 1


def test_analyzer_detects_scope():
    analyzer = DiffAnalyzer()
    result = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    assert result["scope"] == "src"


def test_analyzer_stats():
    analyzer = DiffAnalyzer()
    result = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    assert result["stats"]["lines_added"] > 0


def test_analyzer_empty():
    analyzer = DiffAnalyzer()
    result = analyzer.analyze("", [])
    assert result["commit_type"] == "chore"
    assert result["files"] == []


def test_analyzer_detects_breaking():
    diff = "BREAKING CHANGE: removed login endpoint"
    analyzer = DiffAnalyzer()
    result = analyzer.analyze(diff, [])
    assert result["breaking"] is True


def test_analyzer_detects_tests():
    diff = "def test_user_login():\n    assert response.status_code == 200"
    analyzer = DiffAnalyzer()
    result = analyzer.analyze(diff, ["tests/test_auth.py"])
    assert result["commit_type"] in ["test", "feat"]


# ── Generator Tests ───────────────────────────────────────────

def test_conventional_generates():
    analyzer = DiffAnalyzer()
    analysis = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    gen = ConventionalGenerator()
    suggestions = gen.generate(analysis, count=3)
    assert len(suggestions) == 3
    assert all("message" in s for s in suggestions)


def test_conventional_format():
    analyzer = DiffAnalyzer()
    analysis = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    gen = ConventionalGenerator()
    suggestions = gen.generate(analysis, count=1)
    msg = suggestions[0]["message"]
    # Should follow conventional format: type(scope): description
    assert ":" in msg


def test_emoji_generates():
    analyzer = DiffAnalyzer()
    analysis = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    gen = EmojiGenerator()
    suggestions = gen.generate(analysis, count=3)
    assert len(suggestions) >= 1


def test_main_generator_rule_based():
    gen = CommitGenerator(provider="rule-based")
    suggestions = gen.generate(
        diff=SAMPLE_DIFF,
        files=["src/auth.py"],
        style="conventional",
        count=3
    )
    assert len(suggestions) >= 1
    assert all("message" in s for s in suggestions)


def test_main_generator_emoji_style():
    gen = CommitGenerator(provider="rule-based")
    suggestions = gen.generate(
        diff=SAMPLE_DIFF,
        files=["src/auth.py"],
        style="emoji",
        count=3
    )
    assert len(suggestions) >= 1


def test_confidence_range():
    analyzer = DiffAnalyzer()
    analysis = analyzer.analyze(SAMPLE_DIFF, ["src/auth.py"])
    gen = ConventionalGenerator()
    suggestions = gen.generate(analysis, count=3)
    for s in suggestions:
        assert 0 <= s["confidence"] <= 1


def test_fix_type_detection():
    analyzer = DiffAnalyzer()
    result = analyzer.analyze(SAMPLE_FIX_DIFF, ["src/parser.py"])
    assert result["commit_type"] in ["fix", "feat", "refactor"]
