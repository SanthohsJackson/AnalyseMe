# apps/rowboat/app/actions/job.actions.ts

**File:** apps/rowboat/app/actions/job.actions.ts  
**Language:** typescript

## Purpose
Provide actions to list jobs and fetch a specific job, integrating authentication and controller execution.

## Interfaces
### `listJobs` (function)
```
listJobs(request: { projectId: string, filters?: z.infer<typeof JobFiltersSchema>, cursor?: string, limit?: number })
```
**Intent:** Execute the listJobsController to retrieve a list of jobs based on the provided request parameters.

**Inputs:**
- request: { projectId: string, filters?: z.infer<typeof JobFiltersSchema>, cursor?: string, limit?: number } — parameters for listing jobs
**Outputs:**
- Promise<any> — result of the listJobsController execution
**Side effects:**
- authCheck is called to verify user authentication

### `fetchJob` (function)
```
fetchJob(request: { jobId: string })
```
**Intent:** Execute the fetchJobController to retrieve details of a specific job based on the provided jobId.

**Inputs:**
- request: { jobId: string } — parameters for fetching a specific job
**Outputs:**
- Promise<any> — result of the fetchJobController execution
**Side effects:**
- authCheck is called to verify user authentication

## Internal dependencies
- ./auth.actions

## External dependencies
- @/di/container
- @/src/interface-adapters/controllers/jobs/list-jobs.controller
- @/src/interface-adapters/controllers/jobs/fetch-job.controller
- @/src/application/repositories/jobs.repository.interface
- zod

## Flagged idioms
- Dependency injection via container.resolve to obtain controller instances.

## Behavioral notes
- Both functions require user authentication via authCheck before executing their respective controllers.
