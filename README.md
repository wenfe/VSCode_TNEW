# AI / Agent Skills Sandbox

A working environment for authoring, curating, and running GitHub Copilot / agent skills, instructions, prompts, and MCP configuration. See [CONTEXT.md](CONTEXT.md) for the vocabulary.

> Physics/thesis research that used to live here was relocated to a sibling folder `../Verteidigung_Research/` (see [ADR 0001](docs/adr/0001-ai-sandbox-identity.md)). It remains in this repo's Git history.

## Layout

```
.agents/      Curated skills (23) — managed by the `skills` CLI; see catalog below
.github/      instructions, prompts, agents, plugins, hooks, and skills/ (ignored vendored clone)
.vscode/      Editor + MCP config
docs/         adr/ (decision records) + workspace-reorg-plan.md
logs/         Copilot governance logs (audit / secrets / license / session)
.gitignore  .mcp.json  skills-lock.json  package.json
```

## Skills

- **Curated skills** live in [`.agents/skills/`](.agents/skills/) — see the full catalog in [.agents/skills/README.md](.agents/skills/README.md).
- **Vendored skills** ([`.github/skills/`](.github/skills/), ~290) are a **git-ignored local clone** — browsable, read-only, not tracked here (see [ADR 0002](docs/adr/0002-github-skills-vendoring.md)).

Manage curated skills with the CLI:

```bash
npx skills@latest list          # list installed skills
npx skills@latest add <owner/repo>
npx skills@latest remove <name> -y
npx skills@latest update
```

## Governance

`.github/hooks/` run session-boundary governance (secrets scan, license check, audit, auto-commit) and write to [`logs/copilot/`](logs/copilot/).

## Decisions

Architectural decisions are recorded in [`docs/adr/`](docs/adr/). The workspace reorganization itself is documented in [docs/workspace-reorg-plan.md](docs/workspace-reorg-plan.md).
