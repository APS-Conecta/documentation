# Changelog

All notable changes to `APS-Conecta/documentation` are recorded here.

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial Spanish documentation site for APS Conecta (docs-es R2): Sphinx +
  MyST-Parser + sphinx_rtd_theme with build-time brand transplant, the four
  Spanish audience trees (`usuario/`, `administracion/`, `desarrollo/`,
  `proyecto/`), `aviso.md`, `catalogo.yml` (15 repos) with generated catalog
  and per-app reference pages, graphify module maps, README quickstart
  includes, tracker pages, `build.yml` (CI + Pages), weekly `capturas.yml`,
  `about-sync.yml`, and the governance set (COPYING CC BY 3.0, AGPL, REUSE,
  canon files).
- Per-app release notes (scribe S2a): `proyecto/novedades/` holds one page per
  catalog row whose `kind` is suite, distribution-fork or nextcloud-app, listed in
  that row's `manuals`. `gen-catalogo.py` fails the build when such a row lacks its
  page, so the page set follows the catalog. 📚 Scribe fills the tables.
- Daily `schedule:` on `build.yml` (09:30 UTC, after Scribe) that also deploys, so
  the generated reference follows every repo's `main` on days nothing merges here.
- The base-platform machinery (scribe S2b): `upstream.yml` (source rule
  `nextcloud/documentation` `stable<major>`, the site-wide rename rule, and the map
  of all 509 upstream docs to APS pages); `tools/upstreamlib.py`, its one reader;
  the `{upstream}` directive (marker, attribution, «difiere» notice) and the
  `nc-doc`/`nc-ref` roles, which resolve to the woven APS page or to
  docs.nextcloud.com; `_ext/rebrand.py` («Nextcloud» → «APS Conecta Gestión» on
  every page except code, URLs, attribution, legal names and the legal notice);
  `tools/upstream-fidelity.py` and `tools/rebrand-check.py`, both in CI;
  `glosario.yml` published as `proyecto/glosario`; `tools/fetch-upstream.sh`;
  unit tests under `tools/tests/`.
- The legal notice states where everything comes from (scribe S2c): `aviso.md`
  «Origen: distribución derivada de Nextcloud» — the problem (no reliable document
  version in a CESFAM) and the goal (a primary-care centre installs the platform
  without a system administrator), the unmodified base, what APS modifies, the
  primary-care adaptations, own code, the manual text, and a components table
  generated from `componentes.yml` by `tools/gen-componentes.py` (versions from
  gestion `compose.yaml`/`VENDOR`, patch counts from the `.patch` files and the AIO
  queue; the build fails when gestion ships a component the file does not list, or
  the file lists one gestion no longer ships). The footer links it on every page.

### Changed

- `catalogo.yml` `manuals` accept nested pages (`<audience>/<dir>/<page>.md`).
- Vendored repo-docs re-rendered to canon after repo-docs #11 (no `Docs:` line in
  the PR gate) and #12 (the opt-in `site-structure` rule).

### Fixed

### Removed
