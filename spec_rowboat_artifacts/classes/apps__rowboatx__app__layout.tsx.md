# apps/rowboatx/app/layout.tsx

**File:** apps/rowboatx/app/layout.tsx  
**Language:** typescript

## Purpose
Define the root layout component for a Next.js application.

## Interfaces
### `RootLayout` (function)
```
RootLayout({ children }: Readonly<{ children: React.ReactNode; }>)
```
**Intent:** Render the basic HTML structure for the application, including language and body attributes.

**Inputs:**
- children: React.ReactNode — the content to be rendered within the layout
**Side effects:**
- Renders HTML structure with specified children

## External dependencies
- next
- react

## Flagged idioms
- Use of React functional component to define layout structure

## Behavioral notes
- The body element includes a suppressHydrationWarning attribute.
