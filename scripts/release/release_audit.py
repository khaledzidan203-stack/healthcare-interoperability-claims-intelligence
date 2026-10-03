"""Read-only public-tree release checks. No network, database or source writes.

The regression suite uses its existing isolated OS temporary directories.
This auditor never opens ignored credential/runtime files or prints their values.
"""
from __future__ import annotations

import argparse
import ast
import csv
import fnmatch
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
RUN = "snapshot_20261001_portfolio_4patients_v1"
REPORT = Path("powerbi/HealthcareInteroperabilityClaims.Report")
MODEL = Path("powerbi/HealthcareInteroperabilityClaims.SemanticModel/definition")
PAGES = {
    "6d04c910ec0a42270c1a": ("INDEX", 8),
    "e470b425b32f9bdc7a16": ("Executive Overview", 14),
    "93a77f48dcca84f1a64d": ("Claims Activity", 11),
    "363f4c4b16ab4c25de1d": ("Clinical & Coding", 10),
    "45f44dd944255de928e4": ("Provider & Payer", 10),
    "20908086e6ada0788299": ("Terminology & Governance", 10),
    "5966bf7edfc1090b40fb": ("Methodology & Validation", 14),
}
REQUIRED = [
    "README.md", "SECURITY.md", "LICENSE", "THIRD_PARTY_NOTICES.md", ".gitattributes",
    ".env.example", ".gitignore", "requirements.txt",
    "docs/SETUP.md", "docs/REPOSITORY_MAP.md", "docs/PORTFOLIO_CASE_STUDY.md",
    "docs/architecture/RELEASE_ARCHITECTURE.md",
    "docs/architecture/ENGINEERING_DECISIONS.md",
    "docs/validation/RELEASE_VALIDATION_EVIDENCE.md",
    "docs/validation/RELEASE_CHECKLIST.md", "docs/validation/PUBLICATION_PLAN.md",
    "docs/validation/PUBLICATION_INVENTORY.csv",
    "docs/validation/RELEASE_PRESERVATION_BASELINE.json",
    "docs/validation/RELEASE_NOTES_v1.0.0.md",
    "docs/semantic/RELEASE_DATA_DICTIONARY.md", "docs/powerbi/SCREENSHOT_GALLERY.md",
    "docs/source/PUBLIC_SOURCE_MANIFEST.md", "docs/source/CMS_SAMPLE_FHIR_PROVENANCE.md",
    ".github/workflows/ci.yml", "powerbi/HealthcareInteroperabilityClaims.pbip",
    str(REPORT / "definition.pbir"),
    "powerbi/HealthcareInteroperabilityClaims.SemanticModel/definition.pbism",
    str(MODEL / "model.tmdl"), str(MODEL / "relationships.tmdl"),
]
SQL = ["01_create_foundation.sql", "02_harden_multirun_staging.sql",
       "03_analytical_model_discovery.sql", "04_create_analytics_model.sql",
       "05_promote_analytics_dq_validated.sql"]
PRIVATE_PROBES = [".env", ".env.production", "data/raw/probe.json",
                  "data/staging/probe.csv", "data/processed/probe.json", "logs/probe.log",
                  "powerbi/a/.pbi/localSettings.json", "powerbi/a/cache.abf",
                  "src/a/__pycache__/a.pyc",
                  "data/source_reference/synthetic_users/synthetic_users_by_claim_count_full.csv"]
LOCAL_PATH = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]|/(?:Users|home)/[A-Za-z0-9_.-]+/")
SECRET = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}|\bAKIA[A-Z0-9]{16}\b|"
    r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|"
    r"(?i:Bearer\s+[A-Za-z0-9_.-]{24,})"
)
ASSIGNMENT = re.compile(
    r'''(?ix)["']?(?:client_secret|access_token|refresh_token|password|CMS_BLUEBUTTON_CLIENT_SECRET)["']?\s*[:=]\s*["']([^"'\r\n]+)["']'''
)
# Exact reviewed test-only sentinels, restricted to the persistence regression.
# Hashes avoid duplicating even dummy token strings in release output.
TEST_SENTINEL_HASHES = {
    "8ac950188678f9bb3524b275130332b511bf5092394da6975b5fb9e84302f026",
    "894e01a8315fcc4199bed8138560585d3ebdd0b4a2e295e47d730dc45061d12b",
    "8a1914992d43ca2225bb7ea93ab149b4c455750da5bf8e987f391b935a11722b",
}


