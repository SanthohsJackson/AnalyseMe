# apps/x/apps/main/src/html-to-docx.d.ts

**File:** apps/x/apps/main/src/html-to-docx.d.ts  
**Language:** typescript

## Purpose
Provide a TypeScript declaration for a function that converts HTML to a DOCX format.

## Interfaces
### `htmlToDocx` (function)
```
htmlToDocx(htmlString: string, headerHTMLString?: string, options?: Record<string, unknown>): Promise<ArrayBuffer>
```
**Intent:** Convert HTML content into a DOCX file, optionally including a header and additional options.

**Inputs:**
- htmlString: string — the HTML content to convert
- headerHTMLString?: string — optional HTML content for the header
- options?: Record<string, unknown> — optional configuration options
**Outputs:**
- Promise<ArrayBuffer> — a promise that resolves to an ArrayBuffer representing the DOCX file

## External dependencies
- html-to-docx
