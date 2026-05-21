"""
Render Engine - Combines scenes, audio, and music into final shorts
Uses FFmpeg for video composition
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..base_engine import BaseEngine
import subprocess
import os


class RenderEngine(BaseEngine):
    """Combines scenes into final YouTube Shorts"""

    def __init__(self):
        super().__init__("RenderEngine")

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate render input"""
        required = ["scene_videos", "output_path"]
        return all(key in input_data for key in required)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Render final short"""
        scene_videos = input_data.get("scene_videos", [])
        audio_path = input_data.get("audio_path")
        output_path = Path(input_data.get("output_path"))
        background_music = input_data.get("background_music")

        self.logger.info(f"Rendering short with {len(scene_videos)} scenes")

        # Filter out None/missing videos
        valid_videos = [v for v in scene_videos if v and Path(v).exists()]
        
        if not valid_videos:
            self.logger.error("No valid scene videos provided")
            return {
                "num_scenes": 0,
                "final_video": None,
                "status": "failed",
                "error": "No valid scene videos",
            }

        try:
            final_video = self._compose_with_ffmpeg(
                valid_videos, audio_path, background_music, output_path
            )

            if not final_video:
                raise Exception("FFmpeg composition failed")

            self.logger.info(f"✓ Final video rendered: {final_video}")

            return {
                "num_scenes": len(valid_videos),
                "final_video": str(final_video),
                "duration_seconds": self._calculate_duration(valid_videos),
                "status": "completed",
            }
        except Exception as e:
            self.logger.error(f"Render failed: {str(e)}")
            return {
                "num_scenes": len(valid_videos),
                "status": "failed",
                "error": str(e),
            }

    def _compose_with_ffmpeg(
        self,
        scene_videos: List[str],
        audio_path: Optional[str],
        background_music: Optional[str],
        output_path: Path,
    ) -> Optional[Path]:
        """Compose videos using FFmpeg"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_path = output_path / "final_short.mp4"

        try:
            # If only one scene, just use it directly
            if len(scene_videos) == 1:
                input_video = Path(scene_videos[0])
                if not input_video.exists():
                    self.logger.error(f"Input video not found: {input_video}")
                    return None

                # Use the single scene as final video with optional audio
                if audio_path and Path(audio_path).exists():
                    return self._add_audio_to_video(
                        input_video, audio_path, final_path
                    )
                else:
                    # Just copy if no audio
                    import shutil
                    shutil.copy(input_video, final_path)
                    self.logger.info(f"Single scene copied to: {final_path}")
                    return final_path

            # Multiple scenes: concatenate them
            concat_list_file = output_path / "concat_list.txt"
            with open(concat_list_file, "w") as f:
                for video in scene_videos:
                    if Path(video).exists():
                        f.write(f"file '{Path(video).absolute()}'\n")

            # Build FFmpeg command for concatenation
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list_file),
                "-c", "copy",
                "-y",  # Overwrite output
                str(final_path),
            ]

            self.logger.debug(f"Running FFmpeg: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                self.logger.error(f"FFmpeg error: {result.stderr}")
                return None

            self.logger.info(f"Video concatenation complete: {final_path}")

            # Add audio if provided
            if audio_path and Path(audio_path).exists():
                temp_path = output_path / "final_with_audio.mp4"
                self._add_audio_to_video(final_path, audio_path, temp_path)
                import shutil
                shutil.move(temp_path, final_path)

            # Clean up concat list
            concat_list_file.unlink(missing_ok=True)

            return final_path

        except subprocess.TimeoutExpired:
            self.logger.error("FFmpeg operation timed out")
            return None
        except Exception as e:
            self.logger.error(f"FFmpeg composition error: {str(e)}")
            return None

    def _add_audio_to_video(
        self, video_path: Path, audio_path: Path, output_path: Path
    ) -> Optional[Path]:
        """Add audio track to video using FFmpeg"""
        try:
            cmd = [
                "ffmpeg",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                "-y",  # Overwrite
                str(output_path),
            ]

            self.logger.debug(f"Adding audio with FFmpeg: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                self.logger.error(f"Audio mixing error: {result.stderr}")
                return None

            self.logger.info(f"Audio added to video: {output_path}")
            return output_path

        except subprocess.TimeoutExpired:
            self.logger.error("Audio mixing timed out")
            return None
        except Exception as e:
            self.logger.error(f"Audio mixing error: {str(e)}")
            return None

    def _calculate_duration(self, scene_videos: List[str]) -> float:
        """Calculate total duration from videos"""
        total_duration = 0
        try:
            for video in scene_videos:
                if Path(video).exists():
                    # Use ffprobe to get duration if available, otherwise estimate
                    try:
                        cmd = [
                            "ffprobe",
                            "-v", "error",
                            "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1:nokey=1",
                            str(video),
                        ]
                        result = subprocess.run(
                            cmd, capture_output=True, text=True, timeout=10
                        )
                        if result.returncode == 0:
                            duration = float(result.stdout.strip())
                            total_duration += duration
                        else:
                            total_duration += 2.0  # Default 2 seconds per scene
                    except Exception:
                        total_duration += 2.0  # Default 2 seconds per scene
                else:
                    total_duration += 2.0

            return total_duration
        except Exception:
            return len(scene_videos) * 2.0  # Fallback


__all__ = ["RenderEngine"]