def ignore_rules(root: Path) -> list[str]:
    return [s.strip() for s in (root / ".gitignore").read_text().splitlines()
            if s.strip() and not s.lstrip().startswith("#")]


def ignored(path: str, rules: list[str]) -> bool:
    """Match this repository's simple gitignore dialect, including negations.

    Actual Git is also checked when this root has its own Git repository.
    Nested ignore files are rejected so they cannot silently change the plan.
    """
    result = False
    for raw in rules:
        negate = raw.startswith("!")
        pattern = raw[1:] if negate else raw
        pattern = pattern.lstrip("/")
        if pattern.endswith("/"):
            pattern = pattern[:-1]
            prefixes = ["/".join(path.split("/")[:i]) for i in range(1, len(path.split("/")))]
            matched = any(fnmatch.fnmatchcase(p, pattern) for p in prefixes)
            if "/" not in pattern:
                matched = any(fnmatch.fnmatchcase(p, pattern) for p in path.split("/")[:-1])
            if "/**/" in pattern:
                matched |= any(fnmatch.fnmatchcase(p, pattern.replace("/**/", "/")) for p in prefixes)
        elif "/" not in pattern:
            matched = any(fnmatch.fnmatchcase(p, pattern) for p in path.split("/"))
        else:
            matched = fnmatch.fnmatchcase(path, pattern)
        if matched:
            result = not negate
    return result


def public_tree(root: Path, rules: list[str]) -> tuple[list[Path], list[str]]:
    public, excluded = [], []
    def walk(directory: Path) -> None:
        for p in sorted(directory.iterdir()):
            rel = p.relative_to(root).as_posix()
            if p.name == ".git":
                excluded.append(rel + "/ [Git metadata]")
                continue
            if p.is_symlink() or p.is_junction():
                raise ValueError("Linked filesystem entry requires review: " + rel)
            if p.is_dir():
                if ignored(rel + "/__probe__", rules):
                    excluded.append(rel + "/**")
                    keep = p / ".gitkeep"
                    if keep.is_file() and not ignored(rel + "/.gitkeep", rules):
                        public.append(keep)
                else:
                    walk(p)
            elif ignored(rel, rules):
                excluded.append(rel)
            else:
                public.append(p)
    walk(root)
    return sorted(public), sorted(excluded)


def classification(path: str) -> str:
    if path.startswith("data/source_reference/"):
        return "KEEP_PUBLIC_WITH_ATTRIBUTION"
    if path.startswith("docs/") and not any(x in path for x in (
        "RELEASE_", "PUBLICATION_", "SCREENSHOT_GALLERY", "ENGINEERING_DECISIONS",
        "SETUP.md", "REPOSITORY_MAP", "PORTFOLIO_CASE_STUDY", "docs/source/PUBLIC_SOURCE",
        "docs/source/CMS_SAMPLE", "docs/security/", "docs/governance/")):
        return "KEEP_PUBLIC_HISTORICAL"
    if path in ("PROJECT_INDEX.md", "CHANGELOG.md"):
        return "KEEP_PUBLIC_HISTORICAL"
    return "KEEP_PUBLIC"


def git_ignored_paths(root: Path, paths: list[str]) -> set[str]:
    """NUL-delimited binary I/O avoids Windows CRLF translation and Git quoting."""
    result = subprocess.run(["git", "check-ignore", "--no-index", "-z", "--stdin"],
                            input=("\0".join(paths) + "\0").encode("utf-8"),
                            cwd=root, capture_output=True)
    if result.returncode not in (0, 1):
        raise RuntimeError("Git ignore inspection failed")
    return {p for p in result.stdout.decode("utf-8").split("\0") if p}


