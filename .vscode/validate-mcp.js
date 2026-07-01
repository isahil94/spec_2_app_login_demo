#!/usr/bin/env node

/**
 * MCP Configuration Validator
 * 
 * Verifies that:
 * 1. mcp.json is valid JSON
 * 2. All required servers are configured
 * 3. Security settings are properly set
 * 4. MCP packages are installed
 * 5. Configuration follows best practices
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const VSCODE_DIR = path.join(__dirname);
const MCP_CONFIG_FILE = path.join(VSCODE_DIR, 'mcp.json');

// Colors for output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

const log = {
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
  header: (msg) => console.log(`\n${colors.cyan}=== ${msg} ===${colors.reset}\n`),
};

let passed = 0;
let failed = 0;
let warnings = 0;

// Test 1: JSON validity
function validateJSON() {
  log.header('JSON Validity');
  try {
    const config = JSON.parse(fs.readFileSync(MCP_CONFIG_FILE, 'utf8'));
    log.success('mcp.json is valid JSON');
    passed++;
    return config;
  } catch (error) {
    log.error(`mcp.json parse error: ${error.message}`);
    failed++;
    process.exit(1);
  }
}

// Test 2: Required fields
function validateRequiredFields(config) {
  log.header('Required Fields');
  
  const requiredFields = ['mcpServers', 'security', 'configuration'];
  
  requiredFields.forEach(field => {
    if (config[field]) {
      log.success(`'${field}' is present`);
      passed++;
    } else {
      log.error(`'${field}' is missing`);
      failed++;
    }
  });
}

// Test 3: Required servers
function validateRequiredServers(config) {
  log.header('Required MCP Servers');
  
  const required = ['filesystem', 'git', 'terminal'];
  
  required.forEach(server => {
    if (config.mcpServers[server]) {
      if (!config.mcpServers[server].disabled) {
        log.success(`${server} is configured and enabled`);
        passed++;
      } else {
        log.warning(`${server} is configured but disabled`);
        warnings++;
      }
    } else {
      log.error(`${server} is not configured`);
      failed++;
    }
  });
}

// Test 4: Security configuration
function validateSecurityConfig(config) {
  log.header('Security Configuration');
  
  const security = config.security || {};
  
  if (security.enableSandboxing !== false) {
    log.success('Sandboxing is enabled');
    passed++;
  } else {
    log.warning('Sandboxing is disabled');
    warnings++;
  }
  
  if (security.logAllAccess !== false) {
    log.success('Access logging is enabled');
    passed++;
  } else {
    log.warning('Access logging is disabled');
    warnings++;
  }
  
  if (security.tlsVerification !== false) {
    log.success('TLS verification is enabled');
    passed++;
  } else {
    log.error('TLS verification is disabled (security risk)');
    failed++;
  }
}

// Test 5: Filesystem server security
function validateFilesystemSecurity(config) {
  log.header('Filesystem Server Security');
  
  const fsServer = config.mcpServers.filesystem || {};
  const security = fsServer.security || {};
  
  if (security.sandboxed) {
    log.success('Filesystem server is sandboxed');
    passed++;
  } else {
    log.error('Filesystem server is not sandboxed');
    failed++;
  }
  
  if (security.allowedPaths && security.allowedPaths.length > 0) {
    log.success(`${security.allowedPaths.length} allowed paths configured`);
    passed++;
  } else {
    log.warning('No allowed paths configured (may cause permission issues)');
    warnings++;
  }
  
  if (security.restrictedPaths && security.restrictedPaths.length > 0) {
    log.success(`${security.restrictedPaths.length} restricted paths configured`);
    passed++;
  } else {
    log.warning('No restricted paths configured');
    warnings++;
  }
}

// Test 6: Terminal server safety
function validateTerminalSecurity(config) {
  log.header('Terminal Server Security');
  
  const termServer = config.mcpServers.terminal || {};
  const security = termServer.security || {};
  
  if (security.sandboxed) {
    log.success('Terminal server is sandboxed');
    passed++;
  } else {
    log.error('Terminal server is not sandboxed (security risk)');
    failed++;
  }
  
  if (security.allowedCommands && security.allowedCommands.length > 0) {
    log.success(`${security.allowedCommands.length} commands allowed`);
    passed++;
  } else {
    log.error('No allowed commands specified (too permissive)');
    failed++;
  }
  
  if (security.restrictedCommands && security.restrictedCommands.length > 0) {
    log.success(`${security.restrictedCommands.length} commands restricted`);
    passed++;
  } else {
    log.error('No restricted commands specified');
    failed++;
  }
  
  if (security.timeout) {
    log.success(`Command timeout: ${security.timeout / 1000}s`);
    passed++;
  } else {
    log.warning('No timeout specified');
    warnings++;
  }
}

// Test 7: Rate limiting
function validateRateLimits(config) {
  log.header('Rate Limiting');
  
  let ratedServers = 0;
  
  Object.entries(config.mcpServers).forEach(([name, server]) => {
    if (!server.disabled && server.rateLimits) {
      ratedServers++;
    }
  });
  
  if (ratedServers > 0) {
    log.success(`${ratedServers} servers have rate limiting configured`);
    passed++;
  } else {
    log.warning('No rate limits configured');
    warnings++;
  }
}

// Test 8: Optional servers status
function validateOptionalServers(config) {
  log.header('Optional Servers Status');
  
  const optional = config.optionalServers || {};
  const enabledOptional = Object.entries(config.mcpServers)
    .filter(([name, server]) => !server.disabled && optional[name])
    .map(([name]) => name);
  
  const disabledCount = Object.keys(optional).length - enabledOptional.length;
  
  log.success(`${disabledCount}/${Object.keys(optional).length} optional servers disabled (secure default)`);
  passed++;
  
  if (enabledOptional.length > 0) {
    log.info(`Enabled optional servers: ${enabledOptional.join(', ')}`);
  }
}

// Test 9: Check MCP packages
function checkMCPPackages() {
  log.header('MCP Packages Installation');
  
  const packages = [
    '@modelcontextprotocol/server-filesystem',
    '@modelcontextprotocol/server-git',
    '@modelcontextprotocol/server-bash',
  ];
  
  packages.forEach(pkg => {
    try {
      execSync(`npm list -g ${pkg}`, { stdio: 'pipe' });
      log.success(`${pkg} is installed globally`);
      passed++;
    } catch {
      log.warning(`${pkg} is not installed globally`);
      log.info(`Install with: npm install -g ${pkg}`);
      warnings++;
    }
  });
}

// Test 10: Configuration schema
function validateSchema(config) {
  log.header('Configuration Schema');
  
  if (config.$schema) {
    log.success('JSON schema is defined');
    passed++;
  } else {
    log.warning('JSON schema is not defined');
    warnings++;
  }
  
  if (config.description) {
    log.success('Description is present');
    passed++;
  } else {
    log.warning('Description is missing');
    warnings++;
  }
  
  if (config.version) {
    log.success(`Version: ${config.version}`);
    passed++;
  } else {
    log.warning('Version is not specified');
    warnings++;
  }
}

// Test 11: Documentation
function validateDocumentation(config) {
  log.header('Documentation');
  
  if (config.documentation) {
    log.success('Documentation section exists');
    passed++;
    
    const docSections = ['overview', 'quickStart', 'securityConsiderations', 'troubleshooting'];
    docSections.forEach(section => {
      if (config.documentation[section]) {
        log.success(`Documentation includes: ${section}`);
        passed++;
      }
    });
  } else {
    log.error('Documentation section is missing');
    failed++;
  }
}

// Main execution
function main() {
  console.clear();
  console.log(`${colors.cyan}MCP Configuration Validator${colors.reset}`);
  console.log(`File: ${MCP_CONFIG_FILE}\n`);
  
  if (!fs.existsSync(MCP_CONFIG_FILE)) {
    log.error(`mcp.json not found at ${MCP_CONFIG_FILE}`);
    process.exit(1);
  }
  
  const config = validateJSON();
  validateRequiredFields(config);
  validateRequiredServers(config);
  validateSecurityConfig(config);
  validateFilesystemSecurity(config);
  validateTerminalSecurity(config);
  validateRateLimits(config);
  validateOptionalServers(config);
  checkMCPPackages();
  validateSchema(config);
  validateDocumentation(config);
  
  // Summary
  log.header('Summary');
  console.log(`${colors.green}Passed: ${passed}${colors.reset}`);
  console.log(`${colors.yellow}Warnings: ${warnings}${colors.reset}`);
  console.log(`${colors.red}Failed: ${failed}${colors.reset}\n`);
  
  if (failed === 0) {
    log.success('MCP configuration is valid and production-ready!');
    process.exit(0);
  } else {
    log.error('MCP configuration has errors. Please fix them before deployment.');
    process.exit(1);
  }
}

main();
