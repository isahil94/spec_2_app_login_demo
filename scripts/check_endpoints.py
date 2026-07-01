"""Run lightweight endpoint discovery and smoke GET requests using TestClient.

Writes a report to `artifacts/backend/endpoint-check-report.md` and appends an entry to `artifacts/backend/openlog.md`.
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Ensure test DB used
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_db_for_checks.sqlite3")

import sys

run_ts = datetime.utcnow().isoformat() + "Z"
report_lines = []
report_lines.append(f"Endpoint check run: {run_ts}")

# Try to locate backend 'src' directory dynamically
repo_root = Path(__file__).resolve().parent.parent
backend_candidates = [
    repo_root / 'apps' / 'backend' / 'src',
    repo_root / 'apps' / 'backend',
    repo_root / 'src',
    repo_root,
]

app_client = None
import_requests = False

for candidate in backend_candidates:
    # add candidate to sys.path if it exists
    if candidate.exists():
        sys.path.insert(0, str(candidate))
        report_lines.append(f"Added to sys.path: {candidate}")
        try:
            # attempt to import FastAPI app
            from fastapi.testclient import TestClient  # noqa: E402

            try:
                from src.main import app  # noqa: E402

                app_client = TestClient(app)
                report_lines.append("Imported FastAPI app via src.main:app")
                break
            except Exception as e:
                report_lines.append(f"Import src.main failed from {candidate}: {e}")
                # fallthrough to next candidate
        except Exception:
            # fastapi not available or import failed, we'll use requests later
            import_requests = True

if app_client is None:
    # fallback: try live HTTP requests to a running server
    import_requests = True

if import_requests:
    report_lines.append("Falling back to live HTTP checks (localhost)")
    import requests  # type: ignore
    host = os.environ.get('BACKEND_HOST', 'http://127.0.0.1')
    port = os.environ.get('BACKEND_PORT', '8000')
    base = f"{host}:{port}" if not host.startswith('http') else f"{host}:{port}"
    # try /openapi.json and /docs
    app_client = None
    report_lines.append(f"Using base URL: {base}")

# Fetch OpenAPI and run safe GETs
try:
    if app_client is not None:
        client = app_client
        openapi = client.get('/openapi.json')
        if openapi.status_code == 200:
            data = openapi.json()
            title = data.get('info', {}).get('title')
            report_lines.append(f"OpenAPI title: {title}")
            paths = data.get('paths', {})
            report_lines.append(f"Discovered {len(paths)} paths")

            # collect endpoint results for tabular output
            endpoint_rows = []
            skipped_count = 0
            tested_count = 0

            for path, methods in paths.items():
                for method in methods.keys():
                    method_u = method.upper()
                    if method.lower() != 'get':
                        endpoint_rows.append((method_u, path, 'SKIPPED', 'not GET'))
                        skipped_count += 1
                        continue
                    if '{' in path:
                        endpoint_rows.append(('GET', path, 'SKIPPED', 'path params'))
                        skipped_count += 1
                        continue
                    try:
                        res = client.get(path)
                        endpoint_rows.append(('GET', path, str(res.status_code), ''))
                        tested_count += 1
                    except Exception as e:
                        endpoint_rows.append(('GET', path, 'ERROR', str(e)))

            # render markdown report
            md_lines = []
            md_lines.append(f"# Endpoint Check Report")
            md_lines.append("")
            md_lines.append(f"- Run: {run_ts}")
            md_lines.append(f"- OpenAPI: {title}")
            md_lines.append(f"- Paths discovered: {len(paths)}")
            md_lines.append(f"- Endpoints tested: {tested_count}")
            md_lines.append(f"- Endpoints skipped: {skipped_count}")
            md_lines.append("")
            md_lines.append("| Method | Path | Result | Notes |")
            md_lines.append("|---|---|---:|---|")
            for m, pth, result, notes in endpoint_rows:
                md_lines.append(f"| {m} | {pth} | {result} | {notes} |")

            # write the markdown instead of plain lines
            artifacts_dir = Path('artifacts/backend')
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            report_path = artifacts_dir / 'endpoint-check-report.md'
            with report_path.open('w', encoding='utf-8') as f:
                f.write('\n'.join(md_lines))
        else:
            report_lines.append(f"Failed to fetch OpenAPI via TestClient: status {openapi.status_code}")
    else:
        # live HTTP fallback
        import requests  # type: ignore
        host = os.environ.get('BACKEND_HOST', 'http://127.0.0.1')
        port = os.environ.get('BACKEND_PORT', '8000')
        base = f"{host}:{port}" if not host.startswith('http') else f"{host}:{port}"
        # try openapi
        try:
            r = requests.get(f"{base}/openapi.json", timeout=5)
            if r.status_code == 200:
                data = r.json()
                report_lines.append(f"Live OpenAPI title: {data.get('info', {}).get('title')}")
                paths = data.get('paths', {})
                report_lines.append(f"Discovered {len(paths)} paths (live)")
                for path, methods in paths.items():
                    for method in methods.keys():
                        if method.lower() != 'get':
                            report_lines.append(f"SKIP {method.upper()} {path} (not GET)")
                            continue
                        if '{' in path:
                            report_lines.append(f"SKIP GET {path} (path params)")
                            continue
                        try:
                            resp = requests.get(f"{base}{path}", timeout=5)
                            report_lines.append(f"GET {path} -> {resp.status_code}")
                        except Exception as e:
                            report_lines.append(f"GET {path} -> ERROR: {e}")
            else:
                report_lines.append(f"No OpenAPI at {base}/openapi.json (status {r.status_code})")
        except Exception as e:
            report_lines.append(f"Live HTTP check failed: {e}")
except Exception as e:
    report_lines.append(f"Failed to run endpoint discovery: {e}")

# If we reached here and report_path not written by TestClient branch, write a simpler markdown
artifacts_dir = Path('artifacts/backend')
artifacts_dir.mkdir(parents=True, exist_ok=True)
report_path = artifacts_dir / 'endpoint-check-report.md'
if not report_path.exists():
    with report_path.open('w', encoding='utf-8') as f:
        f.write('# Endpoint Check Report\n\n')
        f.write(f'- Run: {run_ts}\n\n')
        f.write('\n'.join(report_lines))

# Append to openlog
openlog_path = artifacts_dir / 'openlog.md'
entry = {
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'summary': 'Automated endpoint discovery run',
    'details': report_lines,
}
if openlog_path.exists():
    with openlog_path.open('a', encoding='utf-8') as f:
        f.write('\n---\n')
        f.write(json.dumps(entry, indent=2))
else:
    with openlog_path.open('w', encoding='utf-8') as f:
        f.write('# Open Log\n')
        f.write(json.dumps(entry, indent=2))

print('Endpoint check complete. Report written to', report_path)
print('OpenLog updated at', openlog_path)
