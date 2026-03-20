"""
Display Utilities — Colorful terminal output
"""

BOLD  = "\033[1m"
RESET = "\033[0m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED   = "\033[91m"
DIM   = "\033[2m"

TYPE_COLORS = {
    "feat":     "\033[94m",   # Blue
    "fix":      "\033[91m",   # Red
    "docs":     "\033[93m",   # Yellow
    "style":    "\033[95m",   # Magenta
    "refactor": "\033[96m",   # Cyan
    "test":     "\033[92m",   # Green
    "chore":    "\033[90m",   # Gray
    "ci":       "\033[94m",   # Blue
    "perf":     "\033[95m",   # Magenta
}


def print_banner():
    print(f"""{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════╗
║        ⚡ Git Commit Message Generator v1.0              ║
║     Generate perfect commits from your staged diff       ║
║           github.com/khaledxbenali92                     ║
╚══════════════════════════════════════════════════════════╝
{RESET}""")


def display_suggestions(suggestions: list):
    """Display commit suggestions with colors."""
    print(f"\n{BOLD}💡 Generated commit messages:{RESET}\n")

    for i, s in enumerate(suggestions, 1):
        msg = s["message"]
        commit_type = s.get("type", "feat")
        confidence = s.get("confidence", 0.8)
        breaking = s.get("breaking", False)

        # Color by type
        color = TYPE_COLORS.get(commit_type, CYAN)

        # Confidence bar
        bar_filled = int(confidence * 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        conf_pct = int(confidence * 100)

        breaking_tag = f" {RED}[BREAKING CHANGE]{RESET}" if breaking else ""

        print(f"  {BOLD}[{i}]{RESET} {color}{msg}{RESET}{breaking_tag}")
        print(f"       {DIM}Confidence: {bar} {conf_pct}%{RESET}")
        print()


def print_error(message: str):
    print(f"\n{RED}❌ {message}{RESET}\n")


def print_success(message: str):
    print(f"\n{GREEN}✅ {message}{RESET}\n")
