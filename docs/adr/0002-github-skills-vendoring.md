# `.github/skills/` is a git-ignored local clone

The ~290-skill `.github/skills/` collection is kept as a local clone whose nested `.git` is git-ignored; only `.github/skills/README.md` is tracked. Origin already reduced this path to a README-only folder (commit `acd5c28`, "remove broken .github/skills gitlink causing agent job checkout failure"), so this aligns the sandbox with the upstream fix and permanently removes the submodule-checkout failure from CI.

## Considered Options

- **Vendor for real** (commit all ~290 folders) — rejected: bloats history with externally-authored content.
- **Proper submodule** (`.gitmodules`) — rejected: reintroduces the exact submodule checkout that broke CI.
- **Git-ignored local clone** — chosen: skills stay browsable on disk, repo stays slim, CI is fixed.

## Consequences

- The 290 skills are available locally but are not version-controlled here; re-cloning is needed on a fresh checkout.
- The skills catalog ([.agents/skills/README.md](../../.agents/skills/README.md)) already frames them as "vendored, read-only," consistent with this decision.
