#!/usr/bin/env python3
"""gen-componentes — the components table of the legal notice, and the drift gate behind it.

componentes.yml declares what only a person knows (origin, SPDX licence, what APS changes). This
script adds what the code knows, at build time, from the sibling clones under APS_ORG_ROOT:

  version    image tag + digest (gestion compose.yaml); app version (gestion provisioning/apps/<id>/VENDOR)
  modified   a vendored app with .patch files beside it is modified; the AIO fork's patch queue length
  drift      every compose image, every vendored app and every distribution-fork catalog row has a
             row here, and every row here is still shipped — otherwise the build fails

Writes _generated/componentes.md, which aviso.md includes. Never committed.

    python3 tools/gen-componentes.py [--selftest]
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"image", "app", "own-app", "fork", "asset", "data"}
IMAGE_RE = re.compile(
    r"^\s*image:\s*([^\s:@]+(?:/[^\s:@]+)*):([^\s@]+)@sha256:([0-9a-f]{64})", re.M
)


def org() -> Path:
    return Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))


def fail(msg: str) -> None:
    sys.exit(f"[gen-componentes] ERROR: {msg}")


def images(compose: str) -> dict[str, str]:
    return {
        name: f"{tag} (`{digest[:12]}`)"
        for name, tag, digest in IMAGE_RE.findall(compose)
    }


def vendored(apps_dir: Path) -> dict[str, dict]:
    out = {}
    for d in sorted(p for p in apps_dir.iterdir() if p.is_dir()):
        vendor = (
            (d / "VENDOR").read_text(encoding="utf-8")
            if (d / "VENDOR").exists()
            else ""
        )
        m = re.search(r"^version=(\S+)$", vendor, re.M)
        out[d.name] = {
            "version": m.group(1) if m else "",
            "patches": len(list(d.glob("*.patch"))),
        }
    return out


def fork_patches(repo: Path) -> int:
    queue = repo / "patches"
    return (
        len([p for p in queue.iterdir() if p.suffix in (".patch", ".sh")])
        if queue.is_dir()
        else 0
    )


def drift(rows: list[dict], imgs: dict, apps: dict, forks: set[str]) -> list[str]:
    out = []
    by_kind = lambda *k: {r["id"] for r in rows if r["kind"] in k}  # noqa: E731
    for label, shipped, declared in (
        ("compose image", set(imgs), by_kind("image")),
        ("vendored app", set(apps), by_kind("app", "own-app")),
        ("distribution fork", forks, by_kind("fork")),
    ):
        out += [
            f"{label} {x} ships but has no componentes.yml row"
            for x in sorted(shipped - declared)
        ]
        out += [
            f"componentes.yml lists {label} {x}, which no longer ships"
            for x in sorted(declared - shipped)
        ]
    return out


def resolve(rows: list[dict], imgs: dict, apps: dict, aio_patches: int) -> list[dict]:
    out = []
    for r in rows:
        if r["kind"] not in KINDS:
            fail(f"{r['name']}: kind {r['kind']!r} is not one of {sorted(KINDS)}")
        row = dict(r)
        if r["kind"] == "image":
            row["version"], row["modified"] = imgs[r["id"]], "No"
        elif r["kind"] in ("app", "own-app"):
            a = apps[r["id"]]
            row["version"] = a["version"]
            if r["kind"] == "own-app":
                row["modified"] = "Fork propio" if r.get("fork") else "Propio"
            else:
                row["modified"] = (
                    f"Sí ({a['patches']} parches)" if a["patches"] else "No"
                )
            if r["kind"] == "app" and bool(a["patches"]) != bool(r.get("changes")):
                fail(
                    f"{r['name']}: {a['patches']} patch(es) beside the tarball but "
                    f"{'no' if a['patches'] else 'a'} `changes` line — declare what APS changes, or drop it"
                )
        elif r["kind"] == "fork":
            row["version"] = f"cola de {aio_patches} parches"
            row["modified"] = "Sí"
        else:
            row["version"] = r.get("version", "—")
            row["modified"] = "Sí" if r.get("changes") else "No"
        out.append(row)
    return out


def render(rows: list[dict]) -> str:
    def cell(t: str) -> str:
        return str(t).replace("|", "\\|")

    lines = [
        "| Componente | Origen | Versión | Licencia | Modificado | Qué cambia APS |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        origin = f"[{r['upstream'].split('//', 1)[-1].rstrip('/')}]({r['upstream']})"
        if r.get("fork"):
            origin += f" · fork: [{r['fork'].split('github.com/', 1)[-1]}]({r['fork']})"
        changes = r.get("changes", "") or "—"
        if r.get("note"):
            changes = f"{changes} {r['note']}" if changes != "—" else r["note"]
        lines.append(
            f"| {cell(r['name'])} | {origin} | {cell(r['version'])} | `{r['licence']}` "
            f"| {r['modified']} | {cell(changes)} |"
        )
    return "\n".join(lines) + "\n"


def gather():
    rows = yaml.safe_load((ROOT / "componentes.yml").read_text(encoding="utf-8"))[
        "components"
    ]
    gestion = org() / "gestion"
    imgs = images((gestion / "compose.yaml").read_text(encoding="utf-8"))
    apps = vendored(gestion / "provisioning" / "apps")
    catalog = yaml.safe_load((ROOT / "catalogo.yml").read_text(encoding="utf-8"))[
        "repos"
    ]
    forks = {r["repo"] for r in catalog if r["kind"] == "distribution-fork"}
    return rows, imgs, apps, forks


def main() -> int:
    rows, imgs, apps, forks = gather()
    problems = drift(rows, imgs, apps, forks)
    if problems:
        fail("components drift:\n  " + "\n  ".join(problems))
    table = render(resolve(rows, imgs, apps, fork_patches(org() / "AIO")))
    out = ROOT / "_generated" / "componentes.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(table, encoding="utf-8")
    print(f"[gen-componentes] {len(rows)} componentes → {out.relative_to(ROOT)}")
    return 0


def selftest() -> int:
    rows = [
        {
            "name": "S",
            "kind": "image",
            "id": "nextcloud",
            "upstream": "https://x",
            "licence": "AGPL-3.0-or-later",
        },
        {
            "name": "A",
            "kind": "app",
            "id": "calendar",
            "upstream": "https://x",
            "licence": "AGPL-3.0-or-later",
        },
        {
            "name": "P",
            "kind": "app",
            "id": "eurooffice",
            "upstream": "https://x",
            "licence": "AGPL-3.0-only",
            "changes": "Nombre.",
        },
    ]
    imgs = {"nextcloud": "34-apache (`c8aff72362db`)"}
    apps = {
        "calendar": {"version": "6.5.4", "patches": 0},
        "eurooffice": {"version": "11.0.5", "patches": 2},
    }
    assert drift(rows, imgs, apps, set()) == []
    assert drift(rows, dict(imgs, redis="8"), apps, set()) == [
        "compose image redis ships but has no componentes.yml row"
    ]
    assert drift(rows[1:], imgs, apps, set()) == ["compose image nextcloud ships but has no componentes.yml row"]
    gone = rows + [{"name": "G", "kind": "image", "id": "gone", "upstream": "https://x", "licence": "MIT"}]
    assert drift(gone, imgs, apps, set()) == ["componentes.yml lists compose image gone, which no longer ships"]
    assert drift(rows, imgs, apps, {"AIO"}) == [
        "distribution fork AIO ships but has no componentes.yml row"
    ]
    res = resolve(rows, imgs, apps, 31)
    assert [r["modified"] for r in res] == ["No", "No", "Sí (2 parches)"], res
    assert (
        "| P | [x](https://x) | 11.0.5 | `AGPL-3.0-only` | Sí (2 parches) | Nombre. |"
        in render(res)
    )
    try:
        resolve([dict(rows[2], changes="")], imgs, apps, 31)
        raise AssertionError("a patched app without `changes` must fail")
    except SystemExit:
        pass
    assert images("  image: redis:8-alpine@sha256:" + "a" * 64) == {
        "redis": "8-alpine (`aaaaaaaaaaaa`)"
    }
    print(
        "[gen-componentes] selftest OK (drift both ways, patches ⇒ modified, changes required, render)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
