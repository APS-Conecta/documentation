# Changelog

All notable changes to `APS-Conecta/documentation` are recorded here.

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Catalogue rows for the fork apps (`side_menu`, `eurooffice`, `desktop_workspace`) and `totem`
  (instalador #51), with `desarrollo/` reference pages and `proyecto/novedades/` pages for the
  three shipped forks; `componentes.yml` now reads base images from the suite's containers and
  app versions from each app's own repo checkout.
- The «Idioma y registro» section of `desarrollo/documentation` (docs-SSOT D1): the org-wide
  Spanish/English split, its first statement of Conventional Commits, and the README shape every
  repo keeps.
- `tools/check-structure.py` (`make structure`): a stdlib port of the retired repo-docs
  `site-structure` rule, with tests; the `docs` workflow now runs it plus a range-scoped gitleaks
  scan (job-level `RANGE`).
- Store apps' Spanish UI strings (`spreed`, `calendar`, `contacts`, `groupfolders`, `notify_push`)
  fetched from their own upstream repositories into `_generated/apps/` (`fetch-upstream.sh`),
  replacing the retired gestion tarballs as the source `upstream-fidelity` swaps labels against.
- OSM-only basemap pages: `administracion/mapas-base` and its dependents describe the
  OpenStreetMap tile service directly and the retired PMTiles file (redo of the closed #190).
- gestion's `LICENSING.md` §3.2/§3.4 (OFL fonts, Geoportal coordinates), `WELCOME-SCREEN.md`
  (storage-folder rename, walls) and `ARCHITECTURE.md` access model merged into `licencias`,
  `intravox` and `usuarios-y-grupos`.

### Changed

- The tooling reads the suite repo (`instalador`) instead of the old gestion: `fetch-brand.sh`,
  `upstream.yml` (Nextcloud major from `Containers/nextcloud`), `gen-catalogo.py` (parity against
  `apps.json`, the single app manifest), `gen-componentes.py`, `build.yml` (`SUITE_SRC`).
- Site pages that linked gestion ADRs or docs repointed at the suite repo's renumbered ADRs or
  at this site (instalador #51); the wizard step renumbering and the retired `/tiles/` route
  followed the OSM basemap change through `aio`, `calidad`, `arquitectura`, `operaciones`.
- `.github/`: the vendored `repo-docs.py`, profiles, issue/PR templates, `CODEOWNERS` and canon
  markers removed (org defaults and this repo's own gates cover them).

- `desarrollo/apis/`: the APIs section (index plus five pages: Geoportal de Chile CSW and GeoServer, health/education/bomberos layers, administrative boundaries, FONASA and ciclovías, platform and internal REST). `Databases/APIs/catalog.yaml` stays the owner of each service's status.
- Catalogue row for `buscador-documental` (kind `app-in-design`: registered, not distributed with the suite, exempt from OWN_APPS parity and from the map scan) with three `esqueleto: borrador` placeholder pages (usuario, administracion/ia, desarrollo); `gen-catalogo.py` roster 16 → 17. The full Spanish drafts live in `APS-Conecta/buscador-documental`, `buscador/docs-site/`.
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
- The site design (scribe S2d): Furo with the APS palette and fonts through its CSS
  variables, light only (`_templates/base.html`), Spanish interface strings
  (`locales/es/LC_MESSAGES/sphinx.po`); Pagefind instant search in the sidebar with
  `audiencia` and `apps` filters from each page's front matter (`_ext/pagefind_meta.py`,
  `pagefind.yml`), built by `make html`; every page typed with `tipo`, `audiencia`,
  `apps` and `resumen` and opted into repo-docs `site-structure` (`.github/site-structure`),
  placeholders marked `esqueleto: borrador`; chapters the upstream map turns into folders
  moved to `<chapter>/index.md` with a glob toctree; `check-site.py` re-targeted (brand
  sidebar, light under a dark preference, no sideways scroll at 360 px, drawer, Pagefind
  query and filter).
- The AI disclosure (scribe S2e): `aviso.md` «Uso de inteligencia artificial» — how
  APS Conecta Gestión is built (vibe coding from Daniel Espinoza Charrier's idea,
  through rpiv, Claude Code multi-agent workflows, Claude routines, pi and Jules),
  a tools-and-models table generated from `ia.yml` by `tools/gen-ia.py`, what AI
  writes and what it does not, and how each change is reviewed. `tools/ia-check.py`
  and the weekly `ia-check` workflow fail when an APS-authored commit carries a
  Co-Authored-By model or a bot author `ia.yml` does not declare (12,018 commits
  scanned on 2026-10-09: 0 problems).

### Changed

- `tools/gen-catalogo.py` reads the `OWN_APPS` parity registry from `instalador` (`provisioning/phases/12-apps.sh`) instead of `gestion`, which is about to delete its frozen copy of the executor (gestion #245); the missing-registry error names the instalador path, and `--selftest` pins the lookup. `build.yml` needs no change: `instalador` is already a roster row, so it is cloned beside `gestion`. Prose in `tools/capturas/captura.py`, `desarrollo/documentation.md` and `desarrollo/repo-docs.md` follows.
- `tools/gen-inicio-rapido.py` pins (`--selftest`) re-verified against the live org (2026-10-18): six READMEs now carry the quickstart section (repo-docs, aps-common, Databases, epidemiologia, estadistica, farmacia); `instalador` replaces `rpiv-artifacts` among the repos without a root `README.md`.
- `README.md` status brought current (site built and published on Pages, four audience trees populated).
- APS-Conecta/AIO is gone from the catalogue (roster 15 → 14) and from the generators' pins; `desarrollo/aio.md`, `desarrollo/instalador.md` and `administracion/aio.md` now say the repository was deleted after instalador absorbed it, with its full commit history. The two `aio` pages stay: they document the fork, which instalador now holds.
- Theme: `sphinx_rtd_theme` → Furo (scribe Q22); `catalogo.yml` paths follow the
  chapter folders.
- `catalogo.yml` `manuals` accept nested pages (`<audience>/<dir>/<page>.md`).
- Vendored repo-docs re-rendered to canon after repo-docs #11 (no `Docs:` line in
  the PR gate) and #12 (the opt-in `site-structure` rule).

### Fixed

### Removed

- `proyecto/novedades/aio.md` (Scribe page of the deleted AIO repository).