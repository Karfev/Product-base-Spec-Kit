---
status: "proposed"
date: "2026-04-11"
decision-makers: ["@karfev"]
consulted: []
informed: ["@speckit"]
---

# ADR-0001: Local Model Selection for On-Premise SpecKit Deployment

**Status:** proposed
**Date:** 2026-04-11
**Decision-makers:** @karfev

## Context and problem statement

SpecKit commands are text-in/text-out SKILL.md prompts requiring: YAML generation accuracy, instruction following, large context for codebases, structured output (Mermaid, markdown tables). For on-premise deployment (INIT-2026-005), we need to select an open-weight model that fits target hardware and produces acceptable quality output across all 26 commands.

## Decision drivers

- VRAM fit on target hardware (H100 80GB, RTX 6000 PRO 96GB)
- Instruction-following quality for multi-step workflows
- YAML/code generation accuracy
- Latency within SLO targets (120s H100, 300s RTX 6000)
- Open-weight license for on-premise deployment

## Considered options

### 1. Qwen2.5-Coder-32B-Instruct (RECOMMENDED)

| Spec | Value |
|------|-------|
| Parameters | 32B |
| VRAM (fp16) | ~64 GB |
| VRAM (Q4_K_M) | ~22 GB |
| Context (claimed) | 128K |
| Context (practical) | 32K-64K |
| Coding benchmark | 88.4% |
| H100 80GB | ✅ fp16 |
| RTX 6000 PRO 96GB | ✅ fp16 |

Best instruction following among open-weight models. Native JSON mode for structured output.

### 2. Qwen2.5-Coder-14B-Instruct (BUDGET FALLBACK)

| Spec | Value |
|------|-------|
| Parameters | 14B |
| VRAM (fp16) | ~28 GB |
| H100 80GB | ✅ fp16 |
| RTX 6000 PRO 96GB | ✅ fp16 |

Half the parameters, faster inference. Acceptable for simpler commands.

### 3. Llama-3.3-70B-Instruct

| Spec | Value |
|------|-------|
| Parameters | 70B |
| VRAM (fp16) | ~140 GB |
| H100 80GB | ⚠️ Q4_K_M only (~40 GB) |
| RTX 6000 PRO 96GB | ⚠️ Q4_K_M only |

Good general instruction following but lower YAML accuracy than Qwen.

### 4. DeepSeek-V3 (671B MoE) — REJECTED

| Spec | Value |
|------|-------|
| Parameters | 671B (37B active) |
| VRAM | ~380 GB minimum |
| H100 80GB | ❌ Does NOT fit |
| RTX 6000 PRO 96GB | ❌ Does NOT fit |

All 671B parameters must be in VRAM for MoE routing. Single-GPU deployment is NOT feasible.

## Decision outcome

**Primary (both tiers):** Qwen2.5-Coder-32B-Instruct at fp16.
- H100 80GB: fp16 with 16GB headroom
- RTX 6000 PRO 96GB: fp16 with 32GB headroom

**Fallback:** Qwen2.5-Coder-14B-Instruct for constrained environments.

**Status:** proposed — pending smoke-test validation on actual hardware.

### Consequences

- **Good:** All 26 SpecKit commands supported on both hardware tiers. Latency SLO: ~120s (H100) and ~300s (RTX 6000) based on bandwidth difference (3.35 TB/s vs 1.8 TB/s).
- **Bad:** Practical context window is 32K-64K, not 128K — must document in setup guides. Complex reasoning commands (`/speckit-architecture`) may produce lower quality than Claude Opus.
- **Neutral:** Quantized (Q4_K_M) deployment available as escape hatch for GPUs with <64GB VRAM, at quality cost.

### Confirmation

Smoke-test 5 key commands (`/speckit-start`, `/speckit-prd`, `/speckit-requirements`, `/speckit-implement`, `/speckit-trace`) on both H100 and RTX 6000 PRO with Qwen2.5-Coder-32B-Instruct at fp16. Pass criteria: `make validate` succeeds on generated artifacts.

---

*Template based on [MADR](https://adr.github.io/madr/) (including YAML front-matter and Confirmation).*
