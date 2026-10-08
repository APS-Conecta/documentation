#!/usr/bin/env python3
"""captura — the screenshots driver (Phase 11, capturas.yml).

Brings up the throwaway lean stack (tools/capturas/compose.yaml), enables the
five suite apps from clones (never `occ app:install`), pins es/es_CL + the
enforced light theme, seeds a deterministic synthetic fixture, and captures one
1440x900 viewport screenshot per app with Playwright. Every PNG is
oxipng-normalized before diffing against HEAD; the byte-stability table lands
in $GITHUB_STEP_SUMMARY when set, stdout otherwise.

Idioms mirrored from gestion/provisioning (citations org-root-relative):
  - tar-stream each app into custom_apps as www-data (provisioning/lib.sh's
    ensure_vendored_app unpack: files must land owned by www-data);
  - `occ app:enable` only, store off first — enable reads what is on disk and
    never contacts the store; keep occ's own error text (lib.sh:355-361);
  - the four locale calls of provisioning/phases/10-locale.sh:15-18;
  - enforce_theme light (system) + theming disable-user-theming, written 'yes'
    and stored '1' (phases/15-branding.sh:48-49 + lib.sh theming_set's trap);
  - one visibly-synthetic sample file, then `occ files:scan`
    (phases/60-fixtures.sh ensure_sample_file idiom).

Env: APS_ORG_ROOT (default /opt/aps-conecta-org) — local clone root;
     CAPTURAS_APPS — clone dir in CI (takes precedence over APS_ORG_ROOT);
     CAPTURAS_PORT (default 8095, mirrors the compose port default);
     OXIPNG_BIN (default `oxipng` on PATH) — the sha256-verified binary.

Exit: 0 = captured (changed or not); 1 = any hard failure (roster != 5 apps,
missing clone, unhealthy stack, enable failure, wrong PNG set, dimension
mismatch, oxipng failure).
"""

import argparse
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
COMPOSE = HERE / "compose.yaml"
CATALOGO = REPO / "catalogo.yml"
CAPTURAS = REPO / "capturas"

VIEWPORT_W = 1440
VIEWPORT_H = 900
SETTLE_MS = 1500  # fixed settle after networkidle (build-og idiom, sized for the SPA)
SIZECLASS_LENIENCY = 0.05  # --compare sizeclass fallback (build-og.py's "noise people ignore" warning)
NO_ANIM_CSS = ("*, *::before, *::after {"
               " animation: none !important; transition: none !important; }")

FIXTURE_NAME = "Bienvenida-captura.md"
FIXTURE_BODY = """\
# Bienvenida a APS Conecta (captura de pantalla)

Este archivo **sintético** existe para que la captura semanal de pantallas
muestre un estado determinista. No contiene datos reales.
"""


def log(msg: str) -> None:
    print(f"[capturas] {msg}")


