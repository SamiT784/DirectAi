"""
Logging system for DirectorAI
Provides structured logging for all operations
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


class DirectorAILogger:
    """Centralized logging system"""

    _instances = {}

    def __new__(cls, name: str):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

        # Avoid adding multiple handlers
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(console_format)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


def get_logger(name: str) -> DirectorAILogger:
    """Get or create logger instance"""
    return DirectorAILogger(name)
