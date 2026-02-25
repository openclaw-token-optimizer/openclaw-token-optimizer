import shutil
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger("OpenClawUpdater")

def create_skills_backup(skills_dir: Path) -> Path:
    """
    Creates a ZIP archive of the current skills directory.
    Saves it in the parent directory with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"skills_backup_{timestamp}"
    parent_dir = skills_dir.parent
    
    # shutil.make_archive automatically adds the .zip extension
    archive_path = shutil.make_archive(
        base_name=str(parent_dir / backup_filename),
        format="zip",
        root_dir=str(parent_dir),
        base_dir=skills_dir.name
    )
    
    logger.info(f"📦 Backup created successfully: {archive_path}")
    return Path(archive_path)
