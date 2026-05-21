"""
Prompt Engine - Generates cinematic prompts for image/video generation
Creates prompts for Stable Diffusion based on scenes
"""

from typing import Dict, Any, List
from ..base_engine import BaseEngine


class PromptEngine(BaseEngine):
    """Generates cinematic image prompts"""

    def __init__(self):
        super().__init__("PromptEngine")
        self.style_components = {
            "lighting": [
                "dramatic rim lighting",
                "volumetric god rays",
                "cinematic golden hour",
                "moody shadows",
            ],
            "camera": ["wide shot", "close-up", "tracking shot", "aerial view"],
            "quality": ["masterpiece", "cinematic", "4k", "detailed"],
            "historical": [
                "historically accurate",
                "period-appropriate",
                "authentic artifacts",
            ],
        }

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate prompt input"""
        required = ["scene"]
        return all(key in input_data for key in required)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cinematic prompt for scene"""
        scene = input_data.get("scene", {})
        narration = scene.get("narration", "")
        scene_title = scene.get("title", "")

        self.logger.info(f"Generating prompt for scene: {scene_title}")

        prompt = self._build_prompt(narration, scene_title)
        negative_prompt = self._build_negative_prompt()

        return {
            "scene_title": scene_title,
            "positive_prompt": prompt,
            "negative_prompt": negative_prompt,
            "prompt_quality": "cinematic",
            "status": "completed",
        }

    def _build_prompt(self, narration: str, scene_title: str) -> str:
        """Build detailed cinematic prompt"""
        # TODO: Use LLM to enhance prompt from narration
        base = f"{scene_title}, {narration}"

        # Add cinematic elements
        enhanced = f"{base}, {self.style_components['lighting'][0]}, {self.style_components['camera'][0]}, {self.style_components['quality'][0]}"

        return enhanced

    def _build_negative_prompt(self) -> str:
        """Build negative prompt to avoid unwanted elements"""
        negatives = [
            "blurry",
            "distorted",
            "amateur",
            "low quality",
            "watermark",
            "text",
            "deformed",
        ]
        return ", ".join(negatives)


__all__ = ["PromptEngine"]
