# apps/rowboat/app/scripts/job-rules.worker.ts

**File:** apps/rowboat/app/scripts/job-rules.worker.ts  
**Language:** typescript

## Purpose
Execute a job rules worker asynchronously and handle any errors that occur during execution.

## Internal dependencies
- ../lib/loadenv

## External dependencies
- @/di/container
- @/src/application/workers/job-rules.worker

## Flagged idioms
- Immediately Invoked Function Expression (IIFE): used to execute asynchronous code in a contained scope.

## Behavioral notes
- The code attempts to resolve and run a worker from a dependency injection container, logging an error if it fails.
