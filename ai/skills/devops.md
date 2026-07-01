# DevOps Skills

This document defines reusable capabilities for the DevOps & Release agent in building, testing, and deploying applications.

---

## Skill: Build Project

### Purpose
Automate the compilation, packaging, and preparation of application artifacts for testing and deployment.

### When to Use
- Compiling source code
- Running build processes
- Creating executable artifacts
- Preparing code for testing

### Inputs
- `source_code` (object): Code to build
- `build_configuration` (object): Build configuration
- `dependencies` (array): Build dependencies
- `build_targets` (array): What to build (debug, release, etc.)
- `artifacts_dir` (string, optional): Where to store build artifacts

### Outputs
- `build_artifacts` (array): Built application files
- `build_log` (string): Build process log
- `build_status` (string): Success or failure status
- `artifact_info` (object): Information about artifacts
- `build_time` (number): Time to build in seconds

### Dependencies
- Source code available
- Build tools available (scripts/build.py)
- Dependencies resolvable

### Execution Steps
1. Clean previous build artifacts
2. Resolve dependencies
3. Validate source code
4. Compile source code
5. Run build scripts (scripts/build.py)
6. Package artifacts
7. Verify artifact integrity
8. Generate build manifest
9. Log build process
10. Publish build status

### Validation Checklist
- [ ] Build completes without errors
- [ ] All dependencies resolved
- [ ] Artifacts generated correctly
- [ ] Build time reasonable
- [ ] Build is reproducible
- [ ] Build log captures all info

### Success Criteria
- Build succeeds
- Artifacts generated
- Ready for testing
- Build is repeatable
- Build is fast enough

### Failure Conditions
- Build fails
- Dependencies missing
- Artifacts corrupted
- Build too slow
- Build not reproducible

---

## Skill: Run Quality Checks

### Purpose
Execute automated quality checks including linting, testing, and code analysis to ensure code meets standards before deployment.

### When to Use
- Validating code quality
- Running automated tests
- Checking coding standards
- Analyzing code for issues

### Inputs
- `code` (object): Code to check
- `check_types` (array): What to check (lint, test, security, etc.)
- `quality_thresholds` (object): Minimum acceptable levels
- `configuration` (object, optional): Tool configuration

### Outputs
- `quality_report` (object): Overall quality assessment
- `check_results` (array): Results of each check
- `issues_found` (array): List of issues
- `quality_score` (number): Overall quality score
- `check_log` (string): Details of checks run

### Dependencies
- Quality checking tools available (scripts/lint.py, scripts/test.py)
- Code available
- Thresholds defined

### Execution Steps
1. Run linting checks (scripts/lint.py)
2. Run unit tests (scripts/test.py)
3. Run code coverage analysis
4. Run security checks
5. Run performance checks if applicable
6. Aggregate results
7. Calculate quality score
8. Generate quality report
9. Compare against thresholds
10. Report pass/fail status

### Validation Checklist
- [ ] All checks complete
- [ ] Quality score calculated
- [ ] Issues clearly identified
- [ ] Thresholds enforced
- [ ] Report is actionable
- [ ] Checks are deterministic

### Success Criteria
- All checks pass
- Quality score meets threshold
- No critical issues
- Ready for next stage
- Quality trend improving

### Failure Conditions
- Checks fail
- Quality below threshold
- Critical issues found
- Cannot determine issues
- Checks unreliable

---

## Skill: Package Application

### Purpose
Create distributable application packages ready for deployment to target environments.

### When to Use
- Creating Docker images
- Creating release packages
- Preparing for deployment
- Creating artifacts for distribution

### Inputs
- `build_artifacts` (array): Built application files
- `configuration` (object): Packaging configuration
- `target_environment` (string): Where package will run (docker, linux, windows, etc.)
- `version_info` (object): Version and metadata
- `dependencies` (array, optional): Runtime dependencies

### Outputs
- `packages` (array): Created application packages
- `package_metadata` (object): Package information
- `package_manifests` (array): What's in each package
- `package_checksums` (object): Integrity verification
- `deployment_instructions` (string): How to use packages

### Dependencies
- Build artifacts available
- Packaging tools installed
- Configuration defined

### Execution Steps
1. Prepare package structure
2. Copy build artifacts into package
3. Add runtime dependencies
4. Add configuration templates
5. Add startup scripts
6. Create package metadata
7. Generate checksums
8. Verify package contents
9. Test package can be unpacked
10. Document package contents

### Validation Checklist
- [ ] Package contains all files
- [ ] Package size reasonable
- [ ] Checksums calculated
- [ ] Package can be extracted
- [ ] All dependencies included
- [ ] Metadata is correct

### Success Criteria
- Packages created successfully
- Packages ready for deployment
- Checksums verify integrity
- Package size acceptable
- All files present

### Failure Conditions
- Package creation fails
- Files missing from package
- Checksums don't match
- Package corrupted
- Cannot deploy package

---

## Skill: Local Deployment

### Purpose
Deploy application to local development or staging environments for testing and validation.

### When to Use
- Setting up development environment
- Testing deployment procedures
- Validating configuration
- Running application locally

### Inputs
- `package` (object): Application package
- `environment_config` (object): Environment-specific configuration
- `target_environment` (string): Development, staging, etc.
- `deployment_scripts` (array, optional): Custom deployment steps

### Outputs
- `deployment_status` (string): Success or failure
- `deployment_log` (string): Deployment process log
- `deployment_info` (object): Application location and endpoints
- `verification_status` (boolean): Whether verification passed
- `deployment_summary` (object): Summary of what was deployed

### Dependencies
- Application package available
- Target environment accessible
- Configuration available

### Execution Steps
1. Validate deployment prerequisites
2. Prepare deployment environment
3. Extract application package
4. Install or copy application
5. Configure application
6. Start application
7. Run health checks
8. Verify application responds
9. Log deployment details
10. Report deployment status

### Validation Checklist
- [ ] Deployment succeeds
- [ ] Application starts
- [ ] Application is accessible
- [ ] Configuration correct
- [ ] Health checks pass
- [ ] Logs show normal operation

### Success Criteria
- Application deploys successfully
- Application starts and runs
- Health checks pass
- Application accessible
- Ready for testing

### Failure Conditions
- Deployment fails
- Application won't start
- Health checks fail
- Configuration incorrect
- Cannot access application
