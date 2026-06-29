# apps/rowboat/app/providers.tsx

**File:** apps/rowboat/app/providers.tsx  
**Language:** typescript

## Purpose
Provide a context for HeroUI components with navigation capabilities using Next.js router.

## Interfaces
### `Providers` (function)
```
Providers({ className, children }: { className: string, children: React.ReactNode })
```
**Intent:** Wrap children components with HeroUIProvider to enable UI theming and navigation.

**Inputs:**
- className: string — CSS class name for styling
- children: React.ReactNode — React nodes to be rendered within the provider
**Side effects:**
- Integrates HeroUIProvider with Next.js router for navigation

## External dependencies
- @heroui/react
- next/navigation

## Flagged idioms
- React component composition: using a provider to wrap children components for context sharing

## Behavioral notes
- The router's push method is passed to HeroUIProvider, enabling navigation.
