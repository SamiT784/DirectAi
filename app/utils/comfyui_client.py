"""
ComfyUI Integration Helper
Handles communication with ComfyUI server
"""

import requests
import json
import websocket
from typing import Dict, Any, Optional
from pathlib import Path
import time


class ComfyUIClient:
    """Client for communicating with ComfyUI server"""

    def __init__(self, server_url: str = "http://127.0.0.1:8188"):
        self.server_url = server_url
        self.api_url = f"{server_url}/api"
        self.timeout = 300

    def check_server_health(self) -> bool:
        """Check if ComfyUI server is running"""
        try:
            response = requests.get(f"{self.api_url}/system_stats", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"ComfyUI server not responding: {e}")
            return False

    def queue_prompt(self, workflow: Dict[str, Any]) -> Optional[str]:
        """Queue a workflow for execution"""
        try:
            payload = {"prompt": workflow}
            response = requests.post(
                f"{self.api_url}/prompt",
                json=payload,
                timeout=self.timeout,
            )
            if response.status_code == 200:
                result = response.json()
                prompt_id = result.get("prompt_id")
                return prompt_id
            else:
                print(f"Error queueing prompt: {response.text}")
                return None
        except Exception as e:
            print(f"Error communicating with ComfyUI: {e}")
            return None

    def get_history(self, prompt_id: str) -> Optional[Dict]:
        """Get execution history of a prompt"""
        try:
            response = requests.get(
                f"{self.api_url}/history/{prompt_id}",
                timeout=self.timeout,
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting history: {e}")
            return None

    def wait_for_completion(
        self, prompt_id: str, max_wait: int = 3600
    ) -> bool:
        """Wait for prompt execution to complete"""
        start_time = time.time()
        while time.time() - start_time < max_wait:
            history = self.get_history(prompt_id)
            if history and prompt_id in history:
                return True
            time.sleep(5)
        return False

    def upload_image(self, image_path: Path) -> bool:
        """Upload image to ComfyUI"""
        try:
            with open(image_path, "rb") as f:
                files = {"image": f}
                response = requests.post(
                    f"{self.api_url}/upload/image",
                    files=files,
                    timeout=self.timeout,
                )
            return response.status_code == 200
        except Exception as e:
            print(f"Error uploading image: {e}")
            return False


__all__ = ["ComfyUIClient"]
