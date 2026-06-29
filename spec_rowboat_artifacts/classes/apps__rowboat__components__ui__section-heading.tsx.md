# apps/rowboat/components/ui/section-heading.tsx

**File:** apps/rowboat/components/ui/section-heading.tsx  
**Language:** typescript

## Purpose
Render a section heading with optional subheading using specified design tokens for styling.

## Interfaces
### `SectionHeading` (function)
```
SectionHeading({ children, subheading }: SectionHeadingProps)
```
**Intent:** Render a styled section heading and optional subheading using design tokens for consistent typography and color.

**Inputs:**
- children: React.ReactNode — the main heading content
- subheading?: React.ReactNode — optional subheading content

### `SectionHeadingProps` (class)
```
interface SectionHeadingProps
```
**Intent:** Define the props for the SectionHeading component, including main and optional subheading content.

**Inputs:**
- children: React.ReactNode
- subheading?: React.ReactNode

## External dependencies
- clsx
- @/app/styles/design-tokens

## Flagged idioms
- Use of clsx for conditional className construction, allowing dynamic styling based on design tokens.

## Behavioral notes
- The subheading is conditionally rendered only if provided.