def die(msg: str) -> None:
    print(f"[capturas] FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)


def run_bytes(argv, **kw):
    return subprocess.run(argv, capture_output=True, **kw)


# --- roster + appid ----------------------------------------------------------


def apps_dir() -> Path:
    d = os.environ.get("CAPTURAS_APPS") or os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org")
    return Path(d)


def roster() -> list:
    """catalogo.yml -> the five kind: nextcloud-app rows, canonical repo names.

    The SSOT-side half of gen-catalogo.py's parity invariant: exactly five
    nextcloud-app rows. The OWN_APPS fold against gestion stays owned by the
    catalog generator — one invariant, one owner.
    """
    rows = yaml.safe_load(CATALOGO.read_text(encoding="utf-8"))["repos"]
    names = [r["repo"] for r in rows if r.get("kind") == "nextcloud-app"]
    if len(names) != 5:
        die(f"catalogo.yml holds {len(names)} kind: nextcloud-app rows "
            f"({', '.join(names)}); this pipeline is built for exactly five")
    return names


def appid_of(clone: Path) -> str:
    """<id> from the clone's appinfo/info.xml — the only true source
    (IntraVox -> intravox; never a hardcoded map)."""
    info = clone / "appinfo" / "info.xml"
    if not info.is_file():
        die(f"missing {info} — clone incomplete?")
    return ET.parse(info).getroot().findtext("id").strip()


def resolve_roster() -> list:
    """[(repo, appid)] in roster order, every clone verified on disk."""
    pairs = []
    for name in roster():
        clone = apps_dir() / name
        if not (clone / "appinfo" / "info.xml").is_file():
            die(f"clone {clone} is missing its appinfo/info.xml — clone it first "
                f"(APS_ORG_ROOT locally, CAPTURAS_APPS in CI)")
        pairs.append((name, appid_of(clone)))
    return pairs


# --- compose + occ -----------------------------------------------------------


def compose(*argv, **kw):
    return run(["docker", "compose", "-f", str(COMPOSE), *argv], **kw)


def occ(*args):
    """occ in the container as www-data — env.sh's console form. Every call is
    logged: the job log is the evidence that the store went off BEFORE the
    first enable and that no `app:install` ever runs."""
    log("occ " + " ".join(args))
    return compose("exec", "-T", "-u", "www-data", "nextcloud",
                   "php", "/var/www/html/occ", *args)


def wait_installed() -> None:
    """occ's own view of installed — `up --wait` gates on status.php, which can
    answer 200 while the installer is still finishing."""
    for _ in range(60):  # 60 x 5s = 5 min on top of the compose health budget
        p = occ("status", "--output", "json")
        if p.returncode == 0:
            try:
                if json.loads(p.stdout).get("installed") is True:
                    return
            except ValueError:
                pass
        time.sleep(5)
    die("stack never reached installed=true (occ status)")


def stream_app_in(clone: Path, appid: str) -> None:
    """Stage the clone as <appid>/ (repo case != appid for IntraVox), .git and
    node_modules excluded at staging time, then tar-stream it into custom_apps
    as www-data — lib.sh's unpack idiom: nothing is copied through the host, and
    files must land owned by www-data (uid 33) or the app cannot be used.
    node_modules is a local build artifact (untracked in every clone, absent
    from a CI shallow clone — and one local copy self-loops), so excluding it
    makes the local staging byte-equal to CI's."""
    with tempfile.TemporaryDirectory(prefix="capturas-stage-") as stage:
        shutil.copytree(clone, Path(stage) / appid,
                        ignore=shutil.ignore_patterns(".git", "node_modules"))
        pack = subprocess.Popen(["tar", "-C", stage, "-cf", "-", appid], stdout=subprocess.PIPE)
        unpack = subprocess.Popen(
            ["docker", "compose", "-f", str(COMPOSE), "exec", "-T", "-u", "www-data",
             "nextcloud", "tar", "xf", "-", "-C", "/var/www/html/custom_apps"],
            stdin=pack.stdout)
        pack.stdout.close()  # let SIGPIPE propagate either way
        unpack_rc, pack_rc = unpack.wait(), pack.wait()
        if unpack_rc != 0 or pack_rc != 0:
            die(f"tar-stream of {clone.name} into custom_apps/{appid} failed")


def enable_apps(appids: list) -> None:
    # Store OFF before anything is enabled. `app:enable` only, never
    # `app:install`: enable reads what is on disk and never contacts the store.
    p = occ("config:system:set", "appstoreenabled", "--value=false", "--type=boolean")
    if p.returncode != 0:
        die(f"appstoreenabled=false failed — occ said: {p.stderr.strip()[:300]}")
    for appid in appids:
        p = occ("app:enable", appid)
        if p.returncode != 0:
            # Keep occ's own error: it is the only thing that says WHY
            # (lib.sh's #41 lesson — never guess a cause).
            die(f"occ app:enable {appid} failed — occ said: {p.stderr.strip()[:300]}")


def pin_config() -> None:
    """The four 10-locale.sh calls + the 15-branding.sh theme pair, verbatim."""
    for args in (
        ("config:system:set", "default_language", "--value=es"),
        ("config:system:set", "force_language", "--value=es"),
        ("config:system:set", "default_locale", "--value=es_CL"),
        ("config:system:set", "default_phone_region", "--value=CL"),
        ("config:system:set", "enforce_theme", "--value=light"),
    ):
        p = occ(*args)
        if p.returncode != 0:
            die(f"{' '.join(args)} failed — occ said: {p.stderr.strip()[:300]}")
    # theming-app config, NOT a raw config:app:set — ThemingController stores
    # this via setAppValueBool: written 'yes', stored '1' (lib.sh theming_set).
    p = occ("theming:config", "disable-user-theming", "yes")
    if p.returncode != 0:
        die(f"theming:config disable-user-theming failed — occ said: {p.stderr.strip()[:300]}")


def seed_fixture() -> None:
    """One visibly-synthetic welcome file in admin's Files + firstrunwizard
    off, so first-run hints can never differ between runs. Written as www-data
    into the image-default datadir, then files:scan — the ensure_sample_file
    idiom. Content is pinned in this file, so overwrite + scan is idempotent."""
    dest = f"/var/www/html/data/admin/files/{FIXTURE_NAME}"
    argv = ["docker", "compose", "-f", str(COMPOSE), "exec", "-T", "-u", "www-data",
            "nextcloud", "sh", "-c",
            f'mkdir -p "$(dirname "{dest}")" && cat > "{dest}"']
    fed = subprocess.run(argv, input=FIXTURE_BODY.encode(), capture_output=True)
    if fed.returncode != 0:
        die(f"seeding {FIXTURE_NAME} failed — {fed.stderr.decode(errors='replace').strip()[:300]}")
    if occ("files:scan", "admin").returncode != 0:
        die("occ files:scan admin failed")
    if occ("user:setting", "admin", "firstrunwizard", "show", "0").returncode != 0:
        die("occ user:setting admin firstrunwizard show 0 failed")
    log(f"fixture {FIXTURE_NAME} seeded + indexed")


# --- Playwright --------------------------------------------------------------


def assert_ihdr(png: Path) -> None:
    head = png.read_bytes()[:24]
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        die(f"{png.name}: not a PNG")
    w, h = struct.unpack(">II", head[16:24])
    if (w, h) != (VIEWPORT_W, VIEWPORT_H):
        die(f"{png.name}: IHDR is {w}x{h}, expected {VIEWPORT_W}x{VIEWPORT_H}")


def nav_hrefs(page, base_url: str, appids: list) -> dict:
    """appid -> href from the server-side OCS navigation endpoint — the same
    source the SPA and the mobile clients consume. Route-agnostic by
    construction: hrefs come from the server, never guessed (epidemiologia's
    Spanish URL included). NC 34's Vue dashboard renders no li[data-id] nav
    and no app href links to click, so the server is the only route source."""
    r = page.request.get(base_url + "/ocs/v2.php/core/navigation/apps?format=json",
                         headers={"OCS-APIRequest": "true"})
    try:
        entries = r.json()["ocs"]["data"]
    except (ValueError, KeyError):
        die(f"navigation endpoint answered {r.status} — cannot resolve app hrefs")
    hrefs = {o["id"]: o["href"] for o in entries}
    missing = [a for a in appids if a not in hrefs]
    if missing:
        die(f"navigation has no entry for {missing} — app enabled without nav?")
    return hrefs


def capture(base_url: str, appids: list) -> None:
    # Imported lazily so --selftest never needs Playwright installed.
    from playwright.sync_api import sync_playwright

    CAPTURAS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
                                device_scale_factor=1, reduced_motion="reduce")
        page.goto(base_url + "/", wait_until="networkidle")
        page.fill('input[name="user"]', "admin")
        page.fill('input[name="password"]', "admin")
        # NC 34 renders the login form with class login-form (no id), fully
        # client-side; the submit button is the form's type=submit button-vue.
        page.click('form.login-form button[type="submit"]')
        page.wait_for_url(lambda url: "/login" not in url, timeout=90_000)
        page.wait_for_load_state("networkidle")
        hrefs = nav_hrefs(page, base_url, appids)
        for appid in appids:
            # Navigate by the server-served href — see nav_hrefs: guessing
            # routes breaks on apps whose route is a Spanish URL (epidemiologia
            # has exactly one, and it is not guessable).
            page.goto(base_url + hrefs[appid], wait_until="networkidle")
            page.wait_for_timeout(SETTLE_MS)
            page.add_style_tag(content=NO_ANIM_CSS)
            out = CAPTURAS / f"{appid}.png"
            page.screenshot(path=str(out), full_page=False)  # the viewport, exactly
            assert_ihdr(out)
            log(f"captured {out.relative_to(REPO)} ({out.stat().st_size} B)")
        browser.close()


