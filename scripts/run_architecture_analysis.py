"""Run a deeper static analysis on a repository and produce an enriched Architecture Document.

Usage:
  python scripts/run_architecture_analysis.py --repo F:\\Projects\\Specs_to_APP\\

Output:
  analysis-outputs/architecture-document-detailed.md
"""
from pathlib import Path
import argparse
import os
import ast
import re
from collections import defaultdict

PY_EXTS = {'.py'}
JS_EXTS = {'.js', '.ts', '.tsx', '.jsx'}
MD_EXTS = {'.md'}

ROUTE_PATTERN = re.compile(r"@\s*(?:[\w\.]+)\.(get|post|put|delete|patch|options|head)\b")
APP_ROUTE_PATTERN = re.compile(r"@\s*(?:app|router)\.(get|post|put|delete|patch|options|head)\b")


def validate_repo(path: Path):
    if not path.exists():
        raise SystemExit(f"ERROR: Repository not found: {path}")
    if not path.is_dir():
        raise SystemExit(f"ERROR: Path is not a directory: {path}")
    # check for at least one source file
    has_source = any(path.rglob('*.py')) or any(path.rglob('*.js')) or any(path.rglob('*.ts')) or any(path.rglob('*.md'))
    if not has_source:
        raise SystemExit("ERROR: Repository contains no source files.")


def scan_repo(path: Path):
    stats = {
        'total_files': 0,
        'total_folders': 0,
        'by_ext': defaultdict(int),
        'python_files': [],
        'markdown_files': [],
    }
    for root, dirs, files in os.walk(path):
        stats['total_folders'] += len(dirs)
        for f in files:
            stats['total_files'] += 1
            ext = Path(f).suffix.lower()
            stats['by_ext'][ext] += 1
            full = Path(root) / f
            if ext in PY_EXTS:
                stats['python_files'].append(full)
            if ext in MD_EXTS:
                stats['markdown_files'].append(full)
    return stats


def analyze_python_files(py_files):
    counts = {
        'classes': 0,
        'functions': 0,
        'methods': 0,
        'models': 0,
        'routes': 0,
        'class_defs': [],
    }
    for p in py_files:
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        # quick heuristics for routes
        if ROUTE_PATTERN.search(text) or APP_ROUTE_PATTERN.search(text):
            counts['routes'] += len(ROUTE_PATTERN.findall(text)) or len(APP_ROUTE_PATTERN.findall(text))
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                counts['classes'] += 1
                base_names = [getattr(b, 'id', getattr(b, 'attr', None)) for b in node.bases if b is not None]
                counts['class_defs'].append((node.name, [bn for bn in base_names if bn]))
                # heuristics: SQLAlchemy model if has __tablename__ or Column in body
                is_model = False
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if getattr(target, 'id', None) == '__tablename__':
                                is_model = True
                    if isinstance(stmt, ast.Expr):
                        # check for Column(...) usage in expressions
                        if isinstance(stmt.value, ast.Call):
                            fname = getattr(stmt.value.func, 'id', None) or getattr(stmt.value.func, 'attr', None)
                            if fname == 'Column':
                                is_model = True
                    if isinstance(stmt, ast.AnnAssign):
                        # annotated assignment e.g., id: Mapped[int] = mapped_column(...)
                        if isinstance(stmt.annotation, ast.Subscript) or isinstance(stmt.annotation, ast.Name):
                            # weak heuristic
                            pass
                if is_model:
                    counts['models'] += 1
            if isinstance(node, ast.FunctionDef):
                counts['functions'] += 1
                # methods are functions inside class defs; detect by parent relationship is complex — heuristic: if name has self arg
                if node.args.args:
                    first = node.args.args[0].arg
                    if first == 'self':
                        counts['methods'] += 1
    return counts


def render_class_diagram(class_defs):
    if not class_defs:
        return 'Not detected.'
    lines = ['```mermaid', 'classDiagram']
    for name, bases in class_defs:
        lines.append(f'    class {name}')
        for b in bases:
            if b:
                lines.append(f'    {b} <|-- {name}')
    lines.append('```')
    return '\n'.join(lines)


def render_flowchart():
    chart = [
        '```mermaid',
        'flowchart LR',
        '  SRS["SRS + optional Figma"] --> Supervisor',
        '  Supervisor --> Agents[Agents & Skills]',
        '  Agents --> Artifacts[Artifacts Store]',
        '  Artifacts --> Apps[Generated Apps]',
        '  Apps --> Database[(Persistence)]',
        '  Supervisor --> Observability',
        '  Supervisor --> Validation[Validation & Approval]',
        '```'
    ]
    return '\n'.join(chart)


def generate_markdown(path: Path, stats, py_counts, class_diagram):
    out = []
    out.append(f'# Architecture Document — {path.name}\n')
    out.append('## Summary\n')
    out.append(f'- Total files: {stats["total_files"]}')
    out.append(f'- Total folders (approx): {stats["total_folders"]}')
    out.append('\n')
    out.append('## File types detected\n')
    for ext, cnt in sorted(stats['by_ext'].items(), key=lambda x: -x[1]):
        out.append(f'- {ext or "(no ext)"}: {cnt}')
    out.append('\n')
    out.append('## Python analysis\n')
    out.append(f'- Python files analyzed: {len(stats["python_files"]) }')
    out.append(f'- Classes: {py_counts["classes"]}')
    out.append(f'- Functions: {py_counts["functions"]}')
    out.append(f'- Methods (heuristic): {py_counts["methods"]}')
    out.append(f'- Detected SQLAlchemy-like models (heuristic): {py_counts["models"]}')
    out.append(f'- Detected FastAPI-like routes (heuristic): {py_counts["routes"]}')
    out.append('\n')
    out.append('## Class relationships\n')
    out.append(class_diagram)
    out.append('\n')
    out.append('## Execution flow\n')
    out.append(render_flowchart())
    out.append('\n')
    out.append('Generated by run_architecture_analysis.py\n')
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', '-r', required=True, help='Path to repository')
    args = parser.parse_args()
    repo = Path(args.repo)
    validate_repo(repo)
    stats = scan_repo(repo)
    py_counts = analyze_python_files(stats['python_files'])
    class_diagram = render_class_diagram(py_counts.get('class_defs', []))

    out_dir = repo / 'analysis-outputs'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_md = out_dir / 'architecture-document-detailed.md'
    content = generate_markdown(repo, stats, py_counts, class_diagram)
    out_md.write_text(content, encoding='utf-8')
    print(f'Wrote {out_md}')


if __name__ == '__main__':
    main()
