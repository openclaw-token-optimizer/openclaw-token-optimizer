import os
import sys
import logging
from pathlib import Path

def setup_logger() -> logging.Logger:
    """Configures the standard logger for console output."""
    logger = logging.getLogger("OpenClawUpdater")
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

def get_openclaw_dir() -> Path:
    """
    Detects the standard installation path based on the operating system.
    Returns the absolute path to the OpenClaw directory.
    """
    if sys.platform == "win32":
        # Windows: Typically %APPDATA%\OpenClaw
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
        return Path(base_dir) / "OpenClaw"
    else:
        # macOS/Linux: ~/.config/OpenClaw
        return Path.home() / ".config" / "OpenClaw"
