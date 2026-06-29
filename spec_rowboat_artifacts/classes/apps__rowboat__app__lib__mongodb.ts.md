# apps/rowboat/app/lib/mongodb.ts

**File:** apps/rowboat/app/lib/mongodb.ts  
**Language:** typescript

## Purpose
Establish MongoDB collections for storing chat and Twilio-related data.

## Internal dependencies
- ./types/voice_types

## External dependencies
- mongodb
- zod
- rowboat-shared

## Flagged idioms
- Use of MongoDB client to define and export database collections for application data storage.

## Behavioral notes
- The MongoDB connection string defaults to 'mongodb://localhost:27017' if not provided in the environment variables.
