"""
ComfyUI Workflow Templates
Reusable JSON workflow templates for common tasks
"""

def get_image_generation_workflow(
    checkpoint_name: str,
    positive_prompt: str,
    negative_prompt: str,
    width: int = 768,
    height: int = 432,
    steps: int = 30,
    guidance_scale: float = 7.5,
    seed: int = 0,
) -> dict:
    """
    Create a Stable Diffusion image generation workflow
    Ready to be executed via ComfyUI API
    """
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": checkpoint_name},
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": positive_prompt, "clip": [1, 1]},
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": negative_prompt, "clip": [1, 1]},
        },
        "4": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": guidance_scale,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": [1, 0],
                "positive": [2, 0],
                "negative": [3, 0],
            },
        },
        "5": {
            "class_type": "VAEDecode",
            "inputs": {"samples": [4, 0], "vae": [1, 2]},
        },
        "6": {
            "class_type": "SaveImage",
            "inputs": {"images": [5, 0], "filename_prefix": "DirectorAI"},
        },
    }
    return workflow


def get_animatediff_workflow(
    base_image_path: str,
    checkpoint_name: str,
    prompt: str,
    motion_scale: int = 100,
    frames: int = 16,
    fps: int = 8,
) -> dict:
    """
    Create an AnimateDiff animation workflow
    Takes a base image and generates animation
    """
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": checkpoint_name},
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": [1, 1]},
        },
        "3": {
            "class_type": "LoadImage",
            "inputs": {"image": base_image_path},
        },
        "4": {
            "class_type": "AnimateDiffLoader",
            "inputs": {"model": "mm_sd_v15_v2.ckpt"},
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "seed": 0,
                "steps": 25,
                "cfg": 7.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 0.5,
                "model": [1, 0],
                "positive": [2, 0],
                "negative": [2, 0],
            },
        },
        "6": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": [5, 0],
                "frame_rate": fps,
                "loop_count": 0,
                "filename_prefix": "animation",
            },
        },
    }
    return workflow


__all__ = ["get_image_generation_workflow", "get_animatediff_workflow"]
