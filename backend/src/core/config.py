import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class AppConfig:
    app_name: str = "DocViewer"
    app_version: str = "1.0.0"
    
    # Window settings
    window_width: int = 1200
    window_height: int = 800
    window_title: str = "DocViewer - Python WebUI"
    
    # Paths
    frontend_dist: str = "web"
    log_file: str = "app.log"
    
    # Server settings
    host: str = "localhost"
    port: int = 3001
    
    # Development
    debug: bool = False
    
    @property
    def root_path(self) -> Path:
        return Path(__file__).parent.parent.parent
    
    @property
    def dist_path(self) -> Path:
        return self.root_path / self.frontend_dist
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        return cls(
            app_name=os.getenv("APP_NAME", "DocViewer"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            port=int(os.getenv("PORT", "3001")),
        )

_config: AppConfig = None

def get_config() -> AppConfig:
    global _config
    if _config is None:
        _config = AppConfig.from_env()
    return _config

def set_config(config: AppConfig):
    global _config
    _config = config

__all__ = ['AppConfig', 'get_config', 'set_config']