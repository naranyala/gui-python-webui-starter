# Project Roadmap & Status

## ✅ Achieved Milestones

### Core Architecture
- [x] **Hybrid Model**: Successfully combined Python 3.13 backend with React 19 frontend.
- [x] **Modular Structure**: Established `modules/` pattern for both frontend and backend.
- [x] **DI Container**: Robust Dependency Injection for Python services.
- [x] **Observer Pattern**: Solved React reactivity issues with a stable service-subscriber model.

### Communication & API
- [x] **Dual-Path Bridge**: High-speed WebUI IPC for production; FastAPI REST for dev/debugging.
- [x] **WebSocket Support**: Real-time push notifications from Python to React.
- [x] **Standard Protocol**: Unified `{success, data, error}` response format across all layers.

### Persistence & Data
- [x] **SQLite Integration**: Local database persistence for all modules.
- [x] **Concurrency Support**: Enabled WAL (Write-Ahead Logging) for simultaneous API/GUI access.
- [x] **Auto-Seeding**: Initial data and technical documentation automatically injected on first run.

### UI/UX
- [x] **Zero-Flicker Styles**: CSS Extraction prevents "white flash" on startup.
- [x] **Fuzzy Search**: Global card menu with real-time module filtering (Fuse.js).
- [x] **TodoMVC Demo**: Fully functional, persistent task manager example.
- [x] **Project Wiki**: Integrated technical documentation exposing the entire stack.

### Build & Distribution
- [x] **Rspack Integration**: Extremely fast frontend bundling.
- [x] **Unified CLI**: `run.sh` handles build, dev, clean, and test.
- [x] **Packaging System**: Choice between PyInstaller and Nuitka for single-file binaries.

---

## 🛠️ Phase 2: Production Polish (Current Sprint)

### Backend Ecosystem Integration
- [ ] **Strict Validation**: Implement **Pydantic** for request/response schema validation.
- [ ] **Async Tasking**: Use **Asyncio** or **APScheduler** for non-blocking background jobs.
- [ ] **Security**: Add **Cryptography** for encrypting sensitive data in SQLite.
- [ ] **OS Integration**: Implement **Plyer** for native system notifications and tray icons.

### Frontend Feature Expansion
- [ ] **System Monitor** (Low): Real-time CPU/RAM usage using `psutil`.
- [ ] **App Settings** (Low): Persistent user preferences stored in SQLite.
- [ ] **Live Log Streamer** (Medium): WebSocket streaming of backend logs.
- [ ] **Local File Explorer** (Medium): Filesystem navigation and I/O.
- [ ] **Data Dashboard** (Medium): Visual analytics via SQLite aggregation.
- [ ] **API Playground** (Medium): Dynamic endpoint testing tool.
- [ ] **Advanced Kanban** (Medium): Drag-and-drop task management.

### UX & Stability
- [ ] **Error Boundaries**: Global React error handling that logs to Python.
- [ ] **Settings Module**: User-configurable app settings (stored in SQLite).
- [ ] **Log Viewer**: Real-time streaming of Python logs into a GUI console.

## ⚠️ Technical Debt & Architectural Refactoring

### API & Communication
- [ ] **Fix ApiClient Usage**: Standardize on `module:action` pattern across all services. Currently, `TodoService`, `DocumentService`, and `GraphService` incorrectly use REST-style paths (e.g., `/todos`), causing malformed bridge calls.
- [ ] **Correct Response Handling**: Remove redundant `response.success` checks in services. `ApiClient` already handles this and returns `data.data` directly.
- [ ] **Standardize Parameter Serialization**: Remove manual `JSON.stringify` calls in `TableCrudService`; ensure `ApiClient` handles object serialization consistently.

### Dependency Injection
- [ ] **Improve Service Injection**: Instead of services manually resolving `ApiClient` via `this.container.resolve(Symbol.for('ApiClient'))`, inject the `ApiClient` directly into the service constructors.


### 1. Artificial Intelligence (Local AI)
- [ ] **Local LLM Integration**: Use `llama-cpp-python` to embed a local AI chat module.
- [ ] **RAG Engine**: Use the Documentation module as a source for a local vector-search RAG.

### 2. System & OS Integration
- [ ] **Native Shell**: Add a system tray icon with a custom context menu.
- [ ] **Auto-Updater**: Implement a GitHub-based update checker and downloader.
- [ ] **Multi-Window**: Allow opening specific modules in separate native windows.

### 3. Advanced Architecture
- [ ] **Plugin System**: Support for dynamic `.py` and `.jsx` modules loaded at runtime.
- [ ] **Micro-Frontend**: Support for loading remote JS bundles.
- [ ] **Auth Layer**: Local user authentication using Argon2 hashing.

---

*Status updated: 2026-04-22*
*Project State: Framework Stable $\rightarrow$ Moving to Production Polish*
