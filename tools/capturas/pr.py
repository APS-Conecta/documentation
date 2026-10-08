#!/usr/bin/env python3
"""pr — open the weekly screenshots draft PR (Phase 11, capturas.yml).

Adapted from repo-docs' open_pr() (.github/repo-docs.py): refuses on a tree
dirty outside capturas/*.png, branches to the next free capturas/refresh-<n>,
commits the PNG paths add-only, pushes, opens a DRAFT PR with an accent-free
English title (title_is_english-safe: no accented characters, no Spanish
stopwords) and a body carrying the byte-stability table. Never force-pushes,
never merges, never touches the default branch.

The PR is App-authored (mint B in capturas.yml), NOT GITHUB_TOKEN-authored,
precisely so the canon docs.yml pr-gate runs on it — GITHUB_TOKEN-originated
events trigger no workflows. PNG-only paths owe no `Docs:` trailer: the gate's
docs_line_paths watch l10n/, src/, templates/, appinfo/, lib/Command/,
lib/Settings/ — no capturas/ path matches.

Env: GH_TOKEN (mint B). The push authenticates via a one-shot git credential
helper reading $GH_TOKEN from the environment — the token never reaches argv,
URL, or a config file. Exit: 0 = PR opened or nothing to open; 1 = any git/gh
failure or an unrelated dirty tree.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PREFIX = "capturas/refresh-"
PNG = re.compile(r"^capturas/[^/]+\.png$")

BOT_NAME = "aps-pi[bot]"
BOT_EMAIL = "aps-pi[bot]@users.noreply.github.com"


def sh(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def porcelain() -> list:
    r = sh(["git", "-C", str(REPO), "status", "--porcelain"])
    return [ln for ln in r.stdout.split("\n") if ln.strip()]


def path_of(line: str) -> str:
    """Porcelain lines are 'XY path'; split on whitespace — the file is the
    tail (repo-docs _porcelain_path: stdout may arrive as 'M file', a fixed
    column slice silently truncates the filename)."""
    parts = line.split(None, 1)
    return (parts[1] if len(parts) > 1 else parts[0]).strip().strip('"')


def default_branch() -> str:
    r = sh(["git", "-C", str(REPO), "symbolic-ref", "--short",
            "refs/remotes/origin/HEAD"])
    ref = r.stdout.strip()
    return ref[len("origin/"):] if ref.startswith("origin/") else "main"


def next_free_branch() -> str:
    """open_pr scanned local branches only; on an ephemeral runner the REMOTE
    list is the one that persists week to week, so both are scanned."""
    used = set()
    r = sh(["git", "-C", str(REPO), "branch", "--list", f"{PREFIX}*"])
    used |= {int(m.group(1)) for ln in r.stdout.splitlines()
             if (m := re.search(r"(\d+)$", ln.strip()))}
    r = sh(["git", "-C", str(REPO), "ls-remote", "--heads", "origin"])
    used |= {int(m.group(1)) for ln in r.stdout.splitlines()
             if (m := re.search(r"refs/heads/capturas/refresh-(\d+)$", ln))}
    n = 1
    while n in used:
        n += 1
    return f"{PREFIX}{n}"


def byte_table(pngs: list) -> str:
    """The same table captura.py printed — rebuilt here so the PR body is
    self-contained evidence of what changed and by how much."""
    lines = ["| png | old B | new B | delta | equal? |", "|---|---:|---:|---:|---|"]
    for rel in pngs:
        png = REPO / rel
        new = png.read_bytes()
        p = subprocess.run(["git", "-C", str(REPO), "show", f"HEAD:{rel}"],
                           capture_output=True)
        old = p.stdout if p.returncode == 0 and p.stdout else None
        old_s = "new" if old is None else str(len(old))
        delta = "-" if old is None else f"{len(new) - len(old):+d}"
        equal = "yes" if (old is not None and old == new) else "NO"
        lines.append(f"| `{Path(rel).name}` | {old_s} | {len(new)} | {delta} | {equal} |")
    return "\n".join(lines)


def main() -> None:
    changed = [path_of(ln) for ln in porcelain()]
    stray = [p for p in changed if not PNG.match(p)]
    if stray:
        fail("refused: working tree has unrelated changes —\n  "
             + "\n  ".join(stray[:8]) + "\ncommit or stash them first")
    pngs = [p for p in changed if PNG.match(p)]
    if not pngs:
        print("nothing to open a PR for")
        return

    k = len(pngs)
    title = f"capturas: refresh {k} screenshot" + ("s" if k != 1 else "")
    branch = next_free_branch()
    body = (f"### capturas — byte stability\n\n{byte_table(pngs)}\n\n"
            "Rerun: **Actions → capturas → Run workflow** (`workflow_dispatch`), or wait "
            "for the weekly Monday 04:17 UTC run. Byte-equality is the default gate; "
            "`--compare sizeclass` is the pre-built fallback.\n\n"
            "Draft: screenshots need a human look before merge. No `Docs:` trailer — "
            "PNG-only paths are pr-gate-exempt.")

    for label, argv in (
        ("checkout", ["git", "-C", str(REPO), "checkout", "-q", "-b", branch]),
        ("add", ["git", "-C", str(REPO), "add", "--", *pngs]),
        ("commit", ["git", "-C", str(REPO), "-c", f"user.name={BOT_NAME}", "-c",
                    f"user.email={BOT_EMAIL}", "commit", "-qm",
                    f"{title}\n\nGenerated by capturas.yml; byte-diff guarded."]),
        ("push", ["git", "-C", str(REPO),
                  "-c", "credential.helper=",
                  "-c", "credential.helper=!f() { echo username=x-access-token; "
                        "echo password=$GH_TOKEN; }; f",
                  "push", "-q", "-u", "origin", branch]),
    ):
        r = sh(argv)
        if r.returncode != 0:
            fail(f"failed at git {label}: {r.stderr.strip()[:300]}")

    r = sh(["gh", "pr", "create", "--draft", "--repo", "APS-Conecta/documentation",
            "--head", branch, "--base", default_branch(), "--title", title,
            "--body", body])
    if r.returncode != 0:
        fail(f"branch pushed, PR not created: {r.stderr.strip()[:300]}")
    print(r.stdout.strip())


if __name__ == "__main__":
    main()
