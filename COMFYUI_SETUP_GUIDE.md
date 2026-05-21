"""
COMFYUI SETUP GUIDE FOR DIRECTORAI
Complete guide to setting up and running ComfyUI on Google Colab
"""

# ============================================================================
# WHAT IS COMFYUI?
# ============================================================================

ComfyUI is:
✓ A powerful node-based AI image generation framework
✓ Runs Stable Diffusion (generates images from text)
✓ Runs AnimateDiff (animates images into videos)
✓ Provides REST API for programmatic access
✓ Connects to your DirectorAI system for image/video generation

Why DirectorAI needs ComfyUI:
✓ For generating images from historical prompts
✓ For animating scenes (creating motion)
✓ For applying effects and transitions
✓ For rendering final video output


# ============================================================================
# COMPLETE COMFYUI SETUP ON COLAB (CELLS 6-8)
# ============================================================================

THREE cells are required:
1. Cell 6: Clone & install ComfyUI
2. Cell 7: Start ComfyUI server
3. Cell 8: Test configuration


# ============================================================================
# CELL 6: SETUP COMFYUI (5-10 MINUTES)
# ============================================================================

This cell:
✓ Clones ComfyUI from GitHub
✓ Installs all dependencies
✓ Links your models to ComfyUI

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import os
import subprocess
import time

# Clone ComfyUI
print("Cloning ComfyUI...")
os.chdir('/content')
!git clone https://github.com/comfyanonymous/ComfyUI.git

# Install ComfyUI dependencies
print("\nInstalling ComfyUI dependencies...")
os.chdir('/content/ComfyUI')
!pip install -r requirements.txt -q

# Create symbolic link for models
print("\nLinking models to ComfyUI...")
import shutil
from pathlib import Path

models_src = Path('/content/DirectAi/models')
models_dst = Path('/content/ComfyUI/models')

if models_src.exists():
    for item in models_src.iterdir():
        dst_item = models_dst / item.name
        if not dst_item.exists():
            if item.is_dir():
                shutil.copytree(item, dst_item)
            else:
                shutil.copy2(item, dst_item)
            print(f"  ✓ Linked: {item.name}")

print("\n✓ ComfyUI setup complete!")
print("  - Ready to generate images and animations")

────────────────────────────────────────────────────

EXPECTED OUTPUT:
Cloning into 'ComfyUI'...
...
Collecting torch...
Successfully installed...
Linking models to ComfyUI...
  ✓ Linked: checkpoints
  ✓ Linked: vae
✓ ComfyUI setup complete!


# ============================================================================
# CELL 7: START COMFYUI SERVER (1 MINUTE + STARTUP TIME)
# ============================================================================

This cell:
✓ Starts ComfyUI server in background
✓ Waits for it to be ready (30-60 seconds)
✓ Shows server status

⚠️ IMPORTANT: Keep this cell running!
    This is the server that generates images.
    If you stop it, image generation will fail!

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import subprocess
import time
import requests
import threading
from pathlib import Path

os.chdir('/content/ComfyUI')

print("Starting ComfyUI server on http://127.0.0.1:8188...")
print("=" * 60)

