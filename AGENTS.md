# AGENTS.md — documentation

Gate: what `.github/workflows/build.yml` runs — actionlint, then `make html test fidelity
term-check rebrand-check linkcheck check-site` — plus `make structure` (the `docs` workflow).
The roster is cloned under `APS_ORG_ROOT` and `gh` is authenticated; a step you could not run
is named in the pull request.

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
