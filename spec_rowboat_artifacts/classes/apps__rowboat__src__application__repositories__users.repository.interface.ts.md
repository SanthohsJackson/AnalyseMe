# apps/rowboat/src/application/repositories/users.repository.interface.ts

**File:** apps/rowboat/src/application/repositories/users.repository.interface.ts  
**Language:** typescript

## Purpose
Defines an interface for user repository operations with methods for creating, fetching, and updating user data.

## Interfaces
### `IUsersRepository` (class)
```
interface IUsersRepository
```
**Intent:** Specifies the contract for user-related data operations in a repository.


### `create` (method)
```
create(data: z.infer<typeof CreateSchema>): Promise<z.infer<typeof User>>
```
**Intent:** Creates a new user in the repository using the provided data.

**Inputs:**
- data: z.infer<typeof CreateSchema> — the data required to create a user
**Outputs:**
- Promise<z.infer<typeof User>> — a promise resolving to the created user

### `fetch` (method)
```
fetch(id: string): Promise<z.infer<typeof User> | null>
```
**Intent:** Retrieves a user by their unique identifier.

**Inputs:**
- id: string — the unique identifier of the user to fetch
**Outputs:**
- Promise<z.infer<typeof User> | null> — a promise resolving to the user or null if not found

### `fetchByAuth0Id` (method)
```
fetchByAuth0Id(auth0Id: string): Promise<z.infer<typeof User> | null>
```
**Intent:** Retrieves a user by their Auth0 identifier.

**Inputs:**
- auth0Id: string — the Auth0 identifier of the user to fetch
**Outputs:**
- Promise<z.infer<typeof User> | null> — a promise resolving to the user or null if not found

### `updateEmail` (method)
```
updateEmail(id: string, email: string): Promise<z.infer<typeof User>>
```
**Intent:** Updates the email address of a user identified by their unique identifier.

**Inputs:**
- id: string — the unique identifier of the user
- email: string — the new email address
**Outputs:**
- Promise<z.infer<typeof User>> — a promise resolving to the updated user

### `updateBillingCustomerId` (method)
```
updateBillingCustomerId(id: string, billingCustomerId: string): Promise<z.infer<typeof User>>
```
**Intent:** Updates the billing customer ID of a user identified by their unique identifier.

**Inputs:**
- id: string — the unique identifier of the user
- billingCustomerId: string — the new billing customer ID
**Outputs:**
- Promise<z.infer<typeof User>> — a promise resolving to the updated user

## Internal dependencies
- @/src/entities/models/user

## External dependencies
- zod

## Flagged idioms
- Use of Zod for schema validation and inference, ensuring type safety and validation of user data.