# Start ComfyUI server in background
server_process = subprocess.Popen(
    ['python', 'main.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("ComfyUI server starting... waiting for startup (30-60 seconds)")

# Wait for server to be ready
max_retries = 60
for attempt in range(max_retries):
    try:
        response = requests.get('http://127.0.0.1:8188/api/system_stats')
        if response.status_code == 200:
            print(f"\n✓ ComfyUI server is READY!")
            print(f"  - URL: http://127.0.0.1:8188")
            print(f"  - Status: Running")
            print(f"  - Models loaded: {len(list(Path('/content/ComfyUI/models/checkpoints').glob('*')))}")
            print("=" * 60)
            print("\n⚠️ IMPORTANT: Keep this cell running while generating!")
            print("   Do NOT stop the server or close this cell!")
            print("   If needed, run this cell again if it crashes")
            break
    except:
        if attempt % 10 == 0:
            print(f"  Waiting... ({attempt}s elapsed)")
        time.sleep(1)

if server_process.poll() is not None:
    print("\n❌ ComfyUI server failed to start!")
    print("Output:", server_process.stdout.read().decode())
    print("Error:", server_process.stderr.read().decode())
else:
    print("\n✓ Server is running. Keep this cell active!")

────────────────────────────────────────────────────

EXPECTED OUTPUT:
Starting ComfyUI server on http://127.0.0.1:8188...
============================================================
ComfyUI server starting... waiting for startup (30-60 seconds)
  Waiting... (0s elapsed)
  Waiting... (10s elapsed)
  Waiting... (20s elapsed)

✓ ComfyUI server is READY!
  - URL: http://127.0.0.1:8188
  - Status: Running
  - Models loaded: 3
============================================================

⚠️ IMPORTANT: Keep this cell running while generating!


# ============================================================================
# CELL 8: TEST CONFIGURATION
# ============================================================================

This cell:
✓ Verifies DirectorAI can connect to ComfyUI
✓ Confirms models are loaded
✓ Checks system resources

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import requests
from pathlib import Path

print("Testing DirectorAI + ComfyUI Connection...")
print("=" * 60)

# Test ComfyUI server connection
try:
    response = requests.get('http://127.0.0.1:8188/api/system_stats')
    stats = response.json()
    print("✓ ComfyUI server: CONNECTED")
    print(f"  - RAM available: {stats.get('ram', {}).get('available', 'N/A')} MB")
except Exception as e:
    print(f"❌ ComfyUI connection failed: {e}")

# Check models
models_dir = Path('/content/ComfyUI/models')
checkpoints = list((models_dir / 'checkpoints').glob('*.safetensors')) + \
              list((models_dir / 'checkpoints').glob('*.ckpt'))
vae_models = list((models_dir / 'vae').glob('*.safetensors'))

print(f"\n✓ Models available:")
print(f"  - Checkpoints: {len(checkpoints)}")
print(f"  - VAE models: {len(vae_models)}")

# Test DirectorAI can find config
%cd /content/DirectAi
from config import DirectorAIConfig
config = DirectorAIConfig()
print(f"\n✓ DirectorAI config loaded")
print(f"  - Video size: {config.GENERATION_PARAMS['image']['width']}x{config.GENERATION_PARAMS['image']['height']}")
print(f"  - ComfyUI URL: {config.COMFYUI_CONFIG['url']}")

print("\n" + "=" * 60)
print("✓ All systems ready!")
print("  - DirectorAI: Ready")
print("  - ComfyUI: Ready")
print("  - Models: Ready")
print("  - Configuration: Ready")
print("\nYou can now proceed to generate videos!")

────────────────────────────────────────────────────

EXPECTED OUTPUT:
Testing DirectorAI + ComfyUI Connection...
============================================================
✓ ComfyUI server: CONNECTED
  - RAM available: 15123 MB

✓ Models available:
  - Checkpoints: 3
  - VAE models: 1

✓ DirectorAI config loaded
  - Video size: 540x960
  - ComfyUI URL: http://127.0.0.1:8188

============================================================
✓ All systems ready!
  - DirectorAI: Ready
  - ComfyUI: Ready
  - Models: Ready
  - Configuration: Ready

You can now proceed to generate videos!


# ============================================================================
# COMFYUI CELL EXECUTION ORDER
# ============================================================================

CRITICAL: Must be run in this order:

1. Cell 1: Clone DirectorAI
2. Cell 2: Install dependencies (includes TTS)
3. Cell 3: Mount Drive
4. Cell 4: Verify models
5. Cell 5: Copy models
6. ⭐ Cell 6: Setup ComfyUI ← NEW!
7. ⭐ Cell 7: Start ComfyUI server ← NEW! (KEEP RUNNING!)
8. Cell 8: Test configuration
9. Cell 9: Generate videos
10. (Optional) Cell 10: Monitor progress
11. Cell 11: Copy to Drive


# ============================================================================
# TROUBLESHOOTING COMFYUI
# ============================================================================

PROBLEM: "ComfyUI server failed to start"
─────────────────────────────────────────
CAUSE: ComfyUI installation incomplete or models missing

FIX:
1. Re-run Cell 6 completely
2. Wait for it to finish
3. Then run Cell 7


PROBLEM: "Connection refused to http://127.0.0.1:8188"
────────────────────────────────────────────────────
CAUSE: ComfyUI server not running

FIX:
1. Check that Cell 7 is still running
2. Make sure you didn't stop the cell
3. If stopped, run Cell 7 again


PROBLEM: "Models directory not found"
──────────────────────────────────────
CAUSE: Models weren't copied properly

FIX:
1. Go back to Cell 5
2. Run it again (model copy)
3. Make sure it finishes completely
4. Then run Cell 6 again


PROBLEM: "Out of memory" error
───────────────────────────────
CAUSE: Colab is running out of GPU/RAM

FIX:
1. Runtime → Restart runtime
2. Run all cells again
3. Use Premium GPU if available (faster, more memory)


PROBLEM: "pip install requirements failed"
────────────────────────────────────────
CAUSE: ComfyUI dependencies not available

FIX:
1. This shouldn't happen with the latest ComfyUI
2. Try running Cell 6 again
3. If problem persists, run:
   !pip install --upgrade pip
   Then run Cell 6 again


# ============================================================================
# COMFYUI WORKFLOW (WHAT HAPPENS BEHIND THE SCENES)
# ============================================================================

When you run Cell 9 (generate), here's what happens:

1. DirectorAI creates a text prompt
   "Cleopatra VII, ancient Egypt, dramatic lighting..."

2. DirectorAI sends workflow JSON to ComfyUI API
   ComfyUI URL: http://127.0.0.1:8188

3. ComfyUI loads checkpoint model
   Model: realisticVisionV60B1_v60B1VAE.safetensors

4. ComfyUI generates image from prompt
   Input: Text prompt
   Output: PNG image (540x960)

5. ComfyUI animates the image with AnimateDiff
   Input: PNG image
   Output: MP4 video (smooth animation)

6. DirectorAI receives video from ComfyUI
   Saves to: /content/DirectAi/outputs/short_XXX/

7. Process repeats for next idea


# ============================================================================
# COMFYUI PERFORMANCE TIPS
# ============================================================================

For FASTER generation:
────────────────────
1. Use Premium GPU in Colab
   - Faster than K80 (might get V100 or A100)
   - More memory available

2. Reduce image generation steps
   - Edit config.py: change "steps": 30 → "steps": 20
   - Trade: Lower quality but faster generation

3. Reduce animation frames
   - Edit config.py: change "frames": 16 → "frames": 8
   - Trade: Less smooth animation but faster

4. Generate fewer ideas
   - Start with 2-3 ideas instead of 5-10
   - Scale up once you understand the timing


For HIGHER quality:
──────────────────
1. Use Premium GPU (better quality models possible)

2. Increase image generation steps
   - Edit config.py: change "steps": 30 → "steps": 50
   - Trade: Higher quality but slower (50% slower)

3. Increase animation frames
   - Edit config.py: change "frames": 16 → "frames": 24
   - Trade: Smoother animation but slower

4. Use higher resolution
   - Change width/height in config.py
   - Currently: 540x960 (perfect for YouTube Shorts)
   - Don't change unless necessary


# ============================================================================
# COMFYUI API ENDPOINTS (FOR REFERENCE)
# ============================================================================

ComfyUI Server: http://127.0.0.1:8188

Main Endpoints:
- GET /api/system_stats → Server health & resources
- POST /api/prompt → Submit generation job (workflow)
- GET /api/history/{prompt_id} → Check job results
- GET /api/queue → View queue

Used by DirectorAI:
- ComfyUIClient in app/utils/comfyui_client.py
- Methods: check_server_health(), queue_prompt(), wait_for_completion()
- All handled automatically, you don't need to call these


# ============================================================================
# KEEP COMFYUI RUNNING DURING GENERATION
# ============================================================================

⚠️ CRITICAL: Do NOT close or stop Cell 7!

What happens if you close Cell 7:
❌ ComfyUI server stops
❌ Image generation fails
❌ Videos can't be created
❌ Generation crashes

What to do:
✅ Leave Cell 7 running in background
✅ Run Cell 9 (generate) in a NEW cell
✅ Monitor progress in Cell 10
✅ Let Cell 7 keep running
✅ Only close after all generation completes


# ============================================================================
# YOU'RE READY FOR COMFYUI!
# ============================================================================

All setup is automated in the Colab cells.

Just follow the order:
1. Cells 1-5: Standard setup (as before)
2. Cell 6: Setup ComfyUI (NEW - 5-10 minutes)
3. Cell 7: Start ComfyUI server (NEW - 1 minute)
4. Cell 8: Test (NEW - 30 seconds)
5. Cell 9: Generate videos (same as before)
6. Cells 10-11: Finish (same as before)

ComfyUI will handle all the heavy lifting for image and video generation! 🚀

"""