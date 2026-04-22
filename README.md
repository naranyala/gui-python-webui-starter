# 🚀 GUI Python WebUI Starter

A professional-grade boilerplate for creating high-performance desktop applications using a **Python 3.13** backend and a **React 19** frontend, wrapped in a native OS window via `webui2`.

## 🏗️ Architecture Overview

This project implements a **Hybrid Desktop Architecture**, bridging the gap between native system power and modern web UI flexibility.

### The Polyglot Stack
- **Core**: Python 3.13 (managed by `uv` for deterministic environments).
- **GUI Shell**: `webui2` (native window wrapper, no browser installation required).
- **Frontend**: React 19 bundled with **Rspack** (Rust-based bundler for near-instant builds).
- **Persistence**: SQLite with **WAL (Write-Ahead Logging)** for concurrent read/write access.

### Dual-Path Communication Bridge
The application uses a unique `ApiClient` that abstracts the transport layer, allowing the same frontend code to run in two modes:
1. **WebUI Bridge (Production)**: Uses OS-level IPC (Inter-Process Communication) via `window.webui.call()`. Zero network overhead and bypasses CORS/Firewall restrictions.
2. **FastAPI (Development)**: A background REST API server that allows testing in standard browsers and supports WebSockets for real-time server-to-client pushes.

---

## 🛠️ Key Technical Abstractions

### Backend: Dependency Injection & Services
- **DI Container**: A custom `DIContainer` manages service lifecycles as singletons, ensuring a decoupled and testable architecture.
- **Service Layer**: Business logic is encapsulated in `BaseService` extensions, separating "what the app does" from "how it communicates."

### Frontend: Service-Driven State
- **Modular UI**: Features are isolated into independent modules (`frontend/src/modules/`) containing their own views and logic.
- **State Strategy**: Uses a Service-Driven model where JS services act as the source of truth, bridging the React UI to Python backend calls.

---

## ✨ Core Features Demonstrated

- **🖥️ System Monitor**: Real-time hardware metrics (CPU, RAM, Disk) using `psutil`.
- **⚙️ App Settings**: Dynamic, JSON-serialized Key-Value store persisted in SQLite.
- **🕸️ Interactive Graph**: Relationship visualization using Cytoscape.js.
- **✅ Task Manager**: Full CRUD lifecycle with SQLite persistence.
- **📄 Project Wiki**: Integrated markdown documentation system.

---

## 📂 Project Structure

```text
├── backend/
│   ├── src/core/      # DI Container, Database, App Window logic
│   ├── src/services/  # Pure business logic (System, Settings, etc.)
│   └── src/api/       # FastAPI routes & WebUI Bridge bindings
├── frontend/
│   ├── src/core/      # Frontend DI & Config
│   ├── src/services/  # JS wrappers for API communication
│   ├── src/modules/   # Feature-specific UI (System, Graph, Todos)
│   └── src/styles/    # Design tokens and global CSS
└── shared/            # Shared types and constants
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- `uv` (recommended)

### Quick Launch
Run the unified CLI script to handle dependency installation, frontend bundling, and application launch:
```bash
chmod +x run.sh
./run.sh
```

### Packaging for Distribution
The project is designed to be frozen into a single executable using **PyInstaller** or **Nuitka**, packaging the Python runtime and the bundled frontend assets together.
