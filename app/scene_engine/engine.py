"""
Scene Engine - Generates and animates scenes
Uses ComfyUI for Stable Diffusion image generation
Uses AnimateDiff for animation
"""

from typing import Dict, Any, Optional
from pathlib import Path
from ..base_engine import BaseEngine
from ..utils.comfyui_client import ComfyUIClient
import os
import shutil


class SceneEngine(BaseEngine):
    """Generates and animates scenes"""

    def __init__(self, comfyui_server_url: str = "http://127.0.0.1:8188"):
        super().__init__("SceneEngine")
        self.comfyui_server_url = comfyui_server_url
        self.client = ComfyUIClient(comfyui_server_url)
        self.width = 540
        self.height = 960
        self.steps = 30
        self.sampler = "euler"
        self.scheduler = "normal"

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate scene input"""
        required = ["prompt", "output_path"]
        return all(key in input_data for key in required)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate scene image and animate it"""
        prompt = input_data.get("prompt", "")
        output_path = Path(input_data.get("output_path"))
        negative_prompt = input_data.get("negative_prompt", "low quality, blurry, distorted")
        scene_num = input_data.get("scene_num", 0)

        self.logger.info(f"Generating scene {scene_num}: {prompt[:50]}...")

        # Check if ComfyUI is available
        if not self.client.check_server_health():
            self.logger.error("ComfyUI server not responding at " + self.comfyui_server_url)
            return {
                "prompt": prompt,
                "image_path": None,
                "video_path": None,
                "status": "failed",
                "error": "ComfyUI server not available",
            }

        try:
            # Generate base image using ComfyUI + Stable Diffusion
            image_path = self._generate_image(prompt, negative_prompt, output_path)
            if not image_path:
                raise Exception("Failed to generate image")

            # Animate using AnimateDiff
            video_path = self._animate_scene(image_path, output_path)
            if not video_path:
                raise Exception("Failed to animate scene")

            self.logger.info(f"✓ Scene {scene_num} generated: {video_path}")

            return {
                "prompt": prompt,
                "image_path": str(image_path),
                "video_path": str(video_path),
                "duration_seconds": 2.0,  # AnimateDiff 16 frames at 8fps
                "fps": 8,
                "scene_num": scene_num,
                "status": "completed",
            }
        except Exception as e:
            self.logger.error(f"Scene generation failed: {str(e)}")
            return {
                "prompt": prompt,
                "status": "failed",
                "error": str(e),
            }

    def _generate_image(
        self, prompt: str, negative_prompt: str, output_dir: Path
    ) -> Optional[Path]:
        """Generate image using Stable Diffusion via ComfyUI"""
        output_dir.mkdir(parents=True, exist_ok=True)
        image_path = output_dir / "scene_image.png"

        try:
            # Create Stable Diffusion workflow
            workflow = self._create_sd_workflow(prompt, negative_prompt)

            # Queue the workflow
            self.logger.debug("Queueing Stable Diffusion workflow...")
            prompt_id = self.client.queue_prompt(workflow)
            if not prompt_id:
                self.logger.error("Failed to queue prompt")
                return None

            self.logger.debug(f"Workflow queued with ID: {prompt_id}")

            # Wait for completion
            if not self.client.wait_for_completion(prompt_id, max_wait=600):
                self.logger.error("Workflow execution timeout")
                return None

            self.logger.debug("Workflow completed, retrieving image...")

            # Get the generated image from ComfyUI output
            history = self.client.get_history(prompt_id)
            if not history or prompt_id not in history:
                self.logger.error("No history found for prompt")
                return None

            # Extract image path from workflow output
            image_found = self._extract_and_save_image(
                history[prompt_id], output_dir, image_path
            )
            if not image_found:
                self.logger.warning("Image extraction failed, using placeholder")
                # Create a placeholder if generation truly failed
                return None

            self.logger.info(f"Image saved to: {image_path}")
            return image_path

        except Exception as e:
            self.logger.error(f"Image generation error: {str(e)}")
            return None

    def _create_sd_workflow(self, prompt: str, negative_prompt: str) -> Dict[str, Any]:
        """Create Stable Diffusion workflow JSON for ComfyUI"""
        # This is a simplified workflow - adjust based on your model setup
        workflow = {
            "1": {
                "inputs": {
                    "ckpt_name": "realisticVisionV60B1_v60B1VAE.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Load Checkpoint"},
            },
            "2": {
                "inputs": {"text": prompt},
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP Text Encode (Positive)"},
            },
            "3": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["1", 1],
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP Text Encode (Negative)"},
            },
            "4": {
                "inputs": {
                    "width": self.width,
                    "height": self.height,
                    "batch_size": 1,
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Empty Latent Image"},
            },
            "5": {
                "inputs": {
                    "seed": 12345,
                    "steps": self.steps,
                    "cfg": 7.5,
                    "sampler_name": self.sampler,
                    "scheduler": self.scheduler,
                    "denoise": 1.0,
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["4", 0],
                },
                "class_type": "KSampler",
                "_meta": {"title": "KSampler"},
            },
            "6": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2],
                },
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE Decode"},
            },
            "7": {
                "inputs": {
                    "filename_prefix": "DirectorAI_scene",
                    "images": ["6", 0],
                },
                "class_type": "SaveImage",
                "_meta": {"title": "Save Image"},
            },
        }
        return workflow

    def _extract_and_save_image(
        self, output_data: Dict, output_dir: Path, target_path: Path
    ) -> bool:
        """Extract generated image from ComfyUI output and save it"""
        try:
            # ComfyUI saves images to its output directory
            # Check common locations
            comfyui_output = Path("/content/ComfyUI/output") if os.path.exists("/content/ComfyUI/output") else Path("./ComfyUI/output")
            
            if comfyui_output.exists():
                # Find the most recent PNG file in output
                pngs = list(comfyui_output.glob("**/*.png"))
                if pngs:
                    latest_png = max(pngs, key=lambda p: p.stat().st_mtime)
                    shutil.copy(latest_png, target_path)
                    self.logger.info(f"Copied image from {latest_png} to {target_path}")
                    return True
            
            self.logger.warning(f"ComfyUI output directory not found or empty")
            return False
        except Exception as e:
            self.logger.error(f"Image extraction error: {str(e)}")
            return False

    def _animate_scene(self, image_path: Path, output_dir: Path) -> Optional[Path]:
        """Animate scene using AnimateDiff in ComfyUI"""
        video_path = output_dir / "scene_animation.mp4"

        try:
            if not image_path or not image_path.exists():
                self.logger.error(f"Image path does not exist: {image_path}")
                return None

            self.logger.debug("Creating AnimateDiff workflow...")

            # Create AnimateDiff workflow
            workflow = self._create_animatediff_workflow(str(image_path))

            # Queue the workflow
            prompt_id = self.client.queue_prompt(workflow)
            if not prompt_id:
                self.logger.error("Failed to queue AnimateDiff prompt")
                return None

            self.logger.debug(f"AnimateDiff workflow queued: {prompt_id}")

            # Wait for completion
            if not self.client.wait_for_completion(prompt_id, max_wait=600):
                self.logger.error("AnimateDiff execution timeout")
                return None

            self.logger.debug("AnimateDiff completed, retrieving video...")

            # Extract video from ComfyUI output
            video_found = self._extract_and_save_video(output_dir, video_path)
            if not video_found:
                self.logger.warning("Video extraction failed")
                return None

            return video_path

        except Exception as e:
            self.logger.error(f"Animation error: {str(e)}")
            return None

    def _create_animatediff_workflow(self, image_path: str) -> Dict[str, Any]:
        """Create AnimateDiff workflow JSON for ComfyUI"""
        workflow = {
            "1": {
                "inputs": {"ckpt_name": "realisticVisionV60B1_v60B1VAE.safetensors"},
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Load Checkpoint"},
            },
            "2": {
                "inputs": {"image": "scene_image.png"},
                "class_type": "LoadImage",
                "_meta": {"title": "Load Image"},
            },
            "3": {
                "inputs": {
                    "motion_model": "mm_sd_v15_v2.ckpt",
                    "model": ["1", 0],
                    "seed": 12345,
                    "length": 16,
                    "overlap": 4,
                    "context_length": 16,
                    "context_stride": 1,
                    "context_overlap": 4,
                    "steps": 20,
                    "cfg": 7.5,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "image": ["2", 0],
                    "vae": ["1", 2],
                },
                "class_type": "AnimateDiffLoader",
                "_meta": {"title": "AnimateDiff Loader"},
            },
            "4": {
                "inputs": {
                    "filename_prefix": "DirectorAI_animation",
                    "format": "video/mp4",
                    "fps": 8,
                    "images": ["3", 0],
                },
                "class_type": "VHS_VideoCombine",
                "_meta": {"title": "Combine Frames to Video"},
            },
        }
        return workflow

    def _extract_and_save_video(self, output_dir: Path, target_path: Path) -> bool:
        """Extract generated video from ComfyUI output"""
        try:
            comfyui_output = Path("/content/ComfyUI/output") if os.path.exists("/content/ComfyUI/output") else Path("./ComfyUI/output")
            
            if comfyui_output.exists():
                # Find the most recent MP4 file
                videos = list(comfyui_output.glob("**/*.mp4"))
                if videos:
                    latest_video = max(videos, key=lambda p: p.stat().st_mtime)
                    shutil.copy(latest_video, target_path)
                    self.logger.info(f"Copied video from {latest_video} to {target_path}")
                    return True
            
            self.logger.warning("No video output found from ComfyUI")
            return False
        except Exception as e:
            self.logger.error(f"Video extraction error: {str(e)}")
            return False


__all__ = ["SceneEngine"]
