# apps/rowboat/app/providers/help-modal-provider.tsx

**File:** apps/rowboat/app/providers/help-modal-provider.tsx  
**Language:** typescript

## Purpose
Provide a context and hooks for managing the visibility of a help modal in a React application.

## Interfaces
### `useHelpModal` (function)
```
useHelpModal()
```
**Intent:** Access the help modal context to control the modal's visibility.

**Outputs:**
- HelpModalContextType — the context value containing modal control functions
**Raises:**
- Error: when used outside of a HelpModalProvider

### `HelpModalProvider` (function)
```
HelpModalProvider({ children }: { children: ReactNode })
```
**Intent:** Provide the help modal context to its children and manage the modal's state and behavior.

**Inputs:**
- children: ReactNode — the components that will have access to the help modal context
**Side effects:**
- Renders a HelpModal component
- Modifies localStorage by removing 'user_product_tour_completed'
- Reloads the window

## External dependencies
- react
- @/components/common/help-modal

## Flagged idioms
- React Context: Used to provide and consume state across components without prop drilling.
- useState: Manages local component state for modal visibility.

## Behavioral notes
- The HelpModalProvider directly manipulates localStorage and triggers a page reload when starting a tour.
