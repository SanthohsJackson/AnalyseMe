# apps/rowboat/app/lib/qdrant.ts

**File:** apps/rowboat/app/lib/qdrant.ts  
**Language:** typescript

## Purpose
Initialize a QdrantClient instance to connect to a Qdrant server using environment variables for configuration.

## External dependencies
- @qdrant/js-client-rest

## Flagged idioms
- Use of environment variables to configure client connection details, allowing for flexible deployment configurations.

## Behavioral notes
- The API key is conditionally included in the client configuration only if it is present in the environment variables.
