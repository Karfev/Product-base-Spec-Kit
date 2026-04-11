# SpecKit + OpenCode: On-Premise Setup Guide

> Run the full SpecKit workflow with OpenCode and a local LLM. No cloud API required.

## Prerequisites

- Ubuntu 22.04+ (or macOS 14+)
- NVIDIA drivers + CUDA toolkit (for GPU inference)
- Python 3.10+, Node.js 18+
- Git

## 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify: `ollama --version`

## 2. Pull a Model

**For H100 80 GB (datacenter):**
```bash
ollama pull qwen2.5-coder:32b          # fp16, ~64 GB VRAM
```

**For RTX 6000 PRO Blackwell 96 GB (workstation):**
```bash
ollama pull qwen2.5-coder:32b          # fp16, ~64 GB VRAM (fits with 32 GB headroom)
```

**For RTX 4090 / consumer 24 GB GPU:**
```bash
ollama pull qwen2.5-coder:32b-instruct-q4_K_M   # Q4, ~22 GB VRAM
```

See [ADR: Model Selection](../initiatives/INIT-2026-005-multi-agent-portability/decisions/INIT-2026-005-ADR-0001-model-selection.md) for detailed comparison.

## 3. Install OpenCode

```bash
# See https://opencode.ai for latest install instructions
curl -fsSL https://opencode.ai/install.sh | sh
```

Configure local endpoint:
```bash
opencode config set model ollama/qwen2.5-coder:32b
opencode config set api-base http://localhost:11434/v1
```

## 4. Clone SpecKit

```bash
git clone https://github.com/Karfev/Product-base-Spec-Kit.git
cd Product-base-Spec-Kit
make install-tools
```

OpenCode discovers skills via `.opencode/skills/` (symlinked to `.claude/commands/`).

## 5. Smoke Test

```bash
# In OpenCode:
/speckit-start
# Answer 5 questions, then:
make validate
```

## Hardware Recommendations

| Hardware | Model | Precision | Expected Latency |
|----------|-------|-----------|-----------------|
| H100 80 GB HBM3 | Qwen2.5-Coder-32B | fp16 | ~120s for /speckit-prd |
| RTX 6000 PRO Blackwell 96 GB | Qwen2.5-Coder-32B | fp16 | ~300s for /speckit-prd |
| RTX 4090 24 GB | Qwen2.5-Coder-32B | Q4_K_M | ~300-500s (bandwidth limited) |

## Known Limitations

- **Context window:** Qwen2.5-Coder-32B practical context is 32K-64K tokens (not the claimed 128K). For large initiatives with many files, break work into smaller commands.
- **Complex reasoning:** Commands like `/speckit-architecture` (16 questions, IS-ontology) may produce lower quality output compared to Claude Opus. Review outputs carefully.
- **OpenCode directory:** OpenCode does not read `.claude/commands/` natively (issue #6985). SpecKit provides `.opencode/skills/` symlink as workaround.
- **DeepSeek-V3 is NOT supported** for single-GPU deployment (~380 GB VRAM required for full MoE model).
