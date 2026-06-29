# apps/experimental/chat_widget/app/providers.tsx

**File:** apps/experimental/chat_widget/app/providers.tsx  
**Language:** typescript

## Purpose
Wrap children components with the NextUIProvider for styling and theming.

## Interfaces
### `Providers` (function)
```
Providers({ children }: { children: React.ReactNode })
```
**Intent:** Provide a context for NextUI components to inherit styling and theming.

**Inputs:**
- children: React.ReactNode — the components to be wrapped by the provider
**Side effects:**
- Wraps children with NextUIProvider, affecting their styling and theming

## External dependencies
- @nextui-org/react
- react

## Flagged idioms
- React component composition: using a provider to wrap children components for context propagation
