const fs = require('fs');
const path = require('path');

// Parses a markdown table into an array of row-objects.
// Expects a GitHub-flavored table: | Col A | Col B | ... |
function parseMarkdownTable(md, headerMustInclude) {
  const lines = md.split('\n');
  const rows = [];
  let headers = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line.startsWith('|')) continue;

    const cells = line.split('|').slice(1, -1).map(c => c.trim());

    // skip separator rows like |---|---|
    if (cells.every(c => /^:?-+:?$/.test(c))) continue;

    if (!headers) {
      if (headerMustInclude && !cells.some(c => c.includes(headerMustInclude))) continue;
      headers = cells;
      continue;
    }

    const row = {};
    headers.forEach((h, idx) => { row[h] = cells[idx] || ''; });
    rows.push(row);
  }
  return rows;
}

function parseOpenlog(openlogPath, fieldNames) {
  if (!fs.existsSync(openlogPath)) {
    return { exists: false, items: [], criticalBlocking: [] };
  }
  const md = fs.readFileSync(openlogPath, 'utf8');

  // Try to find an "Open Questions" style table first (Blocking / Approval Required / Status columns)
  const rows = parseMarkdownTable(md, fieldNames.status);

  const criticalBlocking = rows.filter(r =>
    (r[fieldNames.blocking] || '').toLowerCase() === 'yes' &&
    (r[fieldNames.approval_required] || '').toLowerCase() === 'yes' &&
    (r[fieldNames.status] || '').toUpperCase() === 'WAITING_FOR_APPROVAL'
  );

  return { exists: true, items: rows, criticalBlocking, raw: md };
}

function countArtifacts(artifactDir, requiredList, repoRoot) {
  const missing = [];
  const present = [];
  for (const rel of requiredList) {
    const p = path.join(repoRoot, artifactDir, rel);
    if (fs.existsSync(p)) present.push(rel);
    else missing.push(rel);
  }
  return { present, missing, total: requiredList.length, presentCount: present.length };
}

module.exports = { parseOpenlog, countArtifacts, parseMarkdownTable };