"""
DirectorAI Configuration Management
Handles all system paths, model configs, and generation parameters
"""

import os
from pathlib import Path
from typing import Dict, Any


class DirectorAIConfig:
    """Central configuration for DirectorAI system"""

    def __init__(self, base_path: str = None):
        """Initialize configuration with optional base path override"""
        if base_path:
            self.BASE_DIR = Path(base_path)
        else:
            self.BASE_DIR = Path(__file__).parent

        # Core directories
        self.APP_DIR = self.BASE_DIR / "app"
        self.WORKFLOWS_DIR = self.BASE_DIR / "workflows"
        self.MODELS_DIR = self.BASE_DIR / "models"
        self.OUTPUTS_DIR = self.BASE_DIR / "outputs"
        self.TEMP_DIR = self.BASE_DIR / "temp"
        self.SCRIPTS_DIR = self.BASE_DIR / "scripts"
        self.COMFYUI_DIR = self.BASE_DIR / "comfyui"

        # Create directories if they don't exist
        for directory in [
            self.OUTPUTS_DIR,
            self.TEMP_DIR,
            self.WORKFLOWS_DIR,
            self.MODELS_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    # Model configurations
    MODELS = {
        "primary": {
            "name": "realisticVisionV60B1_v60B1VAE",
            "filename": "realisticVisionV60B1_v60B1VAE.safetensors",
            "type": "checkpoint",
        },
        "secondary": {
            "name": "v1-5-pruned-emaonly",
            "filename": "v1-5-pruned-emaonly.safetensors",
            "type": "checkpoint",
        },
        "vae": {
            "name": "vae-ft-mse-840000-ema-pruned",
            "filename": "vae-ft-mse-840000-ema-pruned.safetensors",
            "type": "vae",
        },
    }

    # Generation parameters
    GENERATION_PARAMS = {
        "script": {
            "max_scenes": 8,
            "words_per_scene": 50,
            "style": "cinematic_historical",
        },
        "image": {
            "width": 540,
            "height": 960,
            "steps": 30,
            "guidance_scale": 7.5,
        },
        "animation": {
            "frames": 16,
            "fps": 8,
            "duration_seconds": 3,
        },
        "narration": {
            "language": "en",
            "voice_id": "default",
            "speed": 0.9,
        },
    }

    # Batch processing
    BATCH_CONFIG = {
        "max_concurrent_renders": 1,
        "max_retries": 3,
        "timeout_seconds": 3600,
    }

    # ComfyUI configuration
    COMFYUI_CONFIG = {
        "server_url": "http://127.0.0.1:8188",
        "websocket_url": "ws://127.0.0.1:8188/ws",
        "timeout": 300,
    }

    # Output structure
    OUTPUT_STRUCTURE = {
        "script": "script/",
        "audio": "audio/",
        "scenes": "scenes/",
        "renders": "renders/",
        "metadata": "metadata/",
        "final": "final/",
    }

    @classmethod
    def get_short_output_dir(cls, short_id: int, base_output: Path = None) -> Path:
        """Get output directory for a specific short"""
        if base_output is None:
            base_output = cls().OUTPUTS_DIR
        short_dir = base_output / f"short_{short_id:03d}"
        short_dir.mkdir(parents=True, exist_ok=True)
        return short_dir

    @classmethod
    def get_output_subdirs(cls, short_dir: Path) -> Dict[str, Path]:
        """Get all subdirectories for a short"""
        subdirs = {}
        for key, subdir in cls.OUTPUT_STRUCTURE.items():
            path = short_dir / subdir
            path.mkdir(parents=True, exist_ok=True)
            subdirs[key] = path
        return subdirs


# Global config instance
config = DirectorAIConfig()
