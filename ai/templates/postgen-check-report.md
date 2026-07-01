# Post-generation Check Report Template

This template is rendered by agents after running `scripts/postgen_check.py` or equivalent validations.

## Summary
- Stage: {{ stage }}
- Status: {{ status }}
- Issues Found: {{ issues | length }}

## Details
{% for issue in issues %}
- {{ issue.code }}: {{ issue.description }}
  - Path: {{ issue.path }}
  - Severity: {{ issue.severity }}
  - Auto-fix: {{ issue.auto_fix | default('none') }}
{% endfor %}

## Actions
- {{ actions | default('No actions recorded') }}
