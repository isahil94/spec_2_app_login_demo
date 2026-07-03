import pathlib
import re

import yaml

root = pathlib.Path(__file__).resolve().parent.parent
matrix = {}
headers = None
with open(root / 'ai' / 'contracts' / 'artifact-ownership-matrix.md', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('| Artifact |'):
            headers = [h.strip() for h in line.split('|')[1:-1]]
            continue
        if line.startswith('|---'):
            continue
        if headers and line.startswith('|') and 'Artifact' not in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) != len(headers):
                continue
            artifact = parts[0]
            norm = re.sub(r'[^a-z0-9]+', '_', artifact.lower()).strip('_')
            row = {headers[i]: parts[i] for i in range(1, len(headers))}
            matrix[norm] = {'artifact': artifact, 'row': row}
            matrix[artifact.lower().rstrip('.md')] = {'artifact': artifact, 'row': row}
            matrix[artifact.lower().replace('-', '_').rstrip('.md')] = {'artifact': artifact, 'row': row}
            matrix[artifact.lower().replace('_', '').rstrip('.md')] = {'artifact': artifact, 'row': row}

agents = sorted((root / '.github' / 'agents').glob('*.md'))
for path in agents:
    text = path.read_text(encoding='utf-8')
    m = re.search(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        print(f'{path.name}: no frontmatter')
        continue
    data = yaml.safe_load(m.group(1))
    agent_id = (data.get('id') or path.stem).lower()
    print(f'== {path.name} ({agent_id}) ==')
    consumes = data.get('consumes', []) or []
    produces = data.get('produces', []) or []
    if isinstance(consumes, str):
        consumes = [consumes]
    if isinstance(produces, str):
        produces = [produces]
    for art in consumes:
        raw = str(art).lower()
        candidates = [re.sub(r'[^a-z0-9]+', '_', raw).strip('_'), raw.rstrip('.md'), raw.replace('-', '_').rstrip('.md'), raw.replace('_', '').rstrip('.md')]
        artn = next((c for c in candidates if c in matrix), None)
        if artn is None:
            print(f'  CONSUMES UNKNOWN ARTIFACT: {art} -> {candidates}')
            continue
        status = matrix[artn]['row'].get(agent_id.upper())
        if status not in ('CONSUME', 'EXTEND', 'REFERENCE'):
            print(f'  CONSUMES mismatch: {art} status {status} (matrix artifact {matrix[artn]["artifact"]})')
    for art in produces:
        raw = str(art).lower()
        candidates = [re.sub(r'[^a-z0-9]+', '_', raw).strip('_'), raw.rstrip('.md'), raw.replace('-', '_').rstrip('.md'), raw.replace('_', '').rstrip('.md')]
        artn = next((c for c in candidates if c in matrix), None)
        if artn is None:
            print(f'  PRODUCES UNKNOWN ARTIFACT: {art} -> {candidates}')
            continue
        status = matrix[artn]['row'].get(agent_id.upper())
        if status != 'OWN':
            print(f'  PRODUCES mismatch: {art} status {status} (matrix artifact {matrix[artn]["artifact"]})')
