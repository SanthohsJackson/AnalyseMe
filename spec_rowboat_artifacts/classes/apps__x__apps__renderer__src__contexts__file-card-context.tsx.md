# apps/x/apps/renderer/src/contexts/file-card-context.tsx

**File:** apps/x/apps/renderer/src/contexts/file-card-context.tsx  
**Language:** typescript

## Purpose
Provide a context and hook for managing file card operations within a React application.

## Interfaces
### `useFileCard` (function)
```
useFileCard()
```
**Intent:** Access the file card context to perform operations defined in FileCardContextType.

**Outputs:**
- FileCardContextType — the context value
**Raises:**
- Error: when used outside of FileCardProvider

### `FileCardProvider` (function)
```
FileCardProvider({ onOpenKnowledgeFile, children }: { onOpenKnowledgeFile: (path: string) => void, children: ReactNode })
```
**Intent:** Wrap components to provide them with the file card context, enabling file operations.

**Inputs:**
- onOpenKnowledgeFile: (path: string) => void — function to handle file opening
- children: ReactNode — React children components
**Side effects:**
- Provides context to children components

## External dependencies
- react

## Flagged idioms
- React context: used to share state across components without passing props explicitly

## Behavioral notes
- useFileCard throws an error if used outside of FileCardProvider.
