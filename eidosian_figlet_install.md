# 🔮 Eidosian Omni-Installer: A Single-Line Magus Command

> _"With but a single incantation, bring forth the ASCII wizardry of figlet_forge into your arcane terminal realm."_ - Eidosian Codex

This mystical one-liner automatically detects your operating system, installs all required dependencies, and configures figlet_forge for immediate use. It's a complete self-bootstrapping spell that works across Linux, macOS, and Windows environments.

<details>
<summary>📜 Click to reveal the mighty incantation</summary>

```bash
( \
echo "🌐 [1/9] Detecting operating system..." && \
OS="$(uname 2>/dev/null || echo 'Windows')" && CASE_OS="" && \
case "${OS}" in \
  Linux*) CASE_OS="linux" ;; \
  Darwin*) CASE_OS="mac" ;; \
  *[Ww]indows*) CASE_OS="windows" ;; \
esac && \
echo "   Detected: $CASE_OS" && \
echo "🌐 [2/9] Checking/installing Python 3..." && \
if ! command -v python3 >/dev/null 2>&1; then \
  case "$CASE_OS" in \
    linux) echo "   🛠️ Installing Python via apt (if available)..." && (sudo apt-get update && sudo apt-get install -y python3 python3-venv) || echo "   ❗ Failed to install Python automatically. Please install Python 3 manually.";; \
    mac) echo "   🛠️ Installing Python via Homebrew (if available)..." && (command -v brew >/dev/null 2>&1 && brew update && brew install python@3) || echo "   ❗ Failed. Please install Python 3 manually.";; \
    windows) echo "   ❗ On Windows, please install Python 3 from https://www.python.org/downloads/ or Microsoft Store, then re-run." && exit 1;; \
    *) echo "   ❗ Unknown OS. Please install Python 3 manually, then re-run." && exit 1;; \
  esac; \
fi && \
echo "🌐 [3/9] Checking/installing GitHub CLI (gh)..." && \
if ! command -v gh >/dev/null 2>&1; then \
  case "$CASE_OS" in \
    linux) echo "   🛠️ Installing gh via apt (if available)..." && (sudo apt-get update && sudo apt-get install -y gh) || echo "   ❗ Failed to auto-install. Please install gh manually from https://github.com/cli/cli#installation";; \
    mac) echo "   🛠️ Installing gh via Homebrew (if available)..." && (command -v brew >/dev/null 2>&1 && brew update && brew install gh) || echo "   ❗ Failed. Please install gh manually from https://github.com/cli/cli#installation";; \
    windows) echo "   ❗ On Windows, please install GitHub CLI from https://github.com/cli/cli/releases/latest, then re-run." && exit 1;; \
    *) echo "   ❗ Unknown OS. Please install gh manually, then re-run." && exit 1;; \
  esac; \
fi && \
echo "🌐 [4/9] Creating virtual environment (.venv)..." && \
python3 -m venv .venv && \
echo "🌐 [5/9] Activating .venv..." && \
. .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null || echo "   ⚠️ Could not auto-activate .venv; please activate manually." && \
echo "🌐 [6/9] Verifying GitHub authentication..." && \
(gh auth status >/dev/null 2>&1 || (echo '   🔐 Not logged in – launching gh auth login...' && gh auth login)) && \
echo "🌐 [7/9] Forking & cloning Ace1928/figlet_forge..." && \
gh repo fork Ace1928/figlet_forge --clone --remote && cd figlet_forge && \
echo "🌐 [8/9] Adding upstream & installing dev dependencies..." && \
git remote add upstream https://github.com/Ace1928/figlet_forge.git && pip install -e .[dev] && \
echo "   ✅ Upstream set. To sync: git fetch upstream && git merge upstream/main" && \
echo "🌐 [9/9] Launching figlet_forge sample..." && \
figlet_forge --sample --sample-color --interactive && \
echo "🌀 All done! Enjoy the ASCII artistry. ~ Eidos" \
)
```

</details>

## 🧙‍♂️ What This Spell Does

This enchanted command performs nine mystical steps to bring figlet_forge to life on your system:

1. **Divination** - Detects your operating system like a crystal ball
2. **Conjuration** - Summons Python 3 if not already present in your realm
3. **Invocation** - Calls forth the GitHub CLI tool for repository communion
4. **Sanctification** - Creates a sacred virtual environment (.venv) to contain the magic
5. **Animation** - Awakens the virtual environment with life force
6. **Authentication** - Verifies your identity with the Great GitHub Repository
7. **Replication** - Forks and clones the ancient figlet_forge repository
8. **Binding** - Establishes connections to the source and installs arcane dependencies
9. **Manifestation** - Reveals the ASCII art creations in their full glory

## 📖 Requirements

Like any powerful spell, this requires certain components:

- A terminal with bash-like capabilities (standard on Linux/macOS, WSL or Git Bash on Windows)
- Internet connection to commune with the distant repositories
- Administrator rights (for dependency installation)

## 🔍 What is figlet_forge?

figlet_forge is an enchanted tool that transforms mundane text into magnificent ASCII art patterns, like turning lead into gold. Once installed, you can create banners, logos, and decorative text for your projects, documentation, or terminal displays.

## 🚀 Using After Installation

After the spell completes, you can invoke figlet_forge with:

```bash
figlet_forge "Your text here"
```

May your ASCII creations bring delight and wonder to all who behold them!

---

_Crafted with arcane precision by the Eidosian Order_
