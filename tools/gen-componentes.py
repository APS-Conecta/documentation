#!/usr/bin/env python3
"""gen-componentes — the components table of the legal notice, and the drift gate behind it.

componentes.yml declares what only a person knows (origin, SPDX licence, what APS changes). This
script adds what the code knows, at build time, from the suite checkout under APS_ORG_ROOT
(APS-Conecta/gestion — the suite repository, renamed from instalador at the cutover):

  version    app release version (the roster checkout of the app's own repo); "—" for store apps,
             whose version the installer resolves at install time; image tag (the FROM base of the
             suite image, or the server ENV for the Nextcloud row)
  drift      every app of the suite manifest (apps.json), every base image of the suite's shipped
             containers (php/containers.json → Containers/<name>/Dockerfile) and every
             distribution-fork catalog row has a row here, and every row here is still shipped —
             otherwise the build fails

Writes _generated/componentes.md, which aviso.md includes. Never committed.

    python3 tools/gen-componentes.py [--selftest]
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"image", "app", "own-app", "fork", "asset", "data"}
FROM_RE = re.compile(r"^FROM\s+(\S+)", re.M)
NC_ENV_RE = re.compile(r"^ENV NEXTCLOUD_VERSION=(\S+)", re.M)


def org() -> Path:
    return Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))


def fail(msg: str) -> None:
    sys.exit(f"[gen-componentes] ERROR: {msg}")


def shipped_images(containers_json: str) -> set[str]:
    """The suite container names (php/containers.json): aio-<name> images built from Containers/."""
    return {
        str(c["image"]).rsplit("/", 1)[-1].removeprefix("aio-")
        for c in json.loads(containers_json)["aio_services_v1"]
    }


def base_images(containers_dir: Path, shipped: set[str]) -> dict[str, str]:
    """image name → tag, from the FROM bases of the shipped containers' Dockerfiles."""
    out: dict[str, str] = {}
    for d in sorted(containers_dir.iterdir()):
        if d.name not in shipped or not (d / "Dockerfile").is_file():
            continue
        for m in FROM_RE.finditer((d / "Dockerfile").read_text(encoding="utf-8")):
            ref = m.group(1)
            if ref == "scratch":
                continue
            name, _, tag = ref.rpartition(":")
            if not tag or "/" in tag:  # no tag or a registry port: latest
                name, tag = ref, "latest"
            out.setdefault(name, tag)
    return out


def nc_server_version(nextcloud_dockerfile: str) -> str:
    m = NC_ENV_RE.search(nextcloud_dockerfile)
    return m.group(1) if m else ""


def manifest_apps(apps_json: str) -> set[str]:
    """The app ids of the suite manifest (apps.json): the one list of apps the suite installs."""
    return {r["id"] for r in json.loads(apps_json)}


