# Run Instructions Template

Describe how to run and test the component. Agents should render this template into `artifacts/<stage>/run_instructions.md`.

## Environment
- Python: {{ python_version | default('3.11') }}
- Virtualenv path: {{ venv_path | default('.venv') }}

## Bootstrap
```powershell
{{ bootstrap_commands }}
```

## Run dev server
```powershell
{{ run_server_command }}
```

## Run tests
```powershell
{{ test_command }}
```

## Notes
- {{ notes | default('No special notes') }}
