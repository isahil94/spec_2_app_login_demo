# Documentation Tool

Generate, validate, and maintain project documentation.

---

## Purpose

Provide agents with the ability to generate documentation, validate documentation completeness, update README files, and maintain documentation accuracy.

---

## When to Use

- Generating API documentation
- Updating README files
- Creating architecture documentation
- Validating documentation is complete
- Generating changelog entries
- Creating user guides
- Documenting CLI interfaces
- Generating developer guides

---

## Available Operations

### Documentation Generation
- Generate API documentation from code
- Generate architecture diagrams
- Generate changelog
- Generate CLI help documentation
- Generate configuration documentation

### Documentation Validation
- Validate README exists and has content
- Check for broken links
- Validate documentation structure
- Check for outdated references
- Validate markdown formatting

### README Operations
- Read README
- Update README sections
- Add table of contents
- Update badges/status

### Metadata Documentation
- Document configuration files
- Document environment variables
- Document project structure
- Document dependencies

### Artifact Management
- Generate documentation artifacts
- Archive documentation
- Create snapshots

---

## Inputs

### Generation
- **Type** (required): API/Architecture/Changelog/Guide
- **Source** (optional): Source files or modules
- **Output** (required): Output file or directory
- **Format** (optional): Markdown/HTML/PDF

### Validation
- **Path** (required): Documentation path
- **Check Type** (optional): Structure/Links/Format/Completeness

### README Update
- **Section** (required): Section to update
- **Content** (required): New content
- **Append** (optional): Append vs. replace

---

## Outputs

### Generated Documentation
- **Content**: Generated documentation
- **File Path**: Output file location
- **Size**: Generated content size
- **Format**: Documentation format

### Validation Report
- **Valid**: Boolean indicating if documentation valid
- **Issues**: List of validation issues
- **Suggestions**: Recommendations for improvement
- **Coverage**: Documentation coverage percentage

### README Output
- **Updated**: Section updated
- **Path**: README file location
- **Changes**: Number of lines changed

---

## Dependencies

- **Existing Helper Scripts** - Python documentation tools
- **Terminal MCP** - For running documentation generators
- **Filesystem Tool** - For reading/writing documentation
- **Code Analysis** - For extracting documentation from code

---

## Execution

**Method:** Terminal MCP + Filesystem Tool

**How it works:**
1. Agent specifies documentation operation
2. Generator tool (if needed) executes
3. Documentation generated or validated
4. Files written to appropriate locations
5. Results returned to agent

**Supported generators:** Markdown, docstrings parsing

---

## Constraints

- Documentation must be in Markdown (primary format)
- Generated documentation overwrites existing files
- Validation checks for consistency
- Large projects may have extensive documentation
- Links must be relative to project root
- All paths relative to documentation root

---

## Best Practices

### Documentation Quality
- Keep documentation current with code
- Write clear, concise descriptions
- Use consistent formatting
- Include examples where helpful
- Document edge cases and limitations

### README Structure
- Start with project description
- Include table of contents (for long READMEs)
- Provide quick start instructions
- Include usage examples
- Document configuration options
- Link to detailed documentation

### API Documentation
- Document all public APIs
- Include parameter descriptions
- Document return values
- Provide usage examples
- Note any exceptions

### Maintenance
- Review documentation during code reviews
- Update when functionality changes
- Keep changelog current
- Archive old versions
- Link related documentation

### Markdown Standards
- Use consistent heading hierarchy (# ## ###)
- Use code blocks for examples
- Use lists for clarity
- Include links to related docs
- Ensure all links are valid

---

## Error Handling

### Common Failures

**Generator Error**
- Cause: Documentation generator failed
- Recovery: Check source files, fix issues, retry
- Log: Generator error message

**File Not Found**
- Cause: Source files for documentation not found
- Recovery: Verify file paths, check structure
- Log: Missing file paths

**Markdown Error**
- Cause: Invalid Markdown syntax
- Recovery: Fix syntax, validate with linter
- Log: Syntax error locations

**Broken Links**
- Cause: Documentation references non-existent files
- Recovery: Fix link targets or remove links
- Log: Broken link locations

**Incomplete Documentation**
- Cause: Required documentation missing
- Recovery: Generate or write missing sections
- Log: Missing sections and coverage

**Encoding Issue**
- Cause: File encoding problems
- Recovery: Convert to UTF-8, retry
- Log: File paths and encoding issues

---

## Tool Integration Examples

### Generate Architecture Documentation
```
Documentation: Generate architecture guide
Source: docs/architecture.md
Output: docs/ARCHITECTURE-GENERATED.md
Purpose: Auto-document system structure
Output: Generated file path
```

### Validate Documentation Completeness
```
Documentation: Validate
Path: docs/
Type: Completeness
Purpose: Check all sections documented
Output: Issues, coverage percentage
```

### Update README
```
Documentation: Update README
Section: Features
Content: New feature list
Purpose: Keep README current
Output: Updated file
```

### Generate Changelog
```
Documentation: Generate changelog
Type: Changelog
Source: git log
Output: CHANGELOG.md
Purpose: Document release history
Output: Changelog file
```

---

## See Also

- **Filesystem Tool** - For reading/writing documentation files
- **Git Tool** - For changelog generation from commit history
- **Terminal Tool** - For running documentation generators
- **GitHub Tool** - For publishing documentation

Reference: `shared.md` for common guidance on validation and quality standards.
