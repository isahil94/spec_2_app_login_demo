const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', (msg) => console.log('console:', msg.type(), msg.text()));
  page.on('requestfailed', (req) => console.log('requestfailed:', req.url(), req.failure()?.errorText));
  page.on('response', (res) => {
    if (res.url().includes('/auth/login') || res.url().includes('/dashboard/metrics')) {
      console.log('response:', res.status(), res.url());
    }
  });

  await page.goto('http://localhost:4173/login', { waitUntil: 'domcontentloaded' });
  console.log('title:', await page.title());
  await page.fill('input[type="email"]', 'tempuser@example.com');
  await page.fill('input[type="password"]', 'Pass123!');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(5000);
  console.log('url after:', page.url());
  console.log('body snippet:', (await page.textContent('body')).slice(0, 1000));
  await browser.close();
})();
