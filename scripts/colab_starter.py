"""
DirectorAI Enhanced Colab Starter Script
Complete setup and generation workflow for Google Colab
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import List, Optional

# Setup paths
REPO_DIR = Path("/content/DirectorAI")
sys.path.insert(0, str(REPO_DIR))

# Import DirectorAI
from app.orchestrator import DirectorAIOrchestrator
from config import DirectorAIConfig
from app.utils import get_logger

logger = get_logger("ColabStarter")

# Global configuration
DRIVE_MOUNT_POINT = Path("/content/drive")
DRIVE_MODELS_DIR = DRIVE_MOUNT_POINT / "MyDrive" / "DirectorAI_Models"
DRIVE_OUTPUT_DIR = DRIVE_MOUNT_POINT / "MyDrive" / "DirectorAI_Results"
LOCAL_MODELS_DIR = REPO_DIR / "models"


class ColabSetup:
    """Handles Google Colab setup and configuration"""

    @staticmethod
    def mount_drive() -> bool:
        """Mount Google Drive"""
        try:
            from google.colab import drive

            drive.mount(str(DRIVE_MOUNT_POINT), force_remount=True)
            logger.info("✓ Google Drive mounted successfully")
            return True
        except ImportError:
            logger.error("✗ Not running in Google Colab")
            return False
        except Exception as e:
            logger.error(f"✗ Failed to mount Drive: {e}")
            return False

    @staticmethod
    def verify_models_on_drive() -> bool:
        """Verify models exist on Drive"""
        required_files = [
            "checkpoints/realisticVisionV60B1_v60B1VAE.safetensors",
            "checkpoints/v1-5-pruned-emaonly.safetensors",
            "checkpoints/mm_sd_v15_v2.ckpt",
            "vae/vae-ft-mse-840000-ema-pruned.safetensors",
        ]

        logger.info("Verifying models on Drive...")
        all_found = True

        for model_file in required_files:
            model_path = DRIVE_MODELS_DIR / model_file
            if model_path.exists():
                size_mb = model_path.stat().st_size / (1024 * 1024)
                logger.info(f"✓ {model_file} ({size_mb:.0f} MB)")
            else:
                logger.warning(f"✗ {model_file} NOT FOUND at {model_path}")
                all_found = False

        return all_found

    @staticmethod
    def copy_models_to_colab() -> bool:
        """Copy models from Drive to Colab (faster local storage)"""
        logger.info("\nCopying models from Drive to Colab storage...")

        try:
            # Ensure local directories exist
            LOCAL_MODELS_DIR.mkdir(parents=True, exist_ok=True)
            (LOCAL_MODELS_DIR / "checkpoints").mkdir(parents=True, exist_ok=True)
            (LOCAL_MODELS_DIR / "vae").mkdir(parents=True, exist_ok=True)

            # Copy checkpoint models
            checkpoint_models = [
                "realisticVisionV60B1_v60B1VAE.safetensors",
                "v1-5-pruned-emaonly.safetensors",
                "mm_sd_v15_v2.ckpt",
            ]

            for model_file in checkpoint_models:
                src = DRIVE_MODELS_DIR / "checkpoints" / model_file
                dst = LOCAL_MODELS_DIR / "checkpoints" / model_file

                if src.exists():
                    size_mb = src.stat().st_size / (1024 * 1024)
                    logger.info(f"Copying {model_file} ({size_mb:.0f} MB)...")
                    shutil.copy2(src, dst)
                    logger.info(f"✓ {model_file} copied to Colab")
                else:
                    logger.warning(f"⚠ {model_file} not found on Drive")

            # Copy VAE
            vae_src = DRIVE_MODELS_DIR / "vae" / "vae-ft-mse-840000-ema-pruned.safetensors"
            vae_dst = LOCAL_MODELS_DIR / "vae" / "vae-ft-mse-840000-ema-pruned.safetensors"

            if vae_src.exists():
                size_mb = vae_src.stat().st_size / (1024 * 1024)
                logger.info(f"Copying VAE model ({size_mb:.0f} MB)...")
                shutil.copy2(vae_src, vae_dst)
                logger.info("✓ VAE model copied to Colab")
            else:
                logger.warning("⚠ VAE model not found on Drive")

            return True

        except Exception as e:
            logger.error(f"✗ Error copying models: {e}")
            return False

    @staticmethod
    def load_prompts(prompts_file: Path) -> Optional[List[str]]:
        """Load prompts from JSON file"""
        try:
            if not prompts_file.exists():
                logger.error(f"Prompts file not found: {prompts_file}")
                return None

            with open(prompts_file, "r") as f:
                data = json.load(f)

            ideas = data.get("ideas", [])
            if not ideas:
                logger.error("No ideas found in prompts file")
                return None

            logger.info(f"✓ Loaded {len(ideas)} ideas from {prompts_file.name}")
            for idx, idea in enumerate(ideas, 1):
                logger.info(f"  {idx}. {idea[:60]}...")

            return ideas

        except json.JSONDecodeError:
            logger.error("Invalid JSON in prompts file")
            return None
        except Exception as e:
            logger.error(f"Error loading prompts: {e}")
            return None

    @staticmethod
    def create_output_dirs() -> bool:
        """Create output directories"""
        try:
            REPO_DIR.joinpath("outputs").mkdir(parents=True, exist_ok=True)
            REPO_DIR.joinpath("temp").mkdir(parents=True, exist_ok=True)
            DRIVE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            logger.info("✓ Output directories created")
            return True
        except Exception as e:
            logger.error(f"✗ Error creating directories: {e}")
            return False


class ColabGenerator:
    """Handles DirectorAI generation in Colab"""

    def __init__(self):
        self.config = DirectorAIConfig(str(REPO_DIR))
        self.orchestrator = DirectorAIOrchestrator(self.config)

    def generate_batch(self, ideas: List[str]) -> dict:
        """Generate batch of shorts"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting batch generation for {len(ideas)} ideas")
        logger.info(f"{'='*60}\n")

        results = self.orchestrator.process_batch(ideas)
        return results

    def generate_single(self, idea: str, short_id: int = 1) -> dict:
        """Generate single short"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Generating short #{short_id}: {idea}")
        logger.info(f"{'='*60}\n")

        result = self.orchestrator.generate_single_short(idea, short_id)
        return result

    def copy_results_to_drive(self) -> bool:
        """Copy results from Colab to Google Drive"""
        try:
            source = REPO_DIR / "outputs"
            destination = DRIVE_OUTPUT_DIR

            if not source.exists():
                logger.warning("No outputs to copy")
                return False

            logger.info(f"Copying results to Drive...")
            shutil.copytree(source, destination, dirs_exist_ok=True)
            logger.info(f"✓ Results copied to {destination}")
            return True

        except Exception as e:
            logger.error(f"✗ Error copying results: {e}")
            return False

    def show_progress(self) -> None:
        """Display current generation progress"""
        queue_file = REPO_DIR / "queue.json"

        if not queue_file.exists():
            logger.info("No queue file yet")
            return

        try:
            with open(queue_file, "r") as f:
                queue_data = json.load(f)

            jobs = queue_data.get("jobs", [])
            logger.info(f"\nQueue Status:")
            logger.info(f"Total jobs: {len(jobs)}")

            for job in jobs:
                status = job["status"]
                idea = job["idea"][:50]
                logger.info(f"  Job {job['job_id']:3d}: {status:12s} - {idea}...")

        except Exception as e:
            logger.error(f"Error reading queue: {e}")


def main():
    """Main Colab workflow"""

    logger.info("\n" + "="*60)
    logger.info("DIRECTORAI - GOOGLE COLAB SETUP")
    logger.info("="*60 + "\n")

    # Step 1: Mount Drive
    logger.info("[STEP 1] Mounting Google Drive...")
    if not ColabSetup.mount_drive():
        logger.error("Failed to mount Drive. Make sure you're running in Colab.")
        return

    # Step 2: Verify models
    logger.info("\n[STEP 2] Verifying models on Drive...")
    if not ColabSetup.verify_models_on_drive():
        logger.error(
            "Some models missing on Drive. Upload them first to DirectorAI_Models/"
        )
        return

    # Step 3: Copy models
    logger.info("\n[STEP 3] Copying models to Colab...")
    if not ColabSetup.copy_models_to_colab():
        logger.error("Failed to copy models")
        return

    # Step 4: Create output dirs
    logger.info("\n[STEP 4] Creating output directories...")
    ColabSetup.create_output_dirs()

    # Step 5: Load prompts
    logger.info("\n[STEP 5] Loading prompts...")
    prompts_file = REPO_DIR / "prompts.json"

    if not prompts_file.exists():
        logger.warning(f"Prompts file not found at {prompts_file}")
        logger.info("Using sample ideas for testing...")
        ideas = [
            "The rise of Cleopatra VII, the last pharaoh of ancient Egypt",
            "The eruption of Mount Vesuvius in 79 AD",
            "Joan of Arc leading the French army to victory",
        ]
    else:
        ideas = ColabSetup.load_prompts(prompts_file)
        if not ideas:
            logger.error("Failed to load prompts")
            return

    # Step 6: Generate
    logger.info("\n[STEP 6] Starting generation...")
    generator = ColabGenerator()

    if len(ideas) == 1:
        result = generator.generate_single(ideas[0], short_id=1)
    else:
        result = generator.generate_batch(ideas)

    # Step 7: Show progress
    logger.info("\n[STEP 7] Current progress:")
    generator.show_progress()

    # Step 8: Copy to Drive
    logger.info("\n[STEP 8] Copying results to Google Drive...")
    generator.copy_results_to_drive()

    logger.info("\n" + "="*60)
    logger.info("✓ Colab setup and generation complete!")
    logger.info(f"Results saved to: {DRIVE_OUTPUT_DIR}")
    logger.info("="*60 + "\n")


if __name__ == "__main__":
    main()