def run(root: Path, tests: bool = True) -> dict:
    sys.dont_write_bytecode = True
    failures, checks = [], {}
    def check(name: str, ok: bool, detail: object = "") -> None:
        checks[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            failures.append(name)
    rules = ignore_rules(root)
    public, excluded = public_tree(root, rules)
    names = {p.relative_to(root).as_posix() for p in public}
    check("required_files", all((root / p).is_file() for p in REQUIRED),
          [p for p in REQUIRED if not (root / p).is_file()])
    check("private_boundaries", all(ignored(p, rules) for p in PRIVATE_PROBES))
    check("nested_gitignore", not any(p.endswith("/.gitignore") for p in names))
    check("unexpected_public_data", all(p.endswith("/.gitkeep") or p.startswith("data/source_reference/cms_")
                                          for p in names if p.startswith("data/")))
    syntax_errors, json_errors, paths, secrets_found, links, artifacts = [], [], [], [], [], []
    trees = {}
    for p in public:
        rel = p.relative_to(root).as_posix()
        if re.search(r"(?i)(?:^|[/_. -])(backup|temp|tmp|old|copy|draft|scratch)(?:[/_. -]|$)", rel):
            artifacts.append(rel)
        if p.suffix.lower() == ".png":
            continue
        try:
            s = p.read_text(encoding="utf-8-sig")
        except UnicodeError:
            failures.append("unreviewed_binary:" + rel)
            continue
        if p.suffix == ".py":
            try:
                trees[rel] = ast.parse(s, filename=rel)
                compile(s, rel, "exec")
            except SyntaxError:
                syntax_errors.append(rel)
        if p.suffix in (".json", ".pbip", ".pbir", ".pbism"):
            try:
                json.loads(s)
            except ValueError:
                json_errors.append(rel)
        for number, line in enumerate(s.splitlines(), 1):
            if LOCAL_PATH.search(line):
                paths.append(f"{rel}:{number}")
            if SECRET.search(line):
                secrets_found.append(f"{rel}:{number}:token-pattern")
        for hit in ASSIGNMENT.finditer(s):
            value = hit.group(1)
            # Exact test fixtures only, never blanket-exempt test source.
            if rel == "tests/test_ingestion_core.py" and hashlib.sha256(value.encode()).hexdigest() in TEST_SENTINEL_HASHES:
                continue
            secrets_found.append(f"{rel}:{s.count(chr(10), 0, hit.start()) + 1}:credential-literal")
        if p.name == ".env.example":
            for line in s.splitlines():
                if re.match(r"CMS_BLUEBUTTON_CLIENT_(?:ID|SECRET)=.+", line):
                    secrets_found.append(rel + ":nonempty-example-credential")
        if p.suffix == ".md":
            # Ignore fenced examples, validate inline and reference-style destinations.
            prose = re.sub(r"```.*?```", "", s, flags=re.S)
            targets = re.findall(r"!?\[[^\]]*\]\((<[^>]+>|[^)]+)\)", prose)
            targets += re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)", prose)
            for target in targets:
                target = target.strip().strip("<>")
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                dest = (p.parent / unquote(target.split("#")[0])).resolve()
                if not dest.is_relative_to(root) or not dest.exists():
                    links.append(rel + " -> " + target)
                elif dest.is_file() and dest.relative_to(root).as_posix() not in names:
                    links.append(rel + " -> excluded target " + target)
    check("python_syntax", not syntax_errors, syntax_errors)
    check("json_parse", not json_errors, json_errors)
    check("absolute_personal_paths", not paths, paths)
    check("secret_patterns", not secrets_found, secrets_found)
    check("markdown_and_image_links", not links, links)
    check("release_artifacts", not artifacts, artifacts)
    package = {k: v for k, v in trees.items() if k.startswith("src/healthcare_claims/")}
    inventory = (len(package), sum(isinstance(n, ast.FunctionDef) for t in package.values() for n in t.body),
                 sum(isinstance(n, ast.ClassDef) for t in package.values() for n in t.body))
    check("python_inventory", inventory == (17, 70, 13), inventory)
    imports = {n.names[0].name.split('.')[0] if isinstance(n, ast.Import) else n.module.split('.')[0]
               for t in package.values() for n in ast.walk(t)
               if isinstance(n, ast.Import) or isinstance(n, ast.ImportFrom) and not n.level and n.module}
    check("stdlib_runtime", not (imports - sys.stdlib_module_names), sorted(imports - sys.stdlib_module_names))
    sys.path.insert(0, str(root / "src"))
    for rel in package:
        importlib.import_module("healthcare_claims." + Path(rel).stem)
    check("python_imports", True, len(package))
    sqls = sorted((root / "sql").glob("*.sql"))
    check("sql_inventory", [p.name for p in sqls] == SQL)
    counts = {k: sum(len(re.findall(r"(?im)^CREATE\s+" + k + r"\b", p.read_text())) for p in sqls)
              for k in ("TABLE", "SCHEMA", "INDEX", "UNIQUE INDEX")}
    check("sql_objects", counts == {"TABLE": 40, "SCHEMA": 4, "INDEX": 27, "UNIQUE INDEX": 2}, counts)
    tables = list((root / MODEL / "tables").glob("analytics *.tmdl"))
    measures = (root / MODEL / "tables/_Measures.tmdl").read_text(encoding="utf-8-sig")
    relationships = (root / MODEL / "relationships.tmdl").read_text(encoding="utf-8-sig")
    sem = {"business_tables": len(tables), "measures": len(re.findall(r"(?m)^\s*measure ", measures)),
           "relationships": len(re.findall(r"(?m)^relationship ", relationships)),
           "inactive": relationships.count("isActive: false")}
    check("semantic_inventory", sem == {"business_tables": 22, "measures": 9, "relationships": 50, "inactive": 5}, sem)
    check("coverage_excluded", "coverage" not in relationships.lower() and not any("coverage" in p.name for p in tables))
    check("measure_run_guards", measures.count("HASONEVALUE('analytics dim_pipeline_run'[pipeline_run_key])") == 9)
    check("financial_guards", measures.count("HASONEVALUE('analytics dim_financial_concept'[financial_concept_key])") == 3
          and measures.count("HASONEVALUE('analytics dim_currency'[currency_key])") == 3)
    report = json.loads((root / REPORT / "definition/report.json").read_text())
    filters = report.get("filterConfig", {}).get("filters", [])
    run_filters = [f for f in filters if f.get("field", {}).get("Column", {}).get("Property") == "pipeline_run_id"]
    valid = False
    if len(run_filters) == 1:
        f = run_filters[0]
        valid = (f["field"]["Column"]["Expression"]["SourceRef"].get("Entity") == "analytics dim_pipeline_run"
                 and f.get("isLockedInViewMode") is True and f.get("isHiddenInViewMode") is True
                 and f["filter"]["Where"] == [{"Condition": {"In": {
                     "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "r"}}, "Property": "pipeline_run_id"}}],
                     "Values": [[{"Literal": {"Value": "'" + RUN + "'"}}]]}}}])
    check("governed_report_filter", valid, RUN)
    page_inventory = {}
    for p in (root / REPORT / "definition/pages").glob("*/page.json"):
        j = json.loads(p.read_text())
        page_inventory[p.parent.name] = (j["displayName"], len(list(p.parent.glob("visuals/*/visual.json"))))
        check("page_layout:" + p.parent.name, (j["width"], j["height"], j["displayOption"]) == (1920, 1080, "FitToPage"))
    check("report_inventory", page_inventory == PAGES, page_inventory)
    check("page_order", json.loads((root / REPORT / "definition/pages/pages.json").read_text())["pageOrder"] == list(PAGES))
    shots = []
    for i, (name, _) in enumerate(PAGES.values(), 1):
        p = root / "screen_shot" / f"{i}_{name}.png"
        if p.is_file():
            b = p.read_bytes()
            if b[:8] == b"\x89PNG\r\n\x1a\n":
                shots.append({"file": p.name, "pixels": struct.unpack(">II", b[16:24]), "sha256": hashlib.sha256(b).hexdigest()})
    check("screenshots", len(shots) == 7, shots)
    manifest = (root / "docs/source/PUBLIC_SOURCE_MANIFEST.md").read_text()
    fixture_matches = re.findall(r"`(data/source_reference/[^`]+)`\s*\|[^\n]*?`([a-f0-9]{64})`", manifest)
    check("source_fixture_hashes", len(fixture_matches) == 6 and all(
        hashlib.sha256((root / p).read_bytes()).hexdigest() == digest for p, digest in fixture_matches))
    baseline = json.loads((root / "docs/validation/RELEASE_PRESERVATION_BASELINE.json").read_text(encoding="utf-8"))
    protected = {p for p in names if p.startswith(("src/", "tests/", "sql/", "powerbi/", "screen_shot/", "data/source_reference/"))}
    baseline_files = baseline["files"]
    changed = [p for p, digest in baseline_files.items()
               if p not in names or hashlib.sha256((root / p).read_bytes()).hexdigest() != digest]
    check("validated_baseline_preservation", len(baseline_files) == 170 and protected == set(baseline_files) and not changed,
          {"files": len(baseline_files), "changed": changed, "inventory_difference": sorted(protected ^ set(baseline_files))})
    check("curated_data_allowlist", {p for p in names if p.startswith("data/") and not p.endswith("/.gitkeep")}
          == {p for p, _ in fixture_matches})
    inventory_file = root / "docs/validation/PUBLICATION_INVENTORY.csv"
    if inventory_file.is_file():
        rows = list(csv.DictReader(io.StringIO(inventory_file.read_text(encoding="utf-8-sig"))))
        recorded = {r["path_or_boundary"] for r in rows if r["classification"].startswith("KEEP_PUBLIC")}
        check("publication_inventory_current", recorded == names,
              {"missing": sorted(names - recorded), "obsolete": sorted(recorded - names)})
    if (root / ".git").exists():
        git = shutil.which("git")
        if not git:
            check("git_boundary", False, "Git unavailable")
        else:
            tracked = subprocess.run([git, "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout.decode().split("\0")
            check("tracked_private_files", not any(ignored(p, rules) for p in tracked if p))
            check("git_boundary", git_ignored_paths(root, PRIVATE_PROBES) == set(PRIVATE_PROBES))
            candidates = subprocess.run([git, "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                                        cwd=root, capture_output=True, check=True).stdout.decode().split("\0")
            check("git_inclusion_parity", set(p for p in candidates if p) == names)
            index = subprocess.run([git, "ls-files", "--stage", "-z"], cwd=root,
                                   capture_output=True, check=True).stdout.decode().split("\0")
            entries = [e.split("\t", 1) for e in index if e]
            if entries:
                check("staged_inventory", {path for _, path in entries} == names)
                check("index_modes", all(meta.split()[0] == "100644" and meta.split()[2] == "0" for meta, _ in entries))
                # Compare the actual staged blobs to the already scanned working tree.
                # This catches line-ending conversion and stale/unscanned index content.
                ids = [meta.split()[1] for meta, _ in entries]
                blobs = subprocess.run([git, "cat-file", "--batch"], cwd=root,
                                       input=("\n".join(ids) + "\n").encode(), capture_output=True, check=True).stdout
                offset, mismatches = 0, []
                for _, path in entries:
                    end = blobs.index(b"\n", offset)
                    header = blobs[offset:end].split()
                    size = int(header[2])
                    content = blobs[end + 1:end + 1 + size]
                    if header[1] != b"blob" or content != (root / path).read_bytes():
                        mismatches.append(path)
                    offset = end + 1 + size + 1
                check("staged_bytes_match_scanned_source", not mismatches, mismatches)
    else:
        checks["git_boundary"] = {"status": "REVIEW", "detail": "No Git repository; policy projection only. Recheck with actual Git before staging."}
    if tests:
        suite = unittest.defaultTestLoader.discover(str(root / "tests"))
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        check("regression", result.wasSuccessful() and result.testsRun == 94,
              {"run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors)})
        sys.path.insert(0, str(root / "scripts/release"))
        release_suite = unittest.defaultTestLoader.discover(str(root / "scripts/release"), top_level_dir=str(root / "scripts/release"))
        release_result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(release_suite)
        check("auditor_regression", release_result.wasSuccessful() and release_result.testsRun == 7,
              {"run": release_result.testsRun, "failures": len(release_result.failures), "errors": len(release_result.errors)})
    preserved = checks["validated_baseline_preservation"]["status"] == "PASS"
    checks["pbir_runtime"] = {
        "status": "CARRIED_FORWARD" if preserved else "FAIL",
        "detail": "Owner-attested successful PBIR/Desktop baseline; complete protected artifact identity checked. No fresh runtime validation.",
        "validation_state": "CARRIED_FORWARD_FROM_BYTE_IDENTICAL_VALIDATED_BASELINE" if preserved else "BASELINE_CHANGED",
    }
    return {"static_status": "FAIL" if failures else "PASS", "public_file_count": len(public),
            "excluded_groups": excluded, "checks": checks, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", action="store_true", help="Print exact public candidates and excluded boundaries as CSV")
    parser.add_argument("--pbir", action="store_true", help="Also attempt local PBIR validation using the normal policy-controlled launcher")
    args = parser.parse_args()
    if args.inventory:
        public, excluded = public_tree(ROOT, ignore_rules(ROOT))
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(["path_or_boundary", "classification"])
        for p in public:
            rel = p.relative_to(ROOT).as_posix()
            writer.writerow([rel, classification(rel)])
        for p in excluded:
            writer.writerow([p, "KEEP_LOCAL_ONLY / EXCLUDE_GIT"])
        return 0
    try:
        result = run(ROOT)
        if args.pbir:
            command = 'powerbi-report-author validate "powerbi/HealthcareInteroperabilityClaims.Report"'
            if os.name == "nt":
                invocation = ["powershell", "-NoProfile", "-Command", "$ErrorActionPreference='Stop'; " + command]
            else:
                invocation = ["powerbi-report-author", "validate", str(REPORT)]
            try:
                process = subprocess.run(invocation, cwd=ROOT, capture_output=True, text=True, timeout=60)
                output = process.stdout + process.stderr
                blocked = "PSSecurityException" in output or "running scripts is disabled" in output
                status = "BLOCKED" if blocked else ("REVIEW" if process.returncode == 0 else "FAIL")
                result["checks"]["pbir_runtime"] = {
                    "status": status, "exit_code": process.returncode,
                    "schema_unreachable_reported": "PBIR_SCHEMA_UNREACHABLE" in output,
                    "detail": "Execution policy blocked normal launcher" if blocked else
                              "Review validator diagnostics for error/warning counts; exit code alone is not schema certification",
                }
            except (OSError, subprocess.TimeoutExpired):
                result["checks"]["pbir_runtime"] = {"status": "BLOCKED", "detail": "Validator unavailable or timed out"}
    except Exception as exc:
        # No exception values: they may contain environment-specific information.
        print(json.dumps({"static_status": "FAIL", "audit_error_type": type(exc).__name__}))
        return 1
    print(json.dumps(result, indent=2))
    return int(result["static_status"] != "PASS" or args.pbir and result["checks"]["pbir_runtime"]["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
