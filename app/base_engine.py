"""
Base engine interface for all DirectorAI engines
Provides common interface and error handling
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .utils import get_logger


class BaseEngine(ABC):
    """Abstract base class for all engines"""

    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(name)

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return output
        Must be implemented by subclasses
        """
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Override in subclass for custom validation"""
        return True

    def on_error(self, error: Exception) -> None:
        """Handle errors gracefully"""
        self.logger.error(f"Error in {self.name}: {str(error)}")

    def __call__(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make engine callable"""
        try:
            if not self.validate_input(input_data):
                raise ValueError("Input validation failed")
            return self.process(input_data)
        except Exception as e:
            self.on_error(e)
            raise
