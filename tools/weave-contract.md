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

## 3. The block body

| Upstream | In the block |
|---|---|
| Prose | Spanish. Meaning complete and exact: no additions, omissions or summaries. |
| A paragraph listed under «Official Spanish» | That `msgstr`, word for word. Only whitespace may change. |
| Register | The official strings use «usted»; on a page that has them, match it. Otherwise use neutral, direct Spanish (impersonal or infinitive). |
| Section titles | Spanish. Same count, order and relative depth as upstream. The body's first level is `###` on a single-document page. |
| `.. _label:` | `(nc-label)=` on its own line, right before the heading it labels (label lower-case, verbatim). |
| `:doc:\`x\`` / `:ref:\`x\`` | `{nc-doc}\`<absolute docname>\`` / `{nc-ref}\`<label>\``, with Spanish link text when upstream gives text: `{nc-ref}\`Texto <label>\``. |
| External link `` `text <url>`_ `` | `[texto](url)`, URL byte-identical. |
| `.. code-block:: lang`, `.. code::`, `::` literal blocks | A plain fence: ```` ```lang ```` (or ```` ``` ````). Content byte-identical: commands, paths, config keys, output, comments inside code. A `:caption:` becomes a sentence before the fence. |
| ``` ``literal`` ``` | `` `literal` ``, byte-identical. |
| `:guilabel:`, `:menuselection:` | `{guilabel}`, with the Spanish UI label from `glosario.yml` or the app's own Spanish strings. |
| `:file:`, `:command:`, `:kbd:` | The same role, content verbatim. |
| `.. note::` / `warning` / `tip` / `important` / `hint` / `danger` / `seealso` | `:::{note}` … `:::` (same kind, colon fence), translated. No headings inside. |
| Tables (`list-table`, grid, simple) | A Markdown pipe table, or `:::{list-table}`. Cells translated, literals verbatim. |
| `.. figure::`, `.. image::` | Dropped; they show the Nextcloud logo. A figure caption that carries information becomes a sentence. |
| `.. toctree::` | Dropped: the site's own toctree lists the pages. |
| `|version|` and other substitutions | The resolved value (the suite's major, e.g. `34`). |
| `.. include::`, `.. literalinclude::`, anything else unknown | Do not guess. Name it under **gaps** in your result. |
| The word «Nextcloud» | Keep it exactly as upstream writes it. The build renames it site-wide; never rename by hand. |

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
