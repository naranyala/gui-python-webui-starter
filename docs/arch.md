# System Architecture

This project uses a **Hybrid Desktop Architecture** combining a Python 3.13 backend with a React 19 frontend.

## Key Layers
1. **Host**: Python 3.13+ managed by `uv` for fast, deterministic dependency resolution.
2. **GUI Shell**: `webui2` acts as a native window wrapper, eliminating the need for a standalone browser.
3. **Frontend**: React 19 bundled with **Rspack** for near-instant build times.
4. **API Layer**: Dual-path communication (WebUI Bridge + FastAPI).
5. **Persistence**: SQLite with WAL mode enabled for concurrent read/writes.

## Module System
The project follows a strict **Modular Pattern**. Each feature (Docs, Todos, System Monitor) is an isolated unit:
- **Frontend**: `frontend/src/modules/[feature]/` contains the Page and components.
- **Backend Service**: `backend/src/services/[feature]_service.py` contains business logic.
- **API Routes**: `backend/src/api/routes.py` or separate module files bridge the service to the UI.
