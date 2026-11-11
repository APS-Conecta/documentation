# AGENTS.md — documentation

Gate: what `.github/workflows/build.yml` runs — actionlint, then `make html test fidelity
term-check rebrand-check linkcheck check-site` — plus `make structure` (the `docs` workflow).
`APS_ORG_ROOT=<dir> tools/roster.sh` clones the roster (every `catalogo.yml` repository) there;
run the gate with that `APS_ORG_ROOT`, `SUITE_SRC=$APS_ORG_ROOT/gestion-aio` and `gh`
authenticated. A step you could not run is named in the pull request.

## Commits

- Commits and pull request titles: English Conventional Commits, as `desarrollo/documentation.md` («Idioma y registro») sets.
- Author: the identity of `main`'s commits (`git log -1 --format='%an <%ae>' origin/main`), never the machine's.
- Trailer: `Assisted-by: <agent>:<model>`, such as `claude-code:claude-opus-5-5`.
- Once per clone: `git config core.hooksPath .githooks`, the secrets hook.

## Agent skills

### Issue tracker

GitHub Issues on `APS-Conecta/documentation`, via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical vocabulary, unmodified: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`,
`wontfix`. All five exist on the repo. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: the vocabulary is `glosario.yml` (`make term-check`); `CONTEXT.md`, `GLOSSARY.md`
and `docs/adr/` are added only together with a `conf.py` `exclude_patterns` entry. See
`docs/agents/domain.md`.
