#!/usr/bin/env bash

# Build and run script for the GUI project
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Define paths
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_WEB_DIR="$PROJECT_ROOT/backend/src/web"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

function build_frontend() {
    echo "Building frontend (Rspack)..."
    (cd "$FRONTEND_DIR" && npm run build)
    
    echo "Distributing frontend build to backend..."
    mkdir -p "$BACKEND_WEB_DIR"
    cp -r "$FRONTEND_DIR/dist/"* "$BACKEND_WEB_DIR/"
}

case "$1" in
    dev)
        echo "Starting development mode..."
        
        # 0. Sync dependencies (Python)
        echo "Checking Python dependencies..."
        uv sync
        
        build_frontend
        echo "Starting Python application..."
        $VENV_PYTHON main.py
        ;;
    build)
        build_frontend
        echo "Build complete. Frontend is in $BACKEND_WEB_DIR"
        ;;
    package)
        build_frontend
        
        echo ""
        echo "Select a builder for single-file executable:"
        echo "1) PyInstaller (Fast, Standard)"
        echo "2) Nuitka (Compiled, Faster Runtime, Secure)"
        echo "3) PyOxidizer (Rust-based, Advanced, In-memory)"
        read -p "Choice [1-3]: " BUILDER_CHOICE
        
        case $BUILDER_CHOICE in
            1)
                echo "Packaging with PyInstaller..."
                $VENV_PYTHON -m pip install pyinstaller
                $VENV_PYTHON -m PyInstaller --onefile \
                    --name "DocViewer" \
                    --add-data "backend/src/web:web" \
                    --collect-all webui2 \
                    --clean \
                    main.py
                echo "Success! Binary is in dist/DocViewer"
                ;;
            2)
                echo "Packaging with Nuitka..."
                $VENV_PYTHON -m pip install nuitka
                $VENV_PYTHON -m nuitka --standalone --onefile \
                    --include-data-dir="backend/src/web=web" \
                    --output-dir=dist-nuitka \
                    main.py
                echo "Success! Binary is in dist-nuitka/main.bin"
                ;;
            3)
                echo "PyOxidizer requires a PyOxidizer.bzl configuration file."
                echo "Generating basic PyOxidizer config..."
                # (Logic to generate basic PyOxidizer config could go here)
                echo "Please install PyOxidizer and run: pyoxidizer build"
                ;;
            *)
                echo "Invalid choice."
                exit 1
                ;;
        esac
        ;;
    clean)
        echo "Cleaning build artifacts..."
        rm -rf "$FRONTEND_DIR/dist"
        rm -rf "$BACKEND_WEB_DIR"
        rm -rf build dist dist-nuitka *.spec
        find . -name "__pycache__" -type d -exec rm -rf {} +
        
        # Kill any zombie processes on our ports
        echo "Cleaning zombie processes..."
        fuser -k 8000/tcp 2>/dev/null || true
        fuser -k 3001/tcp 2>/dev/null || true
        ;;
    test)
        echo "Running tests..."
        $VENV_PYTHON -m pytest backend/tests || echo "Pytest failed"
        (cd frontend && bun test) || echo "Bun tests failed"
        ;;
    *)
        echo "Usage: ./run.sh {dev|build|clean|package|test}"
        exit 1
        ;;
esac
