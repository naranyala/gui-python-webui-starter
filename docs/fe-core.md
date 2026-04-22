# Frontend Core Logic

## State Management Strategy
The project avoids complex state libraries (like Redux) in favor of a **Service-Driven State** model.
1. **Service Layer**: `GraphService` or `TodoService` holds the cached data.
2. **React Hook**: Components use `useEffect` to fetch the initial state from the service.
3. **Updating**: When a user performs an action, the UI calls the Service $\rightarrow$ Service calls Python $\rightarrow$ Python updates DB $\rightarrow$ Service updates local cache $\rightarrow$ UI re-renders.

## Modular UI Structure
Each module is self-contained:
- `modules/[name]/[Name]Page.jsx`: The main view.
- `services/[Name]Service.js`: The JS wrapper for Python API calls.

## Styling Strategy
We use a global CSS variable system (`:root`) for themes, ensuring that changing a single color value updates the entire application (e.g., switching from a Dark to Light theme).
