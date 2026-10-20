#!/usr/bin/env python3
"""ia-check — no AI writes in the organisation's repositories without being declared in ia.yml.

Walks the history after CUTOFF of every catalog repo cloned under APS_ORG_ROOT and keeps only commits
authored by an APS identity (`identities`), so the upstream history of the forks is out of scope.
On those commits it fails when:

  - a Co-Authored-By trailer names someone that is neither a declared model (`tools[].models`),
    a declared bot (`tools[].bots`), a person (`people`) nor deterministic automation;
  - the author is a bot that is neither a declared AI bot nor deterministic automation.

The ia-check workflow runs it on demand; a new model therefore shows up as a red job,
and the fix is one ia.yml line. AI use that leaves no trailer is invisible here — ia.yml, declared
by a person, stays the source.

    python3 tools/ia-check.py            # the catalog repos under APS_ORG_ROOT
    python3 tools/ia-check.py --selftest
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CUTOFF = "2026-10-20"  # earlier history is not checked
FMT = "%an%x1f%(trailers:key=Co-Authored-By,valueonly,separator=%x1e)%x1d"


def commits(repo: Path) -> list[tuple[str, list[str]]]:
    out = subprocess.run(["git", "-C", str(repo), "log", "--all", f"--since={CUTOFF}", f"--format={FMT}"],
                         capture_output=True, text=True, check=True).stdout
    rows = []
    for rec in out.split("\x1d"):
        rec = rec.strip("\n")
        if not rec:
            continue
        author, _, trailers = rec.partition("\x1f")
        names = [re.sub(r"\s*<.*", "", t).strip() for t in trailers.split("\x1e")]
        rows.append((author, [n for n in names if n]))
    return rows


def problems(repo_name: str, rows: list[tuple[str, list[str]]], doc: dict) -> list[str]:
    ids = set(doc["identities"])
    models = {m for t in doc["tools"] for m in t["models"]}
    bots = {b for t in doc["tools"] for b in t.get("bots", ())}
    known = models | bots | set(doc["people"]) | set(doc["automation"])
    out = set()
    for author, names in rows:
        if author not in ids:
            continue
        if author.endswith("[bot]") and author not in bots | set(doc["automation"]):
            out.add(f"{repo_name}: bot author {author!r} is not declared in ia.yml")
        out |= {f"{repo_name}: co-author {n!r} is not declared in ia.yml" for n in names if n not in known}
    return sorted(out)


def main() -> int:
    doc = yaml.safe_load((ROOT / "ia.yml").read_text(encoding="utf-8"))
    catalog = yaml.safe_load((ROOT / "catalogo.yml").read_text(encoding="utf-8"))["repos"]
    org = Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))
    found, scanned = [], 0
    for row in catalog:
        repo = org / row["repo"]
        if not (repo / ".git").exists():
            found.append(f"{row['repo']}: not cloned under {org} — the check cannot vouch for it")
            continue
        if (repo / ".git" / "shallow").exists():
            found.append(f"{row['repo']}: shallow clone — clone with full history")
            continue
        rows = commits(repo)
        scanned += len(rows)
        found += problems(row["repo"], rows, doc)
    for f in found:
        print(f"ERROR {f}")
    print(f"[ia-check] {scanned} commits in {len(catalog)} repos; {len(found)} problem(s)")
    return 1 if found else 0


def selftest() -> int:
    doc = {"identities": ["Dani", "bot-x[bot]", "dependabot[bot]", "ghost[bot]"],
           "people": ["ddespinoza"], "automation": ["dependabot[bot]"],
           "tools": [{"models": ["Claude Opus 5.5"]}, {"models": ["x"], "bots": ["bot-x[bot]"]}]}
    ok = [("Dani", ["Claude Opus 5.5", "ddespinoza"]), ("bot-x[bot]", []),
          ("dependabot[bot]", []), ("Upstream Dev", ["Claude Opus 4.6"])]
    assert problems("r", ok, doc) == [], problems("r", ok, doc)
    assert problems("r", [("Dani", ["Claude Opus 9"])], doc) == ["r: co-author 'Claude Opus 9' is not declared in ia.yml"]
    assert problems("r", [("ghost[bot]", [])], doc) == ["r: bot author 'ghost[bot]' is not declared in ia.yml"]
    with tempfile.TemporaryDirectory() as tmp:
        def commit(msg: str, date: str) -> None:
            env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
            subprocess.run(["git", "-C", tmp, "-c", "user.name=Dani", "-c", "user.email=d@x", "commit",
                            "--allow-empty", "-q", "-m", msg], check=True, env=env)
        subprocess.run(["git", "init", "-q", tmp], check=True)
        commit("old\n\nCo-Authored-By: Old Model <o@x>", "2026-10-01T12:00:00Z")
        commit("new\n\nCo-Authored-By: Claude Opus 5.5 <c@x>", "2026-10-21T12:00:00Z")
        assert commits(Path(tmp)) == [("Dani", ["Claude Opus 5.5"])], commits(Path(tmp))
    print("[ia-check] selftest OK (declared pass, unlisted model fails, unlisted bot fails, upstream and pre-cutoff ignored)")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
