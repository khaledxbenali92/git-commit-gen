#!/usr/bin/env python3
"""
⚡ git-commit-gen — AI-powered Git Commit Message Generator
Generate perfect conventional commit messages from your staged changes
"""

import sys
import argparse
from src.generator import CommitGenerator
from src.utils.display import print_banner, print_error
from src.utils.git import get_staged_diff, get_staged_files, is_git_repo


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="⚡ Generate perfect Git commit messages with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from staged changes (most common)
  git add . && gcgen

  # Generate with specific style
  gcgen --style conventional
  gcgen --style emoji
  gcgen --style angular

  # Generate multiple options to choose from
  gcgen --count 5

  # Commit automatically with generated message
  gcgen --auto-commit

  # Analyze diff from specific files
  gcgen --files src/main.py src/utils.py

  # Dry run — see what would be committed
  gcgen --dry-run
        """
    )

    parser.add_argument(
        "--style",
        choices=["conventional", "emoji", "angular", "simple"],
        default="conventional",
        help="Commit message style (default: conventional)"
    )
    parser.add_argument(
        "--count", "-n",
        type=int, default=3,
        help="Number of suggestions to generate (default: 3)"
    )
    parser.add_argument(
        "--auto-commit", "-a",
        action="store_true",
        help="Automatically commit with the best suggestion"
    )
    parser.add_argument(
        "--files", "-f",
        nargs="+",
        help="Specific files to analyze"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama", "rule-based"],
        default="rule-based",
        help="AI provider (default: rule-based — works without API key)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be committed without committing"
    )
    parser.add_argument(
        "--lang",
        choices=["en", "fr", "es", "de", "ar"],
        default="en",
        help="Language for commit messages (default: en)"
    )
    parser.add_argument(
        "--hook",
        action="store_true",
        help="Install as git prepare-commit-msg hook"
    )

    args = parser.parse_args()

    # Install hook mode
    if args.hook:
        from src.utils.git import install_hook
        install_hook()
        return

    # Validate git repo
    if not is_git_repo():
        print_error("Not a git repository. Run 'git init' first.")
        sys.exit(1)

    # Get diff
    diff = get_staged_diff(args.files)
    files = get_staged_files(args.files)

    if not diff and not files:
        print_error("No staged changes found. Run 'git add .' first.")
        sys.exit(1)

    # Generate messages
    generator = CommitGenerator(provider=args.provider)
    suggestions = generator.generate(
        diff=diff,
        files=files,
        style=args.style,
        count=args.count,
        lang=args.lang
    )

    if not suggestions:
        print_error("Could not generate commit messages.")
        sys.exit(1)

    # Display and handle
    _handle_suggestions(suggestions, args)


def _handle_suggestions(suggestions: list, args):
    """Display suggestions and handle user choice."""
    from src.utils.display import display_suggestions
    from src.utils.git import do_commit

    if args.dry_run:
        print("\n📋 DRY RUN — These would be committed:\n")
        display_suggestions(suggestions)
        return

    if args.auto_commit:
        best = suggestions[0]
        print(f"\n✅ Auto-committing with:\n  {best['message']}\n")
        do_commit(best['message'])
        return

    # Interactive selection
    display_suggestions(suggestions)

    print("\n💡 Options:")
    print("  [1-{}] Select a suggestion".format(len(suggestions)))
    print("  [e] Edit before committing")
    print("  [r] Regenerate")
    print("  [q] Quit\n")

    choice = input("Your choice: ").strip().lower()

    if choice == "q":
        print("Cancelled.")
        return
    elif choice == "r":
        main()
        return
    elif choice == "e":
        import subprocess
        msg = suggestions[0]['message']
        edited = subprocess.check_output(
            f'echo "{msg}" | vipe', shell=True
        ).decode().strip()
        do_commit(edited)
    elif choice.isdigit() and 1 <= int(choice) <= len(suggestions):
        selected = suggestions[int(choice) - 1]
        do_commit(selected['message'])
        print(f"\n✅ Committed: {selected['message']}\n")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
