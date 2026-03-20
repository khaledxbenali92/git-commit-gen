<div align="center">

# ⚡ git-commit-gen

### Generate perfect Git commit messages from your staged changes — instantly

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/khaledxbenali92/git-commit-gen?style=for-the-badge&color=yellow)](https://github.com/khaledxbenali92/git-commit-gen/stargazers)
[![CI](https://img.shields.io/github/actions/workflow/status/khaledxbenali92/git-commit-gen/ci.yml?style=for-the-badge&label=CI)](https://github.com/khaledxbenali92/git-commit-gen/actions)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Styles](#-commit-styles) • [Contributing](#-contributing)

</div>

---

## 😤 The Problem

Every developer faces this moment:

```bash
$ git add .
$ git commit -m "..."   # what do I write here?!
```

Bad commits like `"fix stuff"`, `"update"`, `"wip"` plague every codebase. They make git history useless.

**git-commit-gen** analyzes your staged diff and generates professional commit messages in seconds — no API key required.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚡ **Zero Dependencies** | Works out of the box — no API key needed |
| 🎨 **Multiple Styles** | Conventional, Emoji (Gitmoji), Angular, Simple |
| 🤖 **AI Mode** | Optional GPT-4 or Ollama for smarter suggestions |
| 📊 **Confidence Score** | Each suggestion rated by relevance |
| 🔍 **Smart Analysis** | Detects file types, change patterns, scope automatically |
| 💥 **Breaking Changes** | Automatically detects and marks breaking changes |
| 🪝 **Git Hook** | Install as prepare-commit-msg hook |
| 🌍 **Multi-language** | Generate messages in EN, FR, ES, DE, AR |
| 🔄 **Interactive** | Select, edit, or regenerate suggestions |

---

## 🎬 Demo

```bash
$ git add src/auth.py
$ python main.py

╔══════════════════════════════════════════════════════════╗
║        ⚡ Git Commit Message Generator v1.0              ║
╚══════════════════════════════════════════════════════════╝

💡 Generated commit messages:

  [1] feat(src): add authenticate_user functionality
       Confidence: ██████████ 95%

  [2] feat(src): implement jwt token feature
       Confidence: █████████░ 85%

  [3] feat(auth): add authentication to backend
       Confidence: ████████░░ 75%

💡 Options:
  [1-3] Select a suggestion
  [e] Edit before committing
  [r] Regenerate
  [q] Quit

Your choice: 1
✅ Committed: feat(src): add authenticate_user functionality
```

---

## 🛠️ Installation

### Quick Start (No API key needed)

```bash
git clone https://github.com/khaledxbenali92/git-commit-gen.git
cd git-commit-gen
```

That's it. No dependencies to install for basic usage.

### Optional — AI Mode

```bash
pip install openai          # for GPT-4 mode
pip install requests        # for Ollama mode
```

### Optional — Add to PATH

```bash
# Add alias to your shell
echo 'alias gcgen="python /path/to/git-commit-gen/main.py"' >> ~/.bashrc
source ~/.bashrc

# Now use anywhere
gcgen
```

---

## 📖 Usage

### Basic — Generate from staged changes

```bash
git add .
python main.py
```

### Choose a style

```bash
python main.py --style conventional   # feat(scope): description
python main.py --style emoji          # ✨ add new feature
python main.py --style simple         # Add user authentication
```

### Generate more options

```bash
python main.py --count 5    # Generate 5 suggestions
```

### Auto-commit with best suggestion

```bash
python main.py --auto-commit
```

### Use AI mode (better results)

```bash
# With OpenAI
export OPENAI_API_KEY=sk-...
python main.py --provider openai

# With Ollama (local, free)
ollama pull llama3
python main.py --provider ollama
```

### Scan specific files only

```bash
python main.py --files src/auth.py src/models.py
```

### Generate in another language

```bash
python main.py --lang fr    # French
python main.py --lang es    # Spanish
python main.py --lang ar    # Arabic
```

### Dry run — preview without committing

```bash
python main.py --dry-run
```

### Install as git hook

```bash
python main.py --hook
# Now every 'git commit' auto-suggests a message
```

---

## 🎨 Commit Styles

### Conventional Commits (default)
```
feat(auth): add JWT token refresh mechanism
fix(api): resolve null pointer in user endpoint
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
```

### Emoji / Gitmoji
```
✨ add JWT token refresh mechanism
🐛 fix null pointer in user endpoint
📝 update installation instructions
♻️ simplify date formatting logic
```

### Simple
```
Add JWT token refresh mechanism
Fix null pointer in user endpoint
Update installation instructions
Simplify date formatting logic
```

---

## 🔍 How It Works

```
git diff --cached
       ↓
  DiffAnalyzer
  ├── Detect file types & domains
  ├── Find change patterns (new function, bug fix, test...)
  ├── Extract meaningful keywords
  ├── Detect scope from file paths
  └── Identify breaking changes
       ↓
  CommitGenerator
  ├── Rule-based (default, no API key)
  ├── OpenAI GPT-4 (optional)
  └── Ollama local LLM (optional)
       ↓
  Ranked suggestions with confidence scores
```

---

## 📁 Project Structure

```
git-commit-gen/
├── main.py                          # CLI entry point
├── src/
│   ├── generator.py                 # Main orchestrator
│   ├── analyzers/
│   │   └── diff_analyzer.py         # Diff analysis engine
│   ├── generators/
│   │   ├── conventional.py          # Conventional commits
│   │   ├── emoji_style.py           # Gitmoji style
│   │   └── ai_generator.py          # OpenAI & Ollama
│   └── utils/
│       ├── git.py                   # Git operations
│       └── display.py               # Terminal output
├── tests/
│   └── test_generator.py            # 14 unit tests
├── .github/workflows/ci.yml         # CI pipeline
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🗺️ Roadmap

- [x] Rule-based generation (zero dependencies)
- [x] Conventional commits style
- [x] Emoji / Gitmoji style
- [x] OpenAI integration
- [x] Ollama local LLM support
- [x] Breaking change detection
- [x] Git hook installation
- [x] Multi-language support
- [ ] VS Code extension
- [ ] PyPI package (`pip install gcgen`)
- [ ] JetBrains plugin
- [ ] Neovim plugin
- [ ] GitHub Action

---

## 🤝 Contributing

```bash
git clone https://github.com/YOUR-USERNAME/git-commit-gen.git
cd git-commit-gen
git checkout -b feat/your-feature
# make changes
pytest tests/ -v
git commit -m "feat: your feature"  # use the tool on itself! 🔄
git push origin feat/your-feature
```

**Ideas:**
- 🎨 New commit styles
- 🌍 More language support
- 🔌 Editor integrations
- 🧠 Better pattern detection
- 📊 More confidence scoring logic

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Khaled Ben Ali**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/benalikhaled)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=flat&logo=twitter)](https://twitter.com/khaledbali92)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-333?style=flat&logo=github)](https://github.com/khaledxbenali92)

---

<div align="center">

⭐ **Star this if you're tired of writing "fix stuff" commits!** ⭐

</div>
