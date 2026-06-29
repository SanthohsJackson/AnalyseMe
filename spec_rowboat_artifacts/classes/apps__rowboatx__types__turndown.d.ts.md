# apps/rowboatx/types/turndown.d.ts

**File:** apps/rowboatx/types/turndown.d.ts  
**Language:** typescript

## Purpose
Defines a TypeScript module for converting HTML to Markdown using the TurndownService class.

## Interfaces
### `TurndownService` (class)
```
class TurndownService
```
**Intent:** Provides methods to convert HTML to Markdown and extend functionality with rules and plugins.


### `constructor` (method)
```
constructor(options?: unknown)
```
**Intent:** Initializes a new instance of TurndownService with optional settings.

**Inputs:**
- options: unknown — optional configuration for the service

### `addRule` (method)
```
addRule(name: string, rule: unknown): void
```
**Intent:** Adds a custom rule to the TurndownService instance.

**Inputs:**
- name: string — the name of the rule
- rule: unknown — the rule definition
**Outputs:**
- void

### `use` (method)
```
use(plugin: unknown): void
```
**Intent:** Applies a plugin to extend the functionality of the TurndownService.

**Inputs:**
- plugin: unknown — the plugin to use
**Outputs:**
- void

### `turndown` (method)
```
turndown(html: string): string
```
**Intent:** Converts HTML content into Markdown format.

**Inputs:**
- html: string — the HTML content to convert
**Outputs:**
- string — the converted Markdown content
