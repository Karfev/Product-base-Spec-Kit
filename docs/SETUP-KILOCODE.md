# SpecKit + Kilo Code: IDE Setup Guide

> Run SpecKit commands from VS Code or JetBrains IDE with any LLM provider.

## VS Code Setup

### 1. Install Kilo Code Extension

Open VS Code → Extensions → Search "Kilo Code" → Install.

### 2. Configure LLM Provider

Open Kilo Code settings and choose one of:

**Option A: Local LLM (Ollama)**
- Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
- Pull model: `ollama pull qwen2.5-coder:32b`
- In Kilo Code settings: Provider → "Ollama", Base URL → `http://localhost:11434`

**Option B: Anthropic API (Claude)**
- In Kilo Code settings: Provider → "Anthropic", API Key → your key

**Option C: OpenAI-compatible endpoint**
- In Kilo Code settings: Provider → "OpenAI Compatible", Base URL → your endpoint

### 3. Clone SpecKit

```bash
git clone https://github.com/Karfev/Product-base-Spec-Kit.git
cd Product-base-Spec-Kit
make install-tools
```

Open the repository in VS Code.

### 4. Run Commands

Kilo Code natively reads `.claude/commands/` — all 31 SpecKit skills are available.

Open Command Palette (Cmd/Ctrl+Shift+P) → type the skill name → run.

### 5. Smoke Test

Run `/speckit-start` from the Command Palette. Answer 5 questions. Then in terminal:

```bash
make validate
```

## JetBrains Setup (IntelliJ IDEA / PyCharm)

### 1. Install Kilo Code Plugin

Settings → Plugins → Marketplace → Search "Kilo Code" → Install → Restart IDE.

### 2. Configure LLM Provider

Same options as VS Code (Ollama, Anthropic, OpenAI-compatible).

### 3. Run Commands

Access SpecKit skills from the AI Assistant panel. Kilo Code discovers skills in `.claude/commands/`.

## Model Recommendations

| Use Case | Recommended Model |
|----------|------------------|
| Full workflow (all 31 commands) | Qwen2.5-Coder-32B fp16 |
| Budget / limited VRAM | Qwen2.5-Coder-14B fp16 |
| Cloud API (best quality) | Claude Opus 4 via Anthropic |

## Known Limitations

- **Context window:** Qwen2.5-Coder-32B practical context is 32K-64K tokens.
- **Complex reasoning:** `/speckit-architecture` quality depends heavily on model capability.
- **Terminal access:** Some commands run `make validate` — ensure VS Code terminal is available.
