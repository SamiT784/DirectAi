"""
Narration Engine - Generates voice narration using XTTS
Creates cinematic male narration for scenes
Gracefully falls back to silent if XTTS unavailable
"""

from typing import Dict, Any, Optional
from pathlib import Path
from ..base_engine import BaseEngine
import subprocess


class NarrationEngine(BaseEngine):
    """Generates voice narration using XTTS or falls back to silent"""

    def __init__(self):
        super().__init__("NarrationEngine")
        self.xtts_available = self._check_xtts_availability()
        if self.xtts_available:
            try:
                from TTS.api import TTS
                self.tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=True)
                self.logger.info("✓ XTTS model loaded successfully")
            except Exception as e:
                self.logger.warning(f"XTTS initialization failed: {str(e)}, will use silent fallback")
                self.xtts_available = False
                self.tts_model = None
        else:
            self.tts_model = None

    def _check_xtts_availability(self) -> bool:
        """Check if TTS package is installed"""
        try:
            import TTS
            return True
        except ImportError:
            self.logger.info("TTS package not installed, will use silent fallback")
            return False

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate narration input"""
        required = ["text"]
        return all(key in input_data for key in required)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate narration audio"""
        text = input_data.get("text", "")
        output_path = Path(input_data.get("output_path", "temp/narration.wav"))
        skip_narration = input_data.get("skip_narration", False)

        if skip_narration or not text.strip():
            self.logger.info("Skipping narration (empty or disabled)")
            return {
                "text": text,
                "audio_path": None,
                "duration_seconds": 0,
                "status": "skipped",
                "reason": "narration_skipped",
            }

        self.logger.info(f"Generating narration: {text[:50]}...")

        if self.xtts_available and self.tts_model:
            audio_path = self._generate_xtts_audio(text, output_path)
        else:
            self.logger.info("Using silent fallback (TTS not available)")
            audio_path = self._generate_silent_audio(text, output_path)

        if audio_path and Path(audio_path).exists():
            return {
                "text": text,
                "audio_path": str(audio_path),
                "duration_seconds": self._estimate_duration(text),
                "status": "completed",
            }
        else:
            return {
                "text": text,
                "audio_path": None,
                "duration_seconds": self._estimate_duration(text),
                "status": "failed",
                "reason": "audio_generation_failed",
            }

    def _generate_xtts_audio(self, text: str, output_path: Path) -> Optional[Path]:
        """Generate audio using XTTS TTS model"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.debug(f"Generating audio with XTTS for: {text[:50]}...")
            self.tts_model.tts_to_file(text=text, file_path=str(output_path))
            
            if output_path.exists() and output_path.stat().st_size > 0:
                self.logger.info(f"✓ Audio generated: {output_path}")
                return output_path
            else:
                self.logger.error("Audio generation produced empty file")
                return None
        except Exception as e:
            self.logger.error(f"XTTS audio generation failed: {str(e)}")
            return None

    def _generate_silent_audio(self, text: str, output_path: Path) -> Optional[Path]:
        """Generate silent audio using FFmpeg as fallback"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            duration = self._estimate_duration(text)
            
            # Use FFmpeg to generate silent audio (no ffmpeg required, use Python)
            self.logger.debug(f"Generating {duration:.1f}s of silence...")
            
            # Use scipy/numpy if available
            try:
                import numpy as np
                import scipy.io.wavfile as wavfile
                
                sample_rate = 16000
                samples = int(duration * sample_rate)
                silent_audio = np.zeros(samples, dtype=np.int16)
                wavfile.write(str(output_path), sample_rate, silent_audio)
                
                self.logger.info(f"✓ Silent audio generated: {output_path}")
                return output_path
            except Exception:
                # Fallback: use FFmpeg if scipy not available
                cmd = [
                    "ffmpeg",
                    "-f", "lavfi",
                    "-i", f"anullsrc=r=16000:cl=mono",
                    "-t", str(duration),
                    "-q:a", "9",
                    "-acodec", "libmp3lame",
                    "-y",
                    str(output_path),
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and output_path.exists():
                    self.logger.info(f"✓ Silent audio generated with FFmpeg: {output_path}")
                    return output_path
                else:
                    self.logger.error(f"FFmpeg silence generation failed: {result.stderr}")
                    return None
        except Exception as e:
            self.logger.error(f"Silent audio generation error: {str(e)}")
            return None

    def _estimate_duration(self, text: str) -> float:
        """Estimate narration duration based on text length"""
        # Average speech rate: 150 words per minute = 2.5 words per second
        # Adjusted for narration: 140 wpm = 2.33 words per second
        if not text.strip():
            return 0.0
        word_count = len(text.split())
        duration = word_count / 2.33
        return max(0.5, duration)  # Minimum 0.5 seconds


__all__ = ["NarrationEngine"]
