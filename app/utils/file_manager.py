"""
File and directory management utilities
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from .logger import get_logger

logger = get_logger(__name__)


class FileManager:
    """Handles file operations safely and reliably"""

    @staticmethod
    def ensure_dir(path: Path) -> Path:
        """Ensure directory exists"""
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory: {path}")
        return path

    @staticmethod
    def clean_dir(path: Path, keep_structure: bool = False) -> None:
        """Clean directory contents"""
        if not path.exists():
            return

        for item in path.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except Exception as e:
                logger.error(f"Error cleaning {item}: {e}")

        logger.info(f"Cleaned directory: {path}")

    @staticmethod
    def copy_file(src: Path, dst: Path, overwrite: bool = True) -> Path:
        """Copy file safely"""
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and not overwrite:
            logger.warning(f"File exists, skipping: {dst}")
            return dst
        shutil.copy2(src, dst)
        logger.debug(f"Copied {src} to {dst}")
        return dst

    @staticmethod
    def list_files(
        directory: Path, extension: str = None, recursive: bool = False
    ) -> List[Path]:
        """List files in directory"""
        if not directory.exists():
            return []

        pattern = f"**/*{extension}" if recursive else f"*{extension}" if extension else "*"
        files = [
            f
            for f in directory.glob(pattern)
            if f.is_file() and (not extension or f.suffix == extension)
        ]
        return sorted(files)

    @staticmethod
    def get_file_size(path: Path) -> int:
        """Get file size in bytes"""
        if path.exists():
            return path.stat().st_size
        return 0

    @staticmethod
    def safe_remove(path: Path) -> bool:
        """Safely remove file or directory"""
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            logger.debug(f"Removed: {path}")
            return True
        except Exception as e:
            logger.error(f"Error removing {path}: {e}")
            return False