def drift(rows: list[dict], imgs: dict, apps: set, forks: set[str]) -> list[str]:
    out = []
    by_kind = lambda *k: {r["id"] for r in rows if r["kind"] in k}  # noqa: E731
    for label, shipped, declared in (
        ("manifest app", set(apps), by_kind("app", "own-app")),
        ("base image", set(imgs), by_kind("image") - {"nextcloud"}),
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


def resolve(rows: list[dict], imgs: dict, nc_version: str, app_versions: dict) -> list[dict]:
    out = []
    for r in rows:
        if r["kind"] not in KINDS:
            fail(f"{r['name']}: kind {r['kind']!r} is not one of {sorted(KINDS)}")
        row = dict(r)
        if r["kind"] == "image":
            row["version"] = nc_version if r["id"] == "nextcloud" else imgs[r["id"]]
            row["modified"] = "No"
        elif r["kind"] in ("app", "own-app"):
            row["version"] = app_versions.get(r["id"], "—")
            if r["kind"] == "own-app":
                row["modified"] = "Fork propio" if r.get("fork") else "Propio"
            else:
                row["modified"] = "Sí" if r.get("changes") else "No"
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


def _json_version(repo_dir: Path, name: str) -> str:
    path = repo_dir / name
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(f"{repo_dir.name}: {name} ilegal: {exc}")
    return str(data.get("version") or "").strip()


def app_versions(rows: list[dict], catalog_rows: list[dict]) -> dict[str, str]:
    """id → release version, read from the app's own repo among the catalog roster; store apps
    without a roster row resolve at install time and print «—»."""
    roster = {r["repo"].lower(): r["repo"] for r in catalog_rows}
    out = {}
    import xml.etree.ElementTree as ET
    for r in rows:
        if r["kind"] not in ("app", "own-app"):
            continue
        repo = roster.get(r["id"].lower())
        if repo is None:
            continue
        repo_dir = org() / repo
        if not repo_dir.is_dir():
            fail(f"checkout ausente para versionar {r['id']}: {repo_dir}")
        info = repo_dir / "appinfo" / "info.xml"
        if info.is_file():
            try:
                root = ET.parse(info).getroot()
            except ET.ParseError as exc:
                fail(f"{repo}: info.xml ilegal: {exc}")
            out[r["id"]] = (root.findtext("version") or "").strip()
        for probe in ("composer.json", "package.json"):
            if not out.get(r["id"]) and (repo_dir / probe).is_file():
                out[r["id"]] = _json_version(repo_dir, probe)
    return out


def gather():
    rows = yaml.safe_load((ROOT / "componentes.yml").read_text(encoding="utf-8"))[
        "components"
    ]
    suite = org() / "gestion"
    if not suite.is_dir():
        fail(f"checkout de gestion ausente: {suite} (clonar la nómina bajo APS_ORG_ROOT)")
    shipped = shipped_images((suite / "php" / "containers.json").read_text(encoding="utf-8"))
    imgs = base_images(suite / "Containers", shipped)
    nc_version = nc_server_version(
        (suite / "Containers" / "nextcloud" / "Dockerfile").read_text(encoding="utf-8"))
    apps = manifest_apps((suite / "apps.json").read_text(encoding="utf-8"))
    catalog_rows = yaml.safe_load((ROOT / "catalogo.yml").read_text(encoding="utf-8"))[
        "repos"
    ]
    forks = {
        r["repo"] for r in catalog_rows
        if r["kind"] == "distribution-fork"
        # An absorbed fork no longer ships: its catalogue status is the record of the
        # transfer (AIO → the suite repository), not a second patch queue to track.
        and not str(r.get("status", "")).startswith("Absorbido")
    }
    return rows, imgs, nc_version, apps, forks, catalog_rows


def main() -> int:
    rows, imgs, nc_version, apps, forks, catalog_rows = gather()
    problems = drift(rows, imgs, apps, forks)
    if problems:
        fail("components drift:\n  " + "\n  ".join(problems))
    versions = app_versions(rows, catalog_rows)
    table = render(resolve(rows, imgs, nc_version, versions))
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
            "name": "R",
            "kind": "image",
            "id": "redis",
            "upstream": "https://x",
            "licence": "AGPL-3.0-or-later",
        },
        {
            "name": "B",
            "kind": "image",
            "id": "php",
            "upstream": "https://x",
            "licence": "PHP-3.01",
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
    imgs = {"redis": "8.10.2-alpine", "php": "8.4.26-fpm-alpine3.24"}
    apps = {"calendar", "eurooffice"}
    assert drift(rows, imgs, apps, set()) == []
    assert drift(rows, dict(imgs, redis="x"), apps, set()) == []  # the tag does not gate drift
    assert drift(rows, {k: v for k, v in imgs.items() if k != "php"}, apps, set()) == [
        "componentes.yml lists base image php, which no longer ships"
    ]
    assert drift(rows, imgs, apps - {"calendar"}, set()) == [
        "componentes.yml lists manifest app calendar, which no longer ships"
    ]
    assert drift(rows, imgs, apps | {"totem"}, set()) == [
        "manifest app totem ships but has no componentes.yml row"
    ]
    assert drift(rows[1:], imgs, apps, set()) == []  # the nextcloud row reads the ENV, not drift
    gone = rows + [{"name": "G", "kind": "image", "id": "gone", "upstream": "https://x", "licence": "MIT"}]
    assert drift(gone, dict(imgs, php="x"), apps, set()) == [
        "componentes.yml lists base image gone, which no longer ships"
    ]
    assert drift(rows, dict(imgs, php="x"), apps, {"gestion"}) == [
        "distribution fork gestion ships but has no componentes.yml row"
    ]
    res = resolve(rows, imgs, "34.0.5", {"eurooffice": "11.0.7"})
    assert [r["version"] for r in res] == ["34.0.5", "8.10.2-alpine", "8.4.26-fpm-alpine3.24", "—", "11.0.7"], res
    assert [r["modified"] for r in res] == ["No", "No", "No", "No", "Sí"], res
    assert (
        "| P | [x](https://x) | 11.0.7 | `AGPL-3.0-only` | Sí | Nombre. |"
        in render(res)
    )
    assert shipped_images('{"aio_services_v1": [{"image": "ghcr.io/aps-conecta/aio-redis"}]}') == {"redis"}
    assert base_images.__doc__ and nc_server_version("ENV NEXTCLOUD_VERSION=34.0.5\n") == "34.0.5"
    assert manifest_apps('[{"id": "intravox", "source": "fork"}, {"id": "calendar", "source": "store"}]') == {"intravox", "calendar"}
    print(
        "[gen-componentes] selftest OK (drift both ways, manifest apps, base images, render)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
