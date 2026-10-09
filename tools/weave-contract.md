# Weave contract — translating and weaving one upstream Nextcloud document

The rules every weave agent follows: the bulk-weave workflow (scribe W-runs) and the 📚 Scribe
`upstream` lane. Deterministic gates enforce what they can (`tools/upstream-fidelity.py`,
repo-docs `site-structure` and `doc-language-es`, `sphinx-build -W`, `tools/rebrand-check.py`);
the reviewer agent checks the rest.

## 1. Inputs

`python3 tools/weave.py brief <docname>` prints the upstream body at the pinned SHA, the exact
block opening line, the target page, whether `:difiere:` is required, the official Spanish
paragraphs to reuse, and the current target page if it exists. Work only from the brief and the
files it names.

## 2. Page shape

A **new** page:

`````markdown
---
tipo: guia | referencia | explicacion | tutorial
esqueleto: plataforma
audiencia: usuario | administracion | desarrollo
apps: [gestion]
resumen: "≤ 158 characters, Spanish, what the page covers"
---
# <the upstream title, in Spanish>

## Resumen

<One to three sentences: what this page covers and for whom. Say nothing about APS Conecta
Gestión beyond what the :difiere: notice points to.>

````{upstream} <docname>.rst@<sha>
:difiere: <page>          ← only when the brief says it is required
<the translated body>
````
`````

- `tipo` follows Diátaxis: a how-to is `guia`, a learning walk-through `tutorial`, settings and
  commands `referencia`, background `explicacion`.
- A folder `index.md` ends with the toctree block the brief gives.
- An **existing** page keeps its front matter and its APS sections. The block goes at the end,
  before any toctree.
- A page holding **several** documents gives each one a `### <title in Spanish>` heading right
  before its block. Inside each block the body starts one level lower (`####`).
- A page whose blocks carry `:difiere:` gets its «En APS Conecta Gestión» section from the
  orchestrator, written from cited code evidence. A translator never writes it.

## 3. The block body

