# apps/experimental/chat_widget/app/layout.tsx

**File:** apps/experimental/chat_widget/app/layout.tsx  
**Language:** typescript

## Purpose
Defines the root layout component for the RowBoat Chat application, applying global styles and fonts.

## Interfaces
### `RootLayout` (function)
```
RootLayout({ children }: Readonly<{ children: React.ReactNode; }>)
```
**Intent:** Wraps application content in a styled HTML structure with global fonts and styles.

**Inputs:**
- children: React.ReactNode — the content to be rendered within the layout
**Side effects:**
- Renders HTML structure with specific fonts and styles applied

## External dependencies
- next
- next/font/local

## Flagged idioms
- Use of localFont from next/font/local to define custom fonts for the application

## Behavioral notes
- The HTML element is set to have a transparent background and full height.
