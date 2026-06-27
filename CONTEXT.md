# VSCode_T — Workspace Context

This repository is an **AI/agent skills sandbox**: a working environment for authoring, curating, and running GitHub Copilot / agent skills, instructions, prompts, and MCP configuration. It is not an application or a research project — those concerns live elsewhere.

## Language

**AI Sandbox**:
The identity of this repository — an environment for agent tooling (skills, prompts, instructions, MCP, hooks). The thing the repo *is*.
_Avoid_: project, app, workspace (when meaning the repo's purpose)

**Curated Skills**:
The hand-picked, actively-maintained skills under `.agents/skills/`, managed by the `skills` CLI and `skills-lock.json`.
_Avoid_: my skills, installed skills

**Vendored Skills**:
The large read-only `.github/skills/` collection — a local clone of an external skills repo, browsed but never edited in place and not tracked in this repo's history.
_Avoid_: submodule, the skills repo

**Legacy Research**:
The physics/thesis-defense material (formerly `Verteidigung/`, `T3D_csv/`, root notebooks) relocated out of the sandbox. Retained for history, not part of the sandbox going forward.
_Avoid_: the data, the science, Verteidigung (when meaning "the files")

**Governance Logs**:
The `logs/copilot/` audit/session/secrets/license output produced by the `.github/hooks/` governance hooks.
_Avoid_: logs (unqualified)
