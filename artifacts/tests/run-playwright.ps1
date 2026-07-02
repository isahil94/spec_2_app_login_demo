param(
    [string]$LocalUrl = 'http://localhost:4173'
)
$env:LOCAL_URL = $LocalUrl
# Ensure Playwright is installed in the environment: npx playwright install
npx playwright test tests/e2e
Write-Host "Playwright execution completed. Reports/screenshots (if any) are under artifacts/tests/e2e/" 
