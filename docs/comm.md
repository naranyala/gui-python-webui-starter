# Backend-Frontend Communication

The application implements a **Polyglot Bridge** to allow flexible development and deployment.

## 1. WebUI Bridge (Production Path)
The Bridge uses OS-level IPC (Inter-Process Communication).
- **How it works**: Python registers a function via `window.bind("name", func)`. JavaScript calls it via `window.webui.call("name", args)`.
- **Benefits**: Zero network overhead, no port conflicts, and bypasses browser CORS/Firewall restrictions.

## 2. FastAPI (Development Path)
A standard REST API server runs in a background thread.
- **Purpose**: Allows developers to test the backend in a standard browser or via `curl` without launching the native window.
- **WebSockets**: Used for server-to-client pushes (e.g., real-time log streaming).

## The Hybrid `ApiClient`
The `ApiClient` in `frontend/src/services/base.js` abstracts the communication. It checks `config.commMode`:
- If `BRIDGE`, it uses `requestWebUI()` $\rightarrow$ `window.webui.call()`.
- If `REST`, it uses `fetch()` $\rightarrow$ `http://localhost:8000/api`.
This allows the same frontend code to work in both a native window and a web browser.
