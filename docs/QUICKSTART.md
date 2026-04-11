# SpecKit Quick Start (5 minutes)

> From zero to a validated, spec-driven initiative in one session.

## Prerequisites

```bash
pip install pyyaml check-jsonschema    # Python 3.10+
npm install -g markdownlint-cli2       # Node 18+
```

## Option A: Guided (Claude Code)

```text
/speckit-start
```

Answer 5 questions. Done. Initiative created and validated.

## Option B: Manual

### 1. Clone & install

```bash
git clone https://github.com/Karfev/Product-base-Spec-Kit.git
cd Product-base-Spec-Kit
make install-tools
```

### 2. Bootstrap your initiative

```bash
./tools/init.sh INIT-2026-042-my-feature 042-my-feature \
  --profile minimal --product platform --owner @your-team
```

### 3. Fill PRD & requirements

Open `initiatives/INIT-2026-042-my-feature/prd.md` — fill problem, outcome, scope.
Open `requirements.yml` — add one requirement per scope item (id, title, type, priority, status, description, acceptance_criteria, trace).

### 5. Validate

```bash
make validate
```

If it passes — you have your first spec-validated initiative.

## What's next?

- **Add detail:** `/speckit-requirements INIT-2026-042-my-feature`
- **Add contracts:** `/speckit-contracts INIT-2026-042-my-feature`
- **Upgrade profile:** `./tools/upgrade.sh INIT-2026-042-my-feature --profile standard`
- **Full guide:** see [README.md](../README.md)
