# apps/rowboat/app/lib/uploads_s3_client.ts

**File:** apps/rowboat/app/lib/uploads_s3_client.ts  
**Language:** typescript

## Purpose
Initialize an S3 client for handling uploads with configurable region and credentials.

## External dependencies
- @aws-sdk/client-s3

## Flagged idioms
- Use of environment variables to configure AWS SDK client settings, allowing for flexible deployment configurations.

## Behavioral notes
- The client defaults to 'us-east-1' region if no environment variable is set.
- Credentials are only set if both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are provided.