# --- normalize + diff --------------------------------------------------------


def normalize(pngs: list) -> None:
    binary = os.environ.get("OXIPNG_BIN", "oxipng")
    for png in pngs:
        p = run([binary, "-o", "4", "--strip", "safe", str(png)])
        if p.returncode != 0:
            die(f"oxipng failed on {png.name}: {(p.stderr or p.stdout).strip()[:300]}")


def old_bytes(png: Path):
    """HEAD's bytes for the PNG, or None when untracked (run 1)."""
    p = run_bytes(["git", "-C", str(REPO), "show", f"HEAD:capturas/{png.name}"])
    return p.stdout if p.returncode == 0 and p.stdout else None


def equal_under(old, new: bytes, compare: str) -> bool:
    if old is None:
        return False  # a new file is a change, not an equality
    if compare == "sizeclass":
        return abs(len(old) - len(new)) <= len(new) * SIZECLASS_LENIENCY
    return old == new


def report(rows: list, compare: str) -> None:
    lines = ["| png | old B | new B | delta | equal? |",
             "|---|---:|---:|---:|---|"]
    for name, old, new, equal in rows:
        old_s = "new" if old is None else str(len(old))
        delta = "-" if old is None else f"{len(new) - len(old):+d}"
        lines.append(f"| `{name}` | {old_s} | {len(new)} | {delta} | {'yes' if equal else 'NO'} |")
    table = "\n".join(lines)
    print(table)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"\n### capturas — byte stability (compare: {compare})\n\n{table}\n")


