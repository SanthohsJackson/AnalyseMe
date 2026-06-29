# apps/x/packages/core/src/config/env.ts

**File:** apps/x/packages/core/src/config/env.ts  
**Language:** typescript

## Purpose
Define a constant for the API URL, defaulting to a specific URL if not set in the environment.

## Flagged idioms
- Use of process.env to access environment variables: allows configuration via environment settings.

## Behavioral notes
- Defaults to 'https://api.x.rowboatlabs.com' if process.env.API_URL is not set.
