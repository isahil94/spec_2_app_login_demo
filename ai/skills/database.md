# Database Developer Skills

This document defines reusable capabilities for the Database Developer agent in data persistence and management.

---

## Skill: Design Database Schema

### Purpose
Create the database schema that persistently stores application data, optimized for performance, integrity, and maintainability.

### When to Use
- Creating initial database structure
- Designing tables and relationships
- Optimizing for query performance
- Planning for scalability

### Inputs
- `data_model` (object): Application data model
- `access_patterns` (array): How data will be queried
- `scale_expectations` (object): Expected data volume and growth
- `constraints` (array, optional): Business or technical constraints
- `existing_schema` (object, optional): Schema to migrate from

### Outputs
- `tables` (array): Table definitions
- `relationships` (array): Foreign keys and relationships
- `indexes` (array): Index strategy
- `constraints` (array): Unique, check, referential constraints
- `schema_diagram` (string): Database schema visualization

### Dependencies
- Application data model defined
- Access patterns understood
- Database technology chosen

### Execution Steps
1. Normalize data model following database normalization principles
2. Define tables for each entity
3. Identify primary and foreign keys
4. Add columns with appropriate data types
5. Define constraints (NOT NULL, UNIQUE, CHECK, etc.)
6. Plan indexing strategy
7. Consider partitioning for large tables
8. Document column purposes and constraints
9. Create schema migration path

### Validation Checklist
- [ ] All data entities have tables
- [ ] Relationships are correctly represented
- [ ] Data types are appropriate
- [ ] Constraints ensure data integrity
- [ ] Performance is acceptable for access patterns
- [ ] Schema is normalized appropriately

### Success Criteria
- Schema stores all required data
- Data integrity is enforced
- Query performance is acceptable
- Schema supports application growth
- Schema is maintainable

### Failure Conditions
- Schema missing required data
- Relationships incorrect or incomplete
- Performance unacceptable for queries
- Data integrity violated
- Schema cannot support growth

---

## Skill: Generate SQL Scripts

### Purpose
Create SQL code for database setup, migrations, and data operations that developers can execute.

### When to Use
- Creating schema creation scripts
- Creating schema migration scripts
- Creating data seeding scripts
- Creating utility queries

### Inputs
- `schema` (object): Database schema design
- `migration_target` (object, optional): Schema to migrate to
- `seed_data` (array, optional): Initial data to load
- `database_type` (string, optional): Database system (PostgreSQL, MySQL, etc.)

### Outputs
- `creation_scripts` (array): Scripts to create tables
- `migration_scripts` (array): Scripts to migrate schema
- `seed_scripts` (array): Scripts to load initial data
- `utility_scripts` (array): Common utility queries
- `script_documentation` (object): How to run scripts

### Dependencies
- Schema designed
- Database technology chosen
- Migration path understood

### Execution Steps
1. Generate CREATE TABLE statements
2. Generate CREATE INDEX statements
3. Generate constraint definitions
4. Generate relationships/foreign keys
5. If migrating: generate ALTER TABLE statements
6. Generate data seeding statements if needed
7. Add transaction control and error handling
8. Document script execution order
9. Create rollback scripts

### Validation Checklist
- [ ] Scripts are syntactically correct
- [ ] Scripts execute in correct order
- [ ] Scripts handle errors gracefully
- [ ] Migration scripts preserve data
- [ ] Scripts are idempotent where appropriate
- [ ] Documentation is complete

### Success Criteria
- Scripts successfully create/migrate database
- Schema is correctly created
- Data integrity enforced
- Scripts execute without errors
- Rollback possible if needed

### Failure Conditions
- Scripts have syntax errors
- Scripts corrupt data
- Scripts execute in wrong order
- Migration loses data
- Cannot rollback failed migration

---

## Skill: Define Relationships

### Purpose
Specify how data entities relate to each other, ensuring referential integrity and supporting proper data access patterns.

### When to Use
- Defining foreign key relationships
- Planning join operations
- Ensuring data consistency
- Designing for data access patterns

### Inputs
- `data_model` (object): Application data model
- `tables` (array): Database tables
- `access_patterns` (array): How data will be queried
- `constraints` (array, optional): Business constraints

### Outputs
- `relationships` (array): Relationship definitions
- `foreign_keys` (array): Foreign key constraints
- `cardinality_definitions` (object): One-to-one, one-to-many, many-to-many
- `referential_integrity_rules` (object): Cascade rules
- `relationship_documentation` (string): Relationship diagrams and docs

### Dependencies
- Data model defined
- Tables designed
- Access patterns understood

### Execution Steps
1. Identify relationships between entities
2. Determine cardinality (1:1, 1:N, N:N)
3. Define foreign key columns
4. Decide on referential integrity rules (CASCADE, SET NULL, etc.)
5. For N:N relationships: design junction tables
6. Plan joins for common access patterns
7. Document relationship purposes
8. Create relationship diagrams
9. Validate no circular dependencies

### Validation Checklist
- [ ] All relationships documented
- [ ] Cardinality correctly represented
- [ ] Foreign keys properly defined
- [ ] Referential integrity enforced
- [ ] Junction tables for many-to-many
- [ ] No circular reference issues

### Success Criteria
- Data relationships correctly modeled
- Referential integrity maintained
- Queries can efficiently access related data
- Data consistency enforced
- No orphaned records

### Failure Conditions
- Relationships missing
- Cardinality incorrect
- Orphaned records exist
- Cannot access related data efficiently
- Referential integrity violated

---

## Skill: Optimize Indexes

### Purpose
Design index strategy that optimizes query performance without excessive storage overhead or write performance degradation.

### When to Use
- Optimizing slow queries
- Planning indexes for new schema
- Balancing query vs. write performance
- Preparing for production scale

### Inputs
- `schema` (object): Database schema
- `access_patterns` (array): Queries to optimize
- `scale_expectations` (object): Data volume and growth
- `write_patterns` (array, optional): How data is written

### Outputs
- `index_strategy` (object): Overall indexing plan
- `indexes` (array): Specific indexes to create
- `compound_indexes` (array): Multi-column indexes
- `index_justifications` (object): Why each index is needed
- `index_maintenance_plan` (object): How to maintain indexes

### Dependencies
- Schema designed
- Access patterns documented
- Performance requirements defined

### Execution Steps
1. Identify queries that need optimization
2. Analyze query plans to find bottlenecks
3. Identify candidate columns for indexing
4. Determine index type (B-tree, hash, etc.)
5. Plan compound indexes for common queries
6. Balance query optimization vs. write performance
7. Consider covering indexes if appropriate
8. Document index justification
9. Plan index maintenance and monitoring

### Validation Checklist
- [ ] Indexes improve query performance
- [ ] Write performance acceptable
- [ ] Index storage overhead reasonable
- [ ] No unused indexes
- [ ] Statistics kept up to date
- [ ] Query plans use indexes

### Success Criteria
- Query performance meets requirements
- Write performance acceptable
- Index storage is reasonable
- Queries use indexes effectively
- No unnecessary indexes

### Failure Conditions
- Queries still slow despite indexes
- Indexes degrade write performance
- Too many unused indexes
- Index storage excessive
- Query plans ignore indexes
