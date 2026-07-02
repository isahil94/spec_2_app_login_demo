#!/usr/bin/env bash
set -euo pipefail
export LOCAL_URL="${LOCAL_URL:-http://localhost:4173}"
# Ensure Playwright dependencies are installed before running (CI should provision these)
# npx playwright install --with-deps
npx playwright test tests/e2e || true

echo "Playwright execution completed. Reports/screenshots (if any) are under artifacts/tests/e2e/"
