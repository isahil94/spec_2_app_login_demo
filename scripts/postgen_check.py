"""Post-generation validation and safe auto-fix template for backend agent.

Usage:
- Copy this file to `scripts/postgen_check.py` and run from the repository root.
- The script performs light-weight checks and applies safe, reversible fixes for
  common generator issues (missing `tests/conftest.py`, scripts importing `src`
  without `sys.path` management). It writes a report to
  `artifacts/backend/postgen-check-report.md` and appends an entry to
  `artifacts/backend/openlog.md`.

Note: This template performs only mechanical fixes. Semantic code changes
must be surfaced as suggested patches under `artifacts/backend/auto_fix_suggestions/`.
"""
from __future__ import annotations

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def find_repo_root(file_path: Path) -> Path:
    p = file_path.resolve()
    for i in range(6):
        candidate = p.parents[i]
        if (candidate / "ai").exists() or (candidate / "requirements.txt").exists() or (candidate / ".git").exists():
            return candidate
    return p.parents[1]


REPO_ROOT = find_repo_root(Path(__file__))
TEMPLATE_CONFT = REPO_ROOT / "ai" / "templates" / "testing" / "conftest.py"
TARGET_CONFT = REPO_ROOT / "tests" / "conftest.py"
SCRIPTS_DIR = REPO_ROOT / "scripts"
ARTIFACTS_DIR = REPO_ROOT / "artifacts" / "backend"
AUTO_FIX_DIR = ARTIFACTS_DIR / "auto_fix_suggestions"


def find_candidate_srcs(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for d in root.iterdir():
        if d.is_dir():
            s = d / "src"
            if s.exists() and s.is_dir():
                candidates.append(s)
    top_src = root / "src"
    if top_src.exists() and top_src.is_dir() and top_src not in candidates:
        candidates.append(top_src)
    if not candidates:
        for py in root.rglob("*.py"):
            try:
                txt = py.read_text(encoding="utf-8")
            except Exception:
                continue
            if "from fastapi" in txt or "import fastapi" in txt:
                candidates.append(py.parent)
                if len(candidates) >= 3:
                    break
    uniq: list[Path] = []
    for c in candidates:
        if c not in uniq:
            uniq.append(c)
    return uniq


def ensure_dirs():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    AUTO_FIX_DIR.mkdir(parents=True, exist_ok=True)


def copy_conftest_if_missing(report_lines: list[str]):
    if not TARGET_CONFT.exists():
        if TEMPLATE_CONFT.exists():
            shutil.copy2(TEMPLATE_CONFT, TARGET_CONFT)
            report_lines.append(f"Created tests/conftest.py from template: {TEMPLATE_CONFT}")
        else:
            report_lines.append("Template conftest not found; cannot create tests/conftest.py")
    else:
        report_lines.append("tests/conftest.py exists; no action taken")


SYS_PATH_SNIPPET = """# Auto-inserted by postgen_check: ensure backend src is importable
from pathlib import Path
import sys
repo_root = Path(__file__).resolve().parent
for p in [repo_root / 'apps' / 'backend' / 'src', repo_root / 'apps' / 'backend']:
    if p.exists():
        sp = str(p)
        if sp not in sys.path:
            sys.path.insert(0, sp)
            break
"""


def ensure_sys_path_in_scripts(report_lines: list[str]):
    if not SCRIPTS_DIR.exists():
        report_lines.append("No scripts/ directory found; skipping script checks")
        return

    for path in sorted(SCRIPTS_DIR.glob("*.py")):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            report_lines.append(f"Could not read {path}: {e}")
            continue

        if ("import src" in text) or ("from src" in text):
            if "Auto-inserted by postgen_check" in text or "repo_root / 'apps' / 'backend'" in text:
                report_lines.append(f"{path.name}: sys.path snippet already present")
                continue

            # Insert after shebang or encoding comment if present, else at top
            lines = text.splitlines()
            insert_at = 0
            if lines and lines[0].startswith("#!"):
                insert_at = 1
            if len(lines) > insert_at and lines[insert_at].startswith("# -*-"):
                insert_at += 1

            new_lines = lines[:insert_at] + [SYS_PATH_SNIPPET] + lines[insert_at:]
            backup = path.with_suffix(path.suffix + ".postgenbak")
            try:
                backup.write_text(text, encoding="utf-8")
            except Exception:
                pass
            path.write_text("\n".join(new_lines), encoding="utf-8")
            report_lines.append(f"Inserted sys.path snippet into {path.name} (backup: {backup.name})")


def detect_import_time_db_side_effects(report_lines: list[str]):
    # Scan backend src for simple patterns indicating import-time DB calls
    src_root = REPO_ROOT / "apps" / "backend" / "src"
    if not src_root.exists():
        report_lines.append("No apps/backend/src found; skipping DB side-effect scan")
        return

    patterns = ["Base.metadata.create_all", "engine.execute(", "db.commit("]
    problems = []
    for p in src_root.rglob("*.py"):
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for pat in patterns:
            if pat in txt:
                problems.append((p, pat))

    if not problems:
        report_lines.append("No import-time DB side-effects detected")
        return

    report_lines.append("Detected potential import-time DB side-effects:")
    for p, pat in problems:
        rel = p.relative_to(REPO_ROOT)
        report_lines.append(f" - {rel}: contains '{pat}'")
        # create a suggested patch file for manual review
        suggestion = AUTO_FIX_DIR / f"suggested_patch_{rel.name}.md"
        suggestion.write_text(
            f"File: {rel}\nIssue: contains '{pat}' at module import level.\nSuggested remediation: move the call into an application startup handler (e.g., FastAPI on_event('startup')) or guard it with: if settings.DEBUG and not os.getenv('TESTING'):\n",
            encoding="utf-8",
        )
        report_lines.append(f"  -> Suggested patch written to {suggestion.name}")


def write_reports(report_lines: list[str]):
    ts = datetime.utcnow().isoformat() + "Z"
    md_lines = []
    md_lines.append("# Postgen Check Report")
    md_lines.append("")
    md_lines.append(f"- Run: {ts}")
    md_lines.append("")
    md_lines.append("## Actions & Results")
    md_lines.append("")
    for line in report_lines:
        md_lines.append(f"- {line}")

    report_path = ARTIFACTS_DIR / "postgen-check-report.md"
    report_path.write_text("\n".join(md_lines), encoding="utf-8")

    # Append structured summary to openlog (human-friendly)
    openlog = ARTIFACTS_DIR / "openlog.md"
    with openlog.open('a', encoding='utf-8') as fh:
        fh.write('\n---\n')
        fh.write(f"Postgen check run: {ts}\n")
        for line in report_lines:
            fh.write(f"- {line}\n")


def main():
    ensure_dirs()
    report_lines: list[str] = []
    copy_conftest_if_missing(report_lines)
    ensure_sys_path_in_scripts(report_lines)
    detect_import_time_db_side_effects(report_lines)
    write_reports(report_lines)
    print("Postgen check complete. See artifacts/backend/postgen-check-report.md for details.")


if __name__ == "__main__":
    main()