| Upstream | In the block |
|---|---|
| Prose | Spanish. Meaning complete and exact: no additions, omissions or summaries. |
| A paragraph or section title listed under «Official Spanish» | That `msgstr`, word for word, literals included: where the `msgstr` translates a literal (``` ``Files`` ``` → ``` ``Archivos`` ```), the `msgstr` wins. Only whitespace may change. |
| Register | The official strings use «usted»; on a page that has them, match it. Otherwise use neutral, direct Spanish (impersonal or infinitive). |
| Administration and developer prose | No official Spanish exists: translate every paragraph, in neutral impersonal Spanish. UI labels are the shipped interface's Spanish (`{guilabel}`, backed by the catalog the gate reads). |
| Section titles | Spanish. Same count, order and relative depth as upstream. The body's first level is `###` on a single-document page. |
| `.. _label:` | `(nc-label)=` on its own line, right before the heading it labels (label lower-case, verbatim). |
| `:doc:\`x\`` / `:ref:\`x\`` | `{nc-doc}\`<absolute docname>\`` / `{nc-ref}\`<label>\``, with Spanish link text when upstream gives text: `{nc-ref}\`Texto <label>\``. A bare `:doc:` stays bare: the build writes the target's Spanish title. |
| External link `` `text <url>`_ `` | A Markdown link (Spanish text, same URL), URL byte-identical. |
| Named reference `` `Name`_ `` with its `.. _Name: url` target | A reference link `[texto][Name]`, with `[Name]: url` at the end of the block. URL byte-identical. |
| A bare URL in prose or in a table cell | An autolink `<url>`, byte-identical: the site has no linkify, so a bare URL renders as plain text (the gate rejects it). |
| A URL template with placeholders (`http://[user@pass:]<server>:<port>`) | As upstream formats it, never an autolink: it names an argument's shape, not a page. |
| A link that is dead or slow upstream (404, 403, rate-limited) | Byte-identical all the same; name it under **gaps** when it is dead. linkcheck skips URLs that appear only inside `{upstream}` blocks: keeping them alive is upstream's job. |
| Single-backtick text with no role (`` `text` ``: RST's default role) | `*text*`. Upstream renders it in italics. |
| A definition list | Bullets `- term: definition`, with the term formatted as upstream formats it. |
| An English-only message upstream quotes (an error or UI string with no Spanish version) | Verbatim, inside «…», with no gloss. The English check skips quoted text. |
| `.. raw:: html` | Dropped. Name it under **gaps** with what it carried. |
| An upstream defect: a pointer with no target («see here» linking nothing), a name the steps contradict («Introduction» vs «Introductions») | As upstream writes it, and named under **gaps** with the upstream line. Repairing upstream's meaning belongs in an upstream PR; a silent repair breaks the next `upstream` lane diff. |
| An official msgstr that drops meaning or reads wrong («A random 15-digit token» without «random») | Verbatim all the same (Q20), and named under **gaps** with the upstream English, so it can be fixed in Transifex. |
| `.. raw:: html` that wraps RST content (`<details><summary>Android</summary>` … `</details>`) | The summary becomes a bold line (`**Android**`) before the content it scopes; the tags are dropped. |
| `.. versionadded::`, `versionchanged`, `deprecated`, `versionremoved` | The same MyST directive in a colon fence (`:::{versionadded} 29` … `:::`), its text translated. The site translates the label («Nuevo en la versión 29»). |
| A code block inside a list item | The fence indented with the item's text, so the list keeps its numbering; the gate reads the body without that indent. |
| `.. code-block:: lang`, `.. code::`, `::` literal blocks | A plain fence: ```` ```lang ```` (or ```` ``` ````). Content byte-identical: commands, paths, config keys, output, comments inside code. A `:caption:` becomes a sentence before the fence. |
| ``` ``literal`` ``` | `` `literal` ``, byte-identical. |
| A ``` ``literal`` ``` that is a UI label (a button, menu item or setting, or a path `Settings -> General`) | `{guilabel}` with the Spanish the interface shows, one per step: `{guilabel}`Ajustes` → {guilabel}`General``. The gate accepts the swap only when the shipped app's `l10n/es.json` or `glosario.yml` backs it, and warns on a literal it could swap. With no Spanish string, keep the literal. |
| A UI string upstream quotes ("Start recording") | The interface's Spanish in «…» («Empezar a grabar»); the gate rejects the English when the catalog has the Spanish. With no Spanish string, the English verbatim in «…». |
| A UI string of other software (WinSCP, Finder, Thunderbird; docs in `upstream.yml` `ui_third_party`) | Verbatim in «…»: it is that program's label, not Nextcloud's. |
| `:guilabel:`, `:menuselection:` | `{guilabel}`, with the Spanish UI label from `glosario.yml` or the app's own Spanish strings. |
| `:file:`, `:command:`, `:kbd:` | The same role, content verbatim. |
| `.. note::` / `warning` / `tip` / `important` / `hint` / `danger` / `seealso` | `:::{note}` … `:::` (same kind, colon fence), translated. No headings inside. |
| Tables (`list-table`, grid, simple) | A Markdown pipe table, or `:::{list-table}`. Cells translated, literals verbatim. |
| `.. figure::`, `.. image::` | Dropped; they show the Nextcloud logo. A caption that carries information becomes a sentence. When the text around the image points at it («this page», «here», «below», «as shown»), its caption or alt text becomes one short sentence saying what the screen shows, so the pointer still lands. An image with no alt text and no caption gives nothing to say: the lead-in just ends in «.». |
| `.. toctree::` | A bullet list of bare `{nc-doc}` links, one per entry, in upstream order: ``- {nc-doc}`user_manual/talk/call` ``. Upstream renders a toctree as that list on the page; the build writes each target's Spanish title once it is woven (the brief lists the entries). A `:hidden:` toctree shows nothing upstream: drop it. |
| `|version|` and other substitutions | The resolved value (the suite's major, e.g. `34`). |
| `.. include::`, `.. literalinclude::`, anything else unknown | Do not guess. Name it under **gaps** in your result. |
| The word «Nextcloud» | Keep it exactly as upstream writes it. The build renames it site-wide; never rename by hand. |
| «Nextcloud» as the **vendor**: the subject that publishes, maintains or offers something («Nextcloud ofrece oficialmente…», «no Nextcloud», «el equipo de Nextcloud») | `{vendor}`Nextcloud``. The rename keeps the name, so the page never claims APS publishes Nextcloud's software. Link text into nextcloud.com or github.com/nextcloud keeps the name by itself. |

**Fences.** Inside a block, backtick fences are for code only. Every directive (admonitions,
`list-table`, …) uses a colon fence, `:::{name}` … `:::`, so a code fence inside it can never close
the 4-backtick `{upstream}` block.

## 4. Checks before you finish

Run these in the worktree you were given, and fix until they pass:

```bash
python3 tools/upstream-fidelity.py <every page you wrote>
python3 .github/repo-docs.py check . --offline
sphinx-build -q -W --keep-going -b html . _build/html
```

`make html` already ran once in the worktree, so `_generated/` exists. Do not run `make` again.

## 5. The reviewer

The reviewer reads each block against its upstream source and returns findings only; it never
edits. It looks for:

- meaning drift: anything added, omitted, softened or changed in a technical sense;
- a wrong or untranslated paragraph, wrong register, or a UI term that contradicts `glosario.yml`;
- a hand rename of «Nextcloud», or a lost `:difiere:`;
- a `resumen` or `Resumen` that claims more than the page says;
- anything the deterministic gates cannot see.

Each finding names the page, the line and the exact fix.