# --- commands ----------------------------------------------------------------


def cmd_capture(args) -> None:
    pairs = resolve_roster()
    appids = [appid for _, appid in pairs]
    port = os.environ.get("CAPTURAS_PORT", "8095")

    up = compose("up", "-d", "--wait", "--wait-timeout", "420")
    try:
        if up.returncode != 0:
            die(f"stack failed to reach healthy: {(up.stderr or up.stdout).strip()[:300]}")
        wait_installed()
        for name, appid in pairs:
            stream_app_in(apps_dir() / name, appid)
            log(f"streamed {name} -> custom_apps/{appid}")
        enable_apps(appids)
        pin_config()
        seed_fixture()
        capture(f"http://localhost:{port}", appids)
    finally:
        down = compose("down", "-v")  # teardown on success AND failure paths
        if down.returncode != 0:
            log(f"WARNING: compose down -v failed: {down.stderr.strip()[:200]}")

    pngs = sorted(CAPTURAS.glob("*.png"))
    expected = {f"{appid}.png" for appid in appids}
    if {p.name for p in pngs} != expected:
        die(f"capturas/ must hold exactly {sorted(expected)}, found "
            f"{sorted(p.name for p in pngs)}")
    normalize(pngs)
    rows = []
    for png in pngs:
        new = png.read_bytes()
        old = old_bytes(png)
        rows.append((png.name, old, new, equal_under(old, new, args.compare)))
    report(rows, args.compare)
    log("done — 5 captures, normalized, diffed against HEAD")


def cmd_selftest(_args) -> None:
    """No docker: pin the roster fold + the appid map against local checkouts."""
    names = roster()
    want_names = {"farmacia", "territorio", "estadistica", "epidemiologia", "IntraVox"}
    assert set(names) == want_names, f"roster fold is {names}, want {sorted(want_names)}"
    want_map = {"farmacia": "farmacia", "territorio": "territorio",
                "estadistica": "estadistica", "epidemiologia": "epidemiologia",
                "IntraVox": "intravox"}
    got = {name: appid_of(apps_dir() / name) for name in names}
    assert got == want_map, f"appid map is {got}, want {want_map}"
    print("selftest ok: roster fold = 5 nextcloud-app rows; appid map = "
          + ", ".join(f"{k}->{v}" for k, v in got.items()))


def main() -> None:
    ap = argparse.ArgumentParser(description="weekly screenshots driver (Phase 11)")
    ap.add_argument("--selftest", action="store_true",
                    help="no docker: pin the roster fold + the appid map")
    sub = ap.add_subparsers(dest="cmd")
    cap = sub.add_parser("capture", help="up, enable, configure, capture, teardown")
    cap.add_argument("--compare", choices=["bytes", "sizeclass"], default="bytes",
                     help="diff gate: byte equality (default) or 5%% size class")
    args = ap.parse_args()
    if args.selftest:
        cmd_selftest(args)
    elif args.cmd == "capture":
        cmd_capture(args)
    else:
        ap.error("nothing to do — pass `capture` or `--selftest`")


if __name__ == "__main__":
    main()
