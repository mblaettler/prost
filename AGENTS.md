# AGENTS.md

## Commands

- Run dev server: `npm run dev`
- Build for production: `npm run build`
- Lint code: `npm run lint`
- Format code: `npm run format`

## Type Checking

- Type check: `npm run type-check`

## Project Setup

- Install dependencies: `npm install`

## Testing

- Run tests: `npm test`

## Code Style

- Use single quotes for strings
- Use semicolons at the end of statements
- Use 2 spaces for indentation

## Recommended IDE Setup

- VS Code + Vue (Official) extension (and disable Vetur)

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - Vue.js devtools
  - Turn on Custom Object Formatter in Chrome DevTools
- Firefox:
  - Vue.js devtools
  - Turn on Custom Object Formatter in Firefox DevTools

## Type Support for `.vue` Imports in TS

- TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need Volar to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Project Structure

### Backend (Python)

- `api/` - Backend source code directory
- `api/auth.py` - Authentication and authorization logic
- `api/bar/` - Bar-related endpoints
- `api/config/` - Configuration settings
- `api/database.py` - Database connection and session management
- `api/main.py` - Main application entry point
- `api/schemas.py` - Data schemas and models

### Frontend (Vue)

- `ui/src/` - Frontend source code directory
- `ui/src/components/` - Vue components
- `ui/src/router/` - Vue Router configuration
- `ui/src/views/` - Application views
- `ui/src/assets/` - Static assets
- `ui/src/utils/` - Utility functions
- `ui/src/store/` - Vuex store configuration
- `ui/src/services/` - API services
- `ui/src/types/` - TypeScript types

## Dependencies

- Python
- Poetry
- FastAPI
- Vue 3
- Vue Router
- TypeScript
- Vite
- Tailwind CSS
- ESLint
- Prettier
- Oxlint
- Vue DevTools
