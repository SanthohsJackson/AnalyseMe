# apps/x/apps/renderer/vite.config.ts

**File:** apps/x/apps/renderer/vite.config.ts  
**Language:** typescript

## Purpose
Configure Vite for a React project with Tailwind CSS and custom path resolution.

## External dependencies
- path
- vite
- @vitejs/plugin-react
- @tailwindcss/vite

## Flagged idioms
- Use of Vite's defineConfig to export configuration: standard practice for Vite projects.

## Behavioral notes
- The base path is set to './' to support Electron's custom protocol.
- An alias '@' is set for the './src' directory to simplify imports.
