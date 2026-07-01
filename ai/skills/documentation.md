# Documentation Skills

This document defines reusable capabilities for the Documentation agent in creating user and technical documentation.

---

## Skill: Generate README

### Purpose
Create a comprehensive README that provides quick start, installation, and overview information for developers and users.

### When to Use
- Creating initial project documentation
- Documenting project setup
- Providing usage overview
- Publishing to repositories

### Inputs
- `project_info` (object): Project name, description, purpose
- `features` (array): Key features to document
- `installation_steps` (array): How to install/set up
- `quick_start` (object): Quick start guide steps
- `technology_stack` (array): Technologies used
- `contributing_guidelines` (object, optional): How to contribute

### Outputs
- `readme_content` (string): Formatted README markdown
- `readme_file` (object): README.md ready to publish
- `sections` (object): Individual sections
- `table_of_contents` (array): Linked TOC

### Dependencies
- Project information available
- Features documented
- Installation procedure clear

### Execution Steps
1. Write project overview
2. Add features list
3. Document installation steps
4. Create quick start guide
5. Document usage examples
6. List technology stack
7. Provide troubleshooting section
8. Add contribution guidelines if applicable
9. Create table of contents
10. Add links to detailed documentation

### Validation Checklist
- [ ] Overview is clear and compelling
- [ ] Installation steps are complete
- [ ] Quick start actually works
- [ ] Examples are accurate
- [ ] Links are functional
- [ ] Formatting is consistent
- [ ] Tone matches audience

### Success Criteria
- README provides quick overview
- Installation steps are clear
- Quick start works for new users
- Examples are correct
- Links to detailed documentation

### Failure Conditions
- README incomplete or outdated
- Installation steps wrong
- Quick start doesn't work
- Examples incorrect
- Dead links

---

## Skill: Generate API Documentation

### Purpose
Create comprehensive API reference documentation that enables developers to integrate with the API effectively.

### When to Use
- Documenting REST or GraphQL APIs
- Creating endpoint reference
- Documenting request/response formats
- Providing integration examples

### Inputs
- `api_spec` (object): API specification (OpenAPI, etc.)
- `endpoints` (array): API endpoints
- `data_models` (object): Data models/schemas
- `authentication` (object): Auth requirements
- `examples` (array): Usage examples

### Outputs
- `api_documentation` (string): Complete API docs
- `endpoint_docs` (array): Per-endpoint documentation
- `schema_docs` (object): Data model documentation
- `examples` (array): Code examples
- `api_reference` (object): Quick reference

### Dependencies
- API specification available
- Endpoints defined
- Data models documented

### Execution Steps
1. Generate overview of API
2. Document authentication/authorization
3. Document base URL and versioning
4. Document each endpoint with:
   - Method and path
   - Parameters
   - Request/response formats
   - Example requests/responses
   - Error responses
5. Document data models/schemas
6. Provide code examples in multiple languages
7. Document rate limiting if applicable
8. Provide troubleshooting section
9. Create quick reference guide

### Validation Checklist
- [ ] All endpoints documented
- [ ] Examples are accurate
- [ ] Data models clearly defined
- [ ] Error responses documented
- [ ] Authentication explained
- [ ] Examples work
- [ ] Formatting consistent

### Success Criteria
- Developers can integrate from docs
- All endpoints have examples
- Error responses documented
- Code examples work
- Documentation is searchable

### Failure Conditions
- Incomplete endpoint documentation
- Incorrect examples
- Missing data models
- Error responses unclear
- Examples don't work

---

## Skill: Generate User Guide

### Purpose
Create step-by-step guides that help users accomplish their goals using the application or system.

### When to Use
- Documenting user workflows
- Creating task-based guides
- Explaining features
- Providing troubleshooting help

### Inputs
- `features` (array): Features to document
- `user_workflows` (array): User tasks/workflows
- `user_personas` (array, optional): User types
- `screenshots` (array, optional): UI screenshots
- `troubleshooting` (array, optional): Common issues

### Outputs
- `user_guide` (string): Complete user guide
- `task_guides` (array): Step-by-step task guides
- `feature_docs` (object): Feature documentation
- `troubleshooting_guide` (object): FAQ and troubleshooting
- `user_guide_pdf` (object): Formatted for download

### Dependencies
- Features documented
- Workflows understood
- UI/UX finalized

### Execution Steps
1. Identify key user tasks
2. Write step-by-step guides for each task
3. Include screenshots/diagrams
4. Explain feature benefits
5. Provide troubleshooting steps
6. Create FAQ section
7. Add quick tips and tricks
8. Create glossary if needed
9. Provide contact/support info
10. Format for readability

### Validation Checklist
- [ ] Steps are clear and complete
- [ ] Screenshots are current
- [ ] Language is user-friendly
- [ ] Common tasks covered
- [ ] Troubleshooting covers common issues
- [ ] Format is readable
- [ ] Navigation is clear

### Success Criteria
- Users can complete tasks from guide
- Users understand features
- Common issues resolved via troubleshooting
- Reduces support requests
- Users feel confident

### Failure Conditions
- Steps incomplete or unclear
- Screenshots outdated
- Important tasks missing
- Troubleshooting inadequate
- Language too technical

---

## Skill: Generate Deployment Guide

### Purpose
Provide clear instructions for deploying the application or system to production environments.

### When to Use
- Creating deployment procedures
- Documenting environment setup
- Planning production deployment
- Creating runbooks for operations

### Inputs
- `deployment_architecture` (object): Deployment topology
- `environments` (array): Target environments (dev, staging, prod)
- `requirements` (array): System requirements
- `configuration` (object): Environment configuration
- `procedures` (array, optional): Step-by-step procedures
- `monitoring` (object, optional): Monitoring setup

### Outputs
- `deployment_guide` (string): Complete deployment guide
- `environment_setup` (array): Per-environment setup
- `deployment_procedures` (array): Deployment steps
- `rollback_procedures` (array): How to rollback
- `monitoring_guide` (object): Post-deployment monitoring

### Dependencies
- Deployment architecture designed
- System requirements documented
- Configuration procedure clear

### Execution Steps
1. Document system requirements
2. Document environment setup for each target
3. Create pre-deployment checklist
4. Write deployment procedure
5. Document configuration steps
6. Include verification steps
7. Document monitoring setup
8. Create rollback procedures
9. Document troubleshooting
10. Create post-deployment checklist

### Validation Checklist
- [ ] Requirements are complete
- [ ] Environment setup is clear
- [ ] Deployment steps are detailed
- [ ] Verification steps included
- [ ] Rollback procedures documented
- [ ] Monitoring configured
- [ ] Support contacts listed

### Success Criteria
- Deployment proceeds smoothly
- All verification steps pass
- System starts and functions
- Monitoring active
- Deployment team confident

### Failure Conditions
- Deployment fails
- Verification steps fail
- Cannot diagnose issues
- Rollback needed but unclear
- Monitoring not working
