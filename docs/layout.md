# Project Layout Guide

## Backend (`/backend`)
- `src/core/`: The engine (DI Container, DB connection, App window).
- `src/services/`: Pure business logic (The "What").
- `src/api/`: Communication layer (The "How").
    - `routes.py`: Maps endpoints to services.
    - `server.py`: FastAPI implementation.
    - `modules/`: WebUI Bridge bindings.

## Frontend (`/frontend`)
- `src/core/`: Dependency injection and configuration.
- `src/services/`: JS wrappers for API calls.
- `src/modules/`: Feature-specific UI components.
- `src/styles/`: Global CSS and design tokens.

## Shared (`/shared`)
- `types/`: Shared Python type definitions (dataclasses) for consistency across services.
