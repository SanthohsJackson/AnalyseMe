# apps/rowboat/src/interface-adapters/controllers/projects/rotate-secret.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/rotate-secret.controller.ts  
**Language:** typescript

## Purpose
Handle the rotation of a secret for a project by validating input and executing the use case.

## Interfaces
### `IRotateSecretController` (class)
```
interface IRotateSecretController
```
**Intent:** Define the contract for a controller that rotates a project secret.


### `RotateSecretController` (class)
```
class RotateSecretController implements IRotateSecretController
```
**Intent:** Implement the IRotateSecretController interface to manage secret rotation.

**Inputs:**
- rotateSecretUseCase: IRotateSecretUseCase

### `constructor` (method)
```
constructor({ rotateSecretUseCase }: { rotateSecretUseCase: IRotateSecretUseCase })
```
**Intent:** Initialize the RotateSecretController with a use case for rotating secrets.

**Inputs:**
- rotateSecretUseCase: IRotateSecretUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<string>
```
**Intent:** Validate the input request and execute the secret rotation use case.

**Inputs:**
- request: z.infer<typeof inputSchema>
**Outputs:**
- Promise<string>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/rotate-secret.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of zod for input validation ensures type-safe request parsing.

## Behavioral notes
- The execute method throws a BadRequestError if input validation fails.
