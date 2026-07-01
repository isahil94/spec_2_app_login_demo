# Browser Tool

Automate browser interactions and validate UI functionality.

---

## Purpose

Provide agents with the ability to automate browser interactions, capture screenshots, validate UI elements, and perform browser-based testing.

---

## When to Use

- Testing web application UI
- Capturing screenshots for documentation
- Validating form functionality
- Testing user workflows
- Checking responsive design
- Automating browser testing
- Visual regression testing
- End-to-end testing

---

## Available Operations

### Navigation
- Navigate to URL
- Go back/forward
- Reload page
- Wait for page load

### Interaction
- Click elements
- Type text
- Submit forms
- Select dropdown options
- Handle dialogs
- Upload files

### Inspection
- Get element text
- Get element attributes
- Find elements by selector
- Check element visibility
- Get page title/URL

### Screenshot Capture
- Screenshot entire page
- Screenshot specific element
- Full page scroll screenshot
- Viewport screenshot

### Validation
- Assert element present
- Assert text visible
- Assert element enabled
- Compare screenshots

### Performance
- Measure page load time
- Get performance metrics
- Measure interaction time

---

## Inputs

### Navigation
- **URL** (required): URL to navigate to
- **Wait** (optional): Wait time for page load

### Interaction
- **Selector** (required): CSS selector or XPath
- **Action** (required): click/type/select/submit
- **Value** (optional): Value for type/select actions

### Screenshot
- **Selector** (optional): Specific element (default: full page)
- **Format** (optional): png/jpeg (default: png)
- **Viewport** (optional): Include viewport info

### Validation
- **Selector** (required): Element selector
- **Check** (required): present/visible/enabled/text/attribute
- **Expected** (optional): Expected value for validation

---

## Outputs

### Navigation Output
- **URL**: Current page URL
- **Title**: Page title
- **Status**: Success/failure
- **Load Time**: Page load duration

### Interaction Output
- **Status**: Action succeeded
- **Result**: Element state after interaction
- **Screenshot**: Optional screenshot

### Screenshot Output
- **File**: Screenshot file path
- **Size**: Image dimensions
- **Format**: Image format (png/jpeg)

### Validation Output
- **Result**: Pass/fail
- **Actual**: Actual value found
- **Expected**: Expected value
- **Details**: Validation details

---

## Dependencies

- **Playwright MCP Server** - Provides browser automation
- **Browser (Chrome/Firefox/Safari)** - Browser engine
- **VS Code Extension** - Browser automation support

**Note:** Browser tool is optional and disabled by default. Enable in `.vscode/mcp.json` if needed.

---

## Execution

**Method:** Playwright MCP Server

**How it works:**
1. Agent specifies browser operation
2. Playwright MCP server launches browser
3. Operation executes in browser
4. Results captured
5. Output returned to agent

**Supported browsers:** Chrome, Firefox, Safari, Edge via Playwright

---

## Constraints

- Requires graphical display or virtual display
- Browser automation is slow (not suitable for large-scale testing)
- Limited to web applications
- Cannot interact with native elements outside browser
- Screenshots may vary by browser
- Interactive tests may fail in headless mode

---

## Best Practices

### Test Structure
- Use page objects for complex applications
- Keep tests focused and atomic
- Use explicit waits instead of sleeps
- Validate state changes, not implementation
- Clean up after tests

### Selectors
- Use stable, semantic selectors
- Avoid brittle xpaths
- Prefer data-testid attributes
- Use role selectors for accessibility
- Document selector rationale

### Screenshot Testing
- Use for documentation only
- Don't rely on pixel-perfect matching
- Compare visual snapshots carefully
- Update baselines when UI changes
- Version control baseline images

### Performance
- Use headless mode when possible
- Run tests in parallel when safe
- Reuse browser instances
- Cache page resources
- Monitor test execution time

### Accessibility
- Test keyboard navigation
- Validate ARIA attributes
- Check color contrast
- Test screen reader compatibility
- Validate form labels

---

## Error Handling

### Common Failures

**Element Not Found**
- Cause: Selector doesn't match any element
- Recovery: Verify selector, inspect page, check timing
- Log: Selector and suggested alternatives

**Timeout**
- Cause: Element takes too long to appear
- Recovery: Increase timeout, check loading state
- Log: Element selector and timeout value

**Stale Element**
- Cause: Element no longer in DOM
- Recovery: Re-find element, check DOM changes
- Log: Element selector and DOM change info

**Navigation Failed**
- Cause: URL unreachable or error
- Recovery: Check URL, verify server, check network
- Log: URL and HTTP status

**Browser Crash**
- Cause: Browser process crashed
- Recovery: Restart browser, check for issues
- Log: Crash details and browser logs

**Screenshot Failed**
- Cause: Cannot capture screenshot
- Recovery: Check permissions, verify display
- Log: Screenshot operation and error

---

## Tool Integration Examples

### Navigate to Application
```
Browser: Navigate to
URL: http://localhost:3000
Purpose: Load application
Output: Page title, URL
```

### Fill and Submit Form
```
Browser: Type text
Selector: #email
Value: user@example.com
Purpose: Enter email
Output: Element value
```

### Capture Screenshot
```
Browser: Screenshot
Selector: #form
Format: png
Purpose: Document UI
Output: Screenshot file
```

### Validate Form Submission
```
Browser: Assert element present
Selector: .success-message
Purpose: Verify form submitted
Output: Pass/fail
```

---

## See Also

- **Testing Tool** - For automated testing
- **Documentation Tool** - For capturing UI documentation
- **Terminal Tool** - For starting application servers

Reference: `shared.md` for common guidance on UI automation best practices.
