# Workspace Root Reorganization — Plan

**Goal:** Turn this cluttered, 2,560-file, behind-by-4, dirty repo into a clean **AI/agent skills sandbox**, with the legacy physics research relocated out and Git hygiene restored.

**Status:** Plan only — not executed. Execute on branch `chore/workspace-reorg`, local-only, **no push** until reviewed.

**Confirmed:** remote `wenfe/VSCode_TNEW` is yours.

---

## Decisions (from grilling session)

| # | Decision | ADR |
|---|----------|-----|
| D1 | Workspace identity = **AI/agent skills sandbox**; physics research is legacy | [0001](adr/0001-ai-sandbox-identity.md) |
| D2 | Relocate research → sibling `../Verteidigung_Research/` (off-repo; history on origin) | — |
| D3 | **Stabilize Git first** (Phase 0); reads/pull during planning, pushes only when approved | — |
| D4 | `.github/skills/` = git-ignored local clone (track only its README) | [0002](adr/0002-github-skills-vendoring.md) |
| D5 | Full hygiene: comprehensive `.gitignore` + `git rm --cached` already-tracked artifacts | — |
| D6 | Remove cruft: `AspireApp/`, `docs/03_AspireApp_*.md`, `my.js`, `.github.zip` | — |
| D7 | Minimal/conventional layout; rewritten `README.md` is the map | — |

---

## Current state (verified)

- On `main`, **behind `origin/main` by 4 commits**; local has **0 commits ahead**.
- Working tree dirty: **406 deletions** (whole `AspireApp/` incl. committed `bin/Debug/*.dll`, `tool-guardian` hooks), **2 modified submodules**, `.vscode/mcp.json` modified, **7 untracked**.
- **2,560 tracked files**, **no `.gitignore`**.
- The 4 incoming commits: a `.github/skills` gitlink fix (→ README-only folder), added governance hooks + `logs/copilot/*`, and a merge.
- `origin/main` **still contains** the full `AspireApp/` tree — the local deletion is uncommitted only.

---

## Phase 0 — Stabilize Git (precondition)

**Outcome:** a clean `chore/workspace-reorg` branch based on an up-to-date `origin/main`, with the `.agents/` skill curation preserved.

```pwsh
# Safety net first
git branch backup/pre-reorg-2026-06-27           # snapshot current main pointer
git stash push -u -m "pre-reorg snapshot"         # set aside ALL local work (tracked + untracked)

# Clean, current base (resolves the .github/skills gitlink to origin's README-only version)
git checkout -b chore/workspace-reorg origin/main

# Reapply local work
git stash pop
```

**Known conflicts on `stash pop` (expected, resolve as noted):**
- `.github/skills` — gitlink → directory transition. Keep **origin's** version (README-only); the 290-skill clone stays on disk untracked (D4).
- `skills-lock.json` / `.agents/skills/**` — keep **local** (your curated 23 + catalog).
- `.vscode/mcp.json` — keep **local** edit.
- `AspireApp/` deletions — discard from the pop (origin's copy returns); it is removed deliberately in Phase 2.

> If `stash pop` gets messy, fall back: `git checkout origin/main -- .github/skills` and re-run the curation deterministically with `npx skills@latest add mattpocock/skills` + the removals from the catalog.

**Gate:** `git status` understood and intentional before proceeding.

---

## Phase 1 — Git hygiene (D5)

Create `.gitignore`:

```gitignore
# Python
.venv/
__pycache__/
*.pyc
# .NET
bin/
obj/
# Node
node_modules/
# Vendored skills clone (D4) — keep only the README
.github/skills/**
!.github/skills/
!.github/skills/README.md
# OS / editor
.DS_Store
Thumbs.db
*.zip
```

Untrack what now matches (disk untouched):

```pwsh
git rm -r --cached --quiet .venv __pycache__ 2>$null
git rm -r --cached --quiet .github/skills 2>$null
git add .gitignore .github/skills/README.md
git commit -m "chore: add .gitignore and untrack generated files + vendored skills clone"
```

**Expected effect:** tracked-file count drops sharply (the bulk of the 2,560 were `bin/Debug` DLLs + the skills clone).

---

## Phase 2 — Remove cruft (D6)

```pwsh
git rm -r AspireApp/                       # recoverable from origin history
git rm docs/03_AspireApp_*.md              # 4 leftover writeups
git rm my.js                               # if tracked; else: Remove-Item my.js
# .github.zip — verify first:
git ls-files --error-unmatch .github.zip   # tracked? -> git rm; untracked? -> Remove-Item (redundant backup)
git commit -m "chore: remove AspireApp project, stale docs, and scratch files"
```

> `tool-guardian` hooks were deleted locally but origin doesn't re-add them — decide whether the sandbox wants them. Default: leave removed (other governance hooks already exist).

---

## Phase 3 — Relocate legacy research (D2)

```pwsh
$dst = "..\Verteidigung_Research"
New-Item -ItemType Directory -Force $dst | Out-Null
Move-Item Verteidigung, T3D_csv, Jupiter_Notebook.ipynb, requirements.txt $dst
git rm -r --cached Verteidigung T3D_csv Jupiter_Notebook.ipynb requirements.txt
git add -A
git commit -m "chore: relocate physics research to sibling ../Verteidigung_Research"
```

**Net:** every research file lives on disk in the sibling folder; removed from the sandbox; history on origin preserves them.

---

## Phase 4 — README + decision docs (D7)

- Rewrite `README.md` as the **sandbox map**: identity (link [CONTEXT.md](../CONTEXT.md)), top-level layout, how skills work (link [.agents/skills/README.md](../.agents/skills/README.md)), governance/logs note, and a "research moved to ../Verteidigung_Research" pointer.
- ADRs already created: [0001](adr/0001-ai-sandbox-identity.md), [0002](adr/0002-github-skills-vendoring.md).
- Glossary already created: [CONTEXT.md](../CONTEXT.md).

```pwsh
git add README.md CONTEXT.md docs/
git commit -m "docs: rewrite README as sandbox map; add ADRs and CONTEXT glossary"
```

---

## Phase 5 — Verify & hand off

```pwsh
(git ls-files | Measure-Object -Line).Lines    # expect a few hundred, not 2,560
git status                                       # clean
npx skills@latest list                           # 23 curated skills intact
```

- **Do not push.** Leave `chore/workspace-reorg` for review; you push when ready.

---

## Projected final root

```
.agents/      curated skills (23) + catalog README
.github/      instructions, agents, prompts, plugins, hooks, skills/ (ignored clone, README tracked)
.vscode/      editor + MCP config
docs/         adr/ + this plan
logs/         copilot governance logs
.gitignore    CONTEXT.md  README.md
.mcp.json  skills-lock.json  package.json
```

---

## Risks & rollback

| Risk | Mitigation |
|------|------------|
| `stash pop` conflicts on `.github/skills` gitlink | Pre-resolved guidance in Phase 0; fallback re-clone + re-curate |
| Research lost | Lives in `../Verteidigung_Research/` **and** origin history; `backup/pre-reorg-2026-06-27` branch |
| Wrong file untracked/removed | Each phase is its own commit → `git revert`; nothing pushed |
| Behind-by-4 divergence | Phase 0 rebases onto `origin/main` before any change |

**Full rollback:** `git checkout main && git branch -D chore/workspace-reorg && git stash pop` (restores pre-reorg working tree from the snapshot).
