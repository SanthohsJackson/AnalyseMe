# apps/rowboat/src/entities/models/data-source.ts

**File:** apps/rowboat/src/entities/models/data-source.ts  
**Language:** typescript

## Purpose
Define a data structure for a data source using zod for validation.

## External dependencies
- zod

## Flagged idioms
- Use of zod for schema validation: provides a declarative way to define and validate data structures.

## Behavioral notes
- The 'active' field defaults to true if not provided.
- The 'status' field is restricted to specific string values.
- The 'data' field uses a discriminated union to handle different types of data sources.
