# Skills Catalog

Index of agent skills available in this workspace. **Nothing here is moved or restructured** — skill folders stay flat because the `skills` CLI and Copilot both discover them by globbing `<name>/SKILL.md`.

Two collections exist:

| Collection | Location | Count | Managed by |
|------------|----------|-------|------------|
| Matt Pocock skills (installed) | `.agents/skills/` | 23 | `skills` CLI + [`skills-lock.json`](../../skills-lock.json) |
| awesome-copilot (vendored) | [`.github/skills/`](../../.github/skills/) | ~290 | Its own git repo (do not edit in place) |

---

## Installed skills — `.agents/skills/` (23)

Source: [`mattpocock/skills`](https://github.com/mattpocock/skills). All are user-invoked (`disable-model-invocation: true`) — you trigger them explicitly.

### Engineering (14)

| Skill | What it does |
|-------|--------------|
| `setup-matt-pocock-skills` | One-time repo setup for the engineering skills — issue tracker, triage labels, domain-doc layout. **Run this first.** |
| `ask-matt` | Router that points you to the right skill or flow for your situation. |
| `codebase-design` | Shared vocabulary for designing deep modules; finds deepening opportunities and seams. |
| `domain-modeling` | Build and sharpen a project's domain model and ubiquitous language. |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. |
| `tdd` | Test-driven development (red-green-refactor), test-first feature and bug work. |
| `implement` | Implement a piece of work from a PRD or set of issues. |
| `prototype` | Build a throwaway prototype — runnable terminal app or several toggleable UI variants. |
| `improve-codebase-architecture` | Scan for deepening opportunities, render an HTML report, then grill the one you pick. |
| `to-prd` | Turn the current conversation into a PRD and publish it to the issue tracker. |
| `to-issues` | Break a plan/spec/PRD into independent, grabbable issues (vertical slices). |
| `triage` | Move issues and external PRs through a triage state machine into agent-ready briefs. |
| `grill-with-docs` | Relentless plan/design interview that also produces ADRs and a glossary. |
| `resolving-merge-conflicts` | Resolve an in-progress git merge/rebase conflict. |

### Productivity (5)

| Skill | What it does |
|-------|--------------|
| `grilling` | Interview you relentlessly to stress-test a plan or design before building. |
| `grill-me` | Lighter relentless interview to sharpen a plan or design. |
| `handoff` | Compact the current conversation into a handoff doc for another agent. |
| `teach` | Teach you a new skill or concept within this workspace. |
| `writing-great-skills` | Reference for writing and editing skills well — vocabulary and principles. |

### Misc / setup (4)

| Skill | What it does |
|-------|--------------|
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged, type-check, and tests. |
| `git-guardrails-claude-code` | Claude Code hooks that block dangerous git commands (push, reset --hard, etc.). |
| `scaffold-exercises` | Create exercise directory structures (sections, problems, solutions). |
| `migrate-to-shoehorn` | Migrate test files from `as` assertions to `@total-typescript/shoehorn`. |

### Managing this collection

```bash
npx skills@latest list                 # list installed skills
npx skills@latest add mattpocock/skills # re-add / restore skills
npx skills@latest remove <name> -y      # remove a skill (updates lock + symlinks)
npx skills@latest update                # update to latest versions
```

> Removed in this curation pass (12): `design-an-interface`, `qa`, `request-refactor-plan`, `ubiquitous-language` (deprecated); `decision-mapping`, `loop-me`, `review`, `writing-beats`, `writing-fragments`, `writing-shape` (in-progress); `edit-article`, `obsidian-vault` (personal). Re-add any with `npx skills@latest add mattpocock/skills`.

---

## Vendored collection — `.github/skills/` (~290)

This is a separate cloned git repo (has its own `.git`, `.claude-plugin/`, `THIRD_PARTY_NOTICES.md`). **Browse, don't restructure** — moving folders here creates large diffs in a foreign repo and breaks Copilot's discovery. Full descriptions live in each `SKILL.md`; high-level themes:

| Theme | Examples |
|-------|----------|
| Azure & cloud infra | `azure-architecture-autopilot`, `az-cost-optimize`, `azure-deployment-preflight`, `import-infrastructure-as-code`, `cloud-design-patterns` |
| MCP servers | `mcp-builder`, `mcp-apps`, `*-mcp-server-generator` (go/java/kotlin/php/python/ruby/rust/swift/typescript) |
| AI / agents / LLM | `agent-governance`, `agentic-eval`, `eval-driven-dev`, `microsoft-agent-framework`, `semantic-kernel`, `prompt-optimizer` |
| Observability | `arize-*` (trace, evaluator, dataset, experiment), `phoenix-*` (cli, evals, tracing) |
| .NET / C# | `csharp-*` (async/docs/xunit/nunit/mstest/tunit), `ef-core`, `mvvm-toolkit*`, `dotnet-best-practices` |
| Java / JVM | `java-*`, `kotlin-springboot`, `spring-boot-testing`, `create-spring-boot-*`, `javax-to-jakarta-migration` |
| Frontend / web | `frontend-design`, `premium-frontend-ui`, `react18-*`, `react19-*`, `unit-test-vue-pinia`, `webapp-testing` |
| Databases | `postgresql-*`, `sql-*`, `qdrant-*`, `*-oracle-to-postgres-*`, `cosmosdb-datamodeling`, `snowflake-semanticview` |
| Power Platform / BI | `power-bi-*`, `powerbi-modeling`, `power-platform-*`, `flowstudio-power-automate-*`, `typespec-*` |
| Docs & content | `docx`, `pdf`, `pptx`, `xlsx`, `documentation-writer`, `create-readme`, `markdown-to-html`, `meeting-minutes` |
| Diagrams & visuals | `draw-io-diagram-generator`, `excalidraw-diagram-generator`, `plantuml-ascii`, `canvas-design`, `generate-image` |
| Git / GitHub / PM | `git-commit`, `conventional-commit`, `github-issues`, `github-release`, `breakdown-*`, `dependabot`, `codeql` |
| Security & quality | `security-review`, `threat-model-analyst`, `gdpr-compliant`, `quality-playbook`, `audit-integrity` |
| Testing | `pytest-coverage`, `playwright-*`, `scoutqa-test`, `javascript-typescript-jest` |
| Refactor & migration | `refactor`, `refactor-plan`, `ruff-recursive-fix`, `dotnet-upgrade`, `winui3-migration-guide` |
| Platform-specific | `rhino3d-scripts`, `freecad-scripts`, `slang-shader-engineer`, `salesforce-*`, `vscode-ext-*`, `batch-files` |
| Personal productivity | `daily-prep`, `email-drafter`, `brag-sheet`, `roundup`, `workiq-copilot`, `exam-ready`, `napkin` |
| Go-to-market / business | `gtm-*` (positioning, pricing, partnerships, onboarding, ...) |
| Meta / authoring | `skill-creator`, `microsoft-skill-creator`, `*-blueprint-generator`, `suggest-awesome-github-copilot-*` |

To explore: open [`.github/skills/`](../../.github/skills/) and read any `SKILL.md`, or discover more at <https://skills.sh/>.
