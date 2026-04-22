# Bundling and Deployment

## Frontend Bundling
We use **Rspack** instead of Webpack. 
- **Why**: Rspack is written in Rust and is significantly faster for development.
- **Output**: Bundles into `frontend/dist`, which is then served by the Python `webui2` wrapper.

## Packaging
The application can be frozen into a single executable using:
1. **PyInstaller**: Standard bundling.
2. **Nuitka**: Compiles Python to C for better performance and obfuscation.

## Runtime Execution
The `run.sh` script manages the lifecycle:
- Cleans old builds.
- Installs dependencies via `uv`.
- Runs the frontend build.
- Launches the Python main entry point.
