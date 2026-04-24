import os
import sys
import logging
import platform
import subprocess
from pathlib import Path
from ..core.bridge import api_action

logger = logging.getLogger(__name__)

class SystemIntegrationService:
    """
    Handles OS-level integrations: System Tray, Auto-start, and Window State.
    """
    def __init__(self, container):
        self.container = container
        self.os_type = platform.system()

    def initialize(self):
        logger.info(f"System Integration Service initialized for {self.os_type}")
        return True

    @api_action
    def set_auto_start(self, enabled: bool):
        """
        Enable or disable application auto-start on OS boot.
        """
        app_path = sys.executable # Path to the running python/binary
        app_name = "DocViewerApp"

        try:
            if self.os_type == "Windows":
                import winreg
                key = winreg.HKEY_CURRENT_USER
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                    if enabled:
                        winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, app_path)
                    else:
                        winreg.DeleteValue(reg_key, app_name)
            
            elif self.os_type == "Linux":
                autostart_dir = Path.home() / ".config" / "autostart"
                autostart_dir.mkdir(parents=True, exist_ok=True)
                desktop_file = autostart_dir / f"{app_name.lower()}.desktop"
                
                if enabled:
                    content = f"[Desktop Entry]\nType=Application\nExec={app_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName={app_name}\n"
                    desktop_file.write_text(content)
                else:
                    if desktop_file.exists():
                        desktop_file.unlink()
            
            logger.info(f"Auto-start {'enabled' if enabled else 'disabled'} for {self.os_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to set auto-start: {e}")
            return False

    def setup_tray(self, window_instance):
        """
        Initialize the system tray icon. 
        Note: This should be run in a separate thread.
        """
        try:
            import pystray
            from PIL import Image, ImageDraw

            # Create a simple icon (16x16 blue square)
            def create_image():
                image = Image.new('RGB', (64, 64), color=(59, 130, 246))
                d = ImageDraw.Draw(image)
                d.text((10, 10), "DV", fill=(255, 255, 255))
                return image

            def on_show(icon, item):
                # This is tricky because webui.Window doesn't have a simple .show() 
                # after it's hidden, but we can try to trigger a window refresh or alert.
                logger.info("Tray: Show window requested")
                # In a real app, you'd call window_instance.show() if the library supports it

            def on_exit(icon, item):
                logger.info("Tray: Exit requested")
                icon.stop()
                os._exit(0)

            menu = pystray.Menu(
                pystray.MenuItem('Show App', on_show),
                pystray.MenuItem('Exit', on_exit)
            )
            
            icon = pystray.Icon("DocViewer", create_image(), "DocViewer", menu)
            icon.run()
        except ImportError:
            logger.error("pystray or Pillow not installed. System tray unavailable.")
        except Exception as e:
            logger.error(f"System tray error: {e}")
