"""
Orchestrator - Main pipeline orchestration
Coordinates all engines to process historical ideas into shorts
"""

from typing import Dict, Any, Optional
from pathlib import Path
from .script_engine import ScriptEngine
from .prompt_engine import PromptEngine
from .narration_engine import NarrationEngine
from .scene_engine import SceneEngine
from .interpolation_engine import InterpolationEngine
from .render_engine import RenderEngine
from .workflow_engine import WorkflowEngine
from .batch_queue import BatchQueue, Job, JobStatus
from .utils import get_logger, FileManager
from config import DirectorAIConfig


class DirectorAIOrchestrator:
    """Main orchestrator coordinating all engines"""

    def __init__(self, config: DirectorAIConfig = None):
        self.config = config or DirectorAIConfig()
        self.logger = get_logger("DirectorAIOrchestrator")

        # Initialize all engines
        self.script_engine = ScriptEngine()
        self.prompt_engine = PromptEngine()
        self.narration_engine = NarrationEngine()
        self.scene_engine = SceneEngine()
        self.interpolation_engine = InterpolationEngine()
        self.render_engine = RenderEngine()
        self.workflow_engine = WorkflowEngine()

        # Initialize batch queue
        self.queue = BatchQueue()

    def generate_single_short(self, idea: str, short_id: int) -> Dict[str, Any]:
        """Generate a single historical short from an idea"""
        self.logger.info(f"Starting generation for short #{short_id}: {idea}")

        try:
            # Create output directories
            short_dir = self.config.get_short_output_dir(short_id, self.config.OUTPUTS_DIR)
            subdirs = self.config.get_output_subdirs(short_dir)

            # Step 1: Generate script
            self.logger.info("Step 1/8: Generating script...")
            script_result = self.script_engine.process({"idea": idea})
            scenes = script_result.get("scenes", [])
            self._save_json(
                subdirs["script"] / "script.json",
                {
                    "idea": idea,
                    "full_script": script_result.get("full_script"),
                    "scenes": scenes,
                },
            )

            # Step 2-4: Process each scene (prompt, narration, generation)
            scene_videos = []
            for scene_idx, scene in enumerate(scenes):
                self.logger.info(f"Processing scene {scene_idx + 1}/{len(scenes)}")

                # Generate prompt
                prompt_result = self.prompt_engine.process({"scene": scene})
                prompt = prompt_result.get("positive_prompt")

                # Generate narration
                narration_result = self.narration_engine.process(
                    {
                        "text": scene.get("narration", ""),
                        "output_path": subdirs["audio"] / f"scene_{scene_idx:02d}.wav",
                    }
                )

                # Generate and animate scene
                scene_result = self.scene_engine.process(
                    {
                        "prompt": prompt,
                        "negative_prompt": prompt_result.get("negative_prompt"),
                        "output_path": subdirs["scenes"] / f"scene_{scene_idx:02d}",
                    }
                )

                video_path = scene_result.get("video_path")
                if video_path:
                    scene_videos.append(video_path)

                # Step 5: Interpolate for smoothness
                self.logger.info(f"Interpolating scene {scene_idx + 1}...")
                interpolation_result = self.interpolation_engine.process(
                    {
                        "video_path": video_path,
                        "output_path": subdirs["renders"] / f"scene_{scene_idx:02d}",
                    }
                )

            # Step 6: Render final short
            self.logger.info("Step 6/8: Rendering final short...")
            render_result = self.render_engine.process(
                {
                    "scene_videos": scene_videos,
                    "audio_path": str(subdirs["audio"] / "narration.wav"),
                    "output_path": subdirs["final"],
                }
            )

            # Save metadata
            metadata = {
                "short_id": short_id,
                "idea": idea,
                "num_scenes": len(scenes),
                "final_video": render_result.get("final_video"),
                "status": "completed",
            }
            self._save_json(subdirs["metadata"] / "metadata.json", metadata)

            self.logger.info(f"✓ Short #{short_id} completed successfully")
            return {"status": "completed", "short_id": short_id, **metadata}

        except Exception as e:
            self.logger.error(f"Error generating short #{short_id}: {str(e)}")
            return {
                "status": "failed",
                "short_id": short_id,
                "idea": idea,
                "error": str(e),
            }

    def process_batch(self, ideas: list) -> Dict[str, Any]:
        """Process batch of ideas"""
        self.logger.info(f"Starting batch processing of {len(ideas)} ideas")

        # Add all ideas to queue
        jobs = self.queue.add_batch_ideas(ideas)

        results = []
        for job in jobs:
            self.queue.update_job_status(job.job_id, JobStatus.PROCESSING)

            result = self.generate_single_short(job.idea, job.job_id)

            if result.get("status") == "completed":
                self.queue.update_job_status(
                    job.job_id,
                    JobStatus.COMPLETED,
                    output_path=result.get("final_video"),
                )
            else:
                self.queue.update_job_status(
                    job.job_id, JobStatus.FAILED, error=result.get("error")
                )

            results.append(result)

        stats = self.queue.get_stats()
        self.logger.info(f"Batch processing complete. Stats: {stats}")

        return {"results": results, "stats": stats}

    def _save_json(self, path: Path, data: Dict) -> None:
        """Save JSON safely"""
        import json

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self.logger.debug(f"Saved: {path}")


__all__ = ["DirectorAIOrchestrator"]
