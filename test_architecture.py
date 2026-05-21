"""
DirectorAI Quick Test Script
Verify the modular architecture without actual generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.orchestrator import DirectorAIOrchestrator
from config import DirectorAIConfig
from app.utils import get_logger

logger = get_logger("QuickTest")


def test_architecture():
    """Test that all modules load correctly"""

    logger.info("=" * 60)
    logger.info("DirectorAI Architecture Test")
    logger.info("=" * 60)

    # Initialize
    config = DirectorAIConfig()
    orchestrator = DirectorAIOrchestrator(config)

    logger.info("\n✓ Configuration loaded")
    logger.info(f"  Output dir: {config.OUTPUTS_DIR}")
    logger.info(f"  Temp dir: {config.TEMP_DIR}")

    # Test script engine
    logger.info("\n✓ Script Engine initialized")
    script_result = orchestrator.script_engine.process(
        {"idea": "An ancient emperor's rise to power"}
    )
    logger.info(f"  Scenes generated: {script_result.get('num_scenes')}")

    # Test prompt engine
    logger.info("\n✓ Prompt Engine initialized")
    if script_result.get("scenes"):
        prompt_result = orchestrator.prompt_engine.process(
            {"scene": script_result["scenes"][0]}
        )
        logger.info(f"  Prompt quality: {prompt_result.get('prompt_quality')}")

    # Test narration engine
    logger.info("\n✓ Narration Engine initialized")
    narration_result = orchestrator.narration_engine.process(
        {
            "text": "In the annals of history...",
            "output_path": config.TEMP_DIR / "test_narration.wav",
        }
    )
    logger.info(f"  Duration estimate: {narration_result.get('duration_seconds'):.1f}s")

    # Test batch queue
    logger.info("\n✓ Batch Queue initialized")
    test_ideas = ["Idea 1", "Idea 2", "Idea 3"]
    jobs = orchestrator.queue.add_batch_ideas(test_ideas)
    stats = orchestrator.queue.get_stats()
    logger.info(f"  Queue stats: {stats}")

    logger.info("\n" + "=" * 60)
    logger.info("✓ All engines loaded successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    test_architecture()
