# apps/rowboat/app/lib/loadenv.ts

**File:** apps/rowboat/app/lib/loadenv.ts  
**Language:** typescript

## Purpose
Load environment variables from specified .env files.

## External dependencies
- dotenv

## Flagged idioms
- Using dotenv to load environment variables from .env files: ensures configuration is loaded from environment-specific files.

## Behavioral notes
- The order of paths in dotenv.config determines precedence; .env.local is prioritized over .env.
