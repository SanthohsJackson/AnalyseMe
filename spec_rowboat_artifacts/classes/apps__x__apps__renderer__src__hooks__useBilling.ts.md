# apps/x/apps/renderer/src/hooks/useBilling.ts

**File:** apps/x/apps/renderer/src/hooks/useBilling.ts  
**Language:** typescript

## Purpose
Manage billing information retrieval and loading state based on connection status.

## Interfaces
### `useBilling` (function)
```
useBilling(isRowboatConnected: boolean)
```
**Intent:** Fetch and manage billing information when the Rowboat service is connected, providing loading state and a refresh function.

**Inputs:**
- isRowboatConnected: boolean — indicates if the Rowboat service is connected
**Outputs:**
- { billing: BillingInfo | null, isLoading: boolean, refresh: function } — billing data, loading state, and a function to refresh billing info
**Side effects:**
- Logs error to console if billing info fetch fails

## External dependencies
- react
- @x/shared/dist/billing.js

## Flagged idioms
- useEffect: used to trigger side effects (fetching billing info) when dependencies change
- useCallback: memoizes the fetchBilling function to prevent unnecessary re-creations

## Behavioral notes
- Billing info is set to null if the Rowboat service is not connected
- Loading state is managed to indicate when billing info is being fetched
