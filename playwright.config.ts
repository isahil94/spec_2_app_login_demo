const config = {
  testDir: 'tests/e2e',
  timeout: 30000,
  use: {
    baseURL: process.env.LOCAL_URL || 'http://localhost:4173',
    headless: true,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'retain-on-failure',
    locale: 'en-US',
  },
  reporter: [['list'], ['html', { outputFolder: 'artifacts/tests/e2e/playwright-report' }]],
  outputDir: 'artifacts/tests/e2e/screenshots',
};

module.exports = config;
