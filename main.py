"""
Main entry point for DirectorAI
Supports single short generation and batch processing
Works on local machine and Google Colab
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.orchestrator import DirectorAIOrchestrator
from config import DirectorAIConfig
from app.utils import get_logger

logger = get_logger("DirectorAI")


def detect_environment() -> str:
    """Detect if running in Colab or locally"""
    try:
        import google.colab
        return "colab"
    except ImportError:
        return "local"


def main():
    parser = argparse.ArgumentParser(
        description="DirectorAI - Cinematic YouTube Shorts Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single short
  python main.py --mode single --idea "Cleopatra ruling Egypt"
  
  # Batch processing
  python main.py --mode batch --ideas-file prompts.json
  
  # Custom output directory
  python main.py --mode batch --ideas-file prompts.json --output-dir /path/to/output
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["single", "batch"],
        default="single",
        help="Generation mode (default: single)",
    )
    parser.add_argument(
        "--idea",
        type=str,
        help="Single historical idea for generation",
    )
    parser.add_argument(
        "--ideas-file",
        type=str,
        help="JSON file with list of ideas for batch processing",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Custom output directory (default: ./outputs)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Detect environment
    env = detect_environment()
    if env == "colab":
        logger.info("Running in Google Colab")
    else:
        logger.info("Running locally")

    # Initialize
    config = DirectorAIConfig(args.output_dir)
    orchestrator = DirectorAIOrchestrator(config)

    logger.info("=" * 60)
    logger.info("DirectorAI - Cinematic YouTube Shorts Generator")
    logger.info("=" * 60)
    logger.info(f"Output directory: {config.OUTPUTS_DIR}\n")

    if args.mode == "single":
        if not args.idea:
            logger.error("--idea required for single mode")
            logger.error("Example: python main.py --mode single --idea \"Cleopatra ruling Egypt\"")
            sys.exit(1)

        result = orchestrator.generate_single_short(args.idea, short_id=1)

        logger.info("\n" + "=" * 60)
        if result.get("status") == "completed":
            logger.info(f"✓ Generation successful!")
            logger.info(f"  Output: {result.get('final_video')}")
        else:
            logger.error(f"✗ Generation failed: {result.get('error')}")
        logger.info("=" * 60)

    elif args.mode == "batch":
        if not args.ideas_file:
            logger.error("--ideas-file required for batch mode")
            logger.error("Example: python main.py --mode batch --ideas-file prompts.json")
            sys.exit(1)

        import json

        ideas_path = Path(args.ideas_file)
        if not ideas_path.exists():
            logger.error(f"Ideas file not found: {ideas_path}")
            sys.exit(1)

        try:
            with open(ideas_path, "r") as f:
                data = json.load(f)

            if isinstance(data, dict) and "ideas" in data:
                ideas = data["ideas"]
            elif isinstance(data, list):
                ideas = data
            else:
                logger.error("Ideas file must contain 'ideas' array or be a list")
                sys.exit(1)

            logger.info(f"Loaded {len(ideas)} ideas from {ideas_path.name}\n")

            results = orchestrator.process_batch(ideas)

            logger.info("\n" + "=" * 60)
            logger.info("Batch Generation Complete")
            logger.info("=" * 60)
            logger.info(f"Results: {results['stats']}")

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {ideas_path}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
