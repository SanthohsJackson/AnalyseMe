# apps/rowboatx/components/ai-elements/image.tsx

**File:** apps/rowboatx/components/ai-elements/image.tsx  
**Language:** typescript

## Purpose
Render an image element with optional styling and alt text from base64 encoded data.

## Interfaces
### `Image` (function)
```
Image({ base64, mediaType, ...props }: ImageProps)
```
**Intent:** Render an HTML img element using base64 data and apply optional CSS classes and alt text.

**Inputs:**
- base64: string — the base64 encoded image data
- mediaType: string — the media type of the image
- props: ImageProps — additional properties including className and alt

## Internal dependencies
- @/lib/utils

## External dependencies
- ai

## Flagged idioms
- Destructuring props to separate base64 and mediaType from other properties for cleaner code.

## Behavioral notes
- The img element uses a data URL constructed from mediaType and base64 for the src attribute.
