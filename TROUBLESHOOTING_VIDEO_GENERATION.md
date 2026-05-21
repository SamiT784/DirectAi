# VIDEO GENERATION TROUBLESHOOTING

When videos show as "completed" but no actual video files are created, follow these steps:

## Step 1: Run the Debug Script

In a Colab cell, run:
```python
!python debug_generation.py
```

This will check:
- ✓ ComfyUI server is running
- ✓ Models are accessible  
- ✓ Output directories exist
- ✓ Simple workflows execute

## Common Issues & Solutions

### ❌ Issue 1: "ComfyUI server is NOT responding"

**Cause**: ComfyUI server is not running or crashed

**Solutions**:
1. Check that you completed **Cell 7** in EXECUTION_STEPS.md
2. The ComfyUI cell must stay **running during all generation**
3. If server crashed, restart it:
   ```python
   %cd /content/ComfyUI
   !python main.py --listen 127.0.0.1
   ```
4. Wait 30-60 seconds for "READY" message
5. Look for GPU memory errors - may need to restart Colab runtime

---

### ❌ Issue 2: "No models found" or "Missing checkpoint"

**Cause**: Models not copied to Colab or wrong path

**Solutions**:
1. Verify models are on Google Drive: My Drive → AI → models
2. Run **Cell 5** to copy models to Colab (takes 5-10 minutes)
3. After Cell 5, verify models exist:
   ```python
   !ls -lh /content/ComfyUI/models/checkpoints/
   !ls -lh /content/ComfyUI/models/animatediff/
   !ls -lh /content/ComfyUI/models/vae/
   ```
   Should show 4 files (2 checkpoints, 1 animatediff, 1 vae)

---

### ❌ Issue 3: "Workflow did not complete" or no output generated

**Cause**: ComfyUI workflow failed silently, or model out of memory

**Solutions**:

1. **Check ComfyUI terminal output** (Cell 7):
   - Look for red error messages
   - GPU out of memory error?
   - Model loading errors?

2. **Reduce image dimensions** in config.py:
   ```python
   # In DirectorAIConfig
   "image": {"width": 384, "height": 640}  # Smaller than default 540x960
   ```

3. **Reduce quality/steps** in config.py:
   ```python
   "steps": 15  # Instead of default 30
   ```

4. **Restart Colab** (Cell 1):
   - Runtime → Restart runtime
   - This frees GPU memory
   - Rerun Cell 3 (mount), Cell 5 (copy models), Cell 7 (ComfyUI)

---

### ❌ Issue 4: Jobs show "completed" but no output_path

**Cause**: Scene generation failed but marked completed anyway

**Solutions**:
1. Check queue.json for error messages:
   ```python
   import json
   with open('queue.json') as f:
       data = json.load(f)
   for job in data['jobs']:
       if job['error']:
           print(f"Job {job['job_id']}: {job['error']}")
   ```

2. Check DirectorAI logs directory:
   ```python
   !ls -lh logs/
   !tail -100 logs/DirectorAIOrchestrator.log
   ```

---

### ❌ Issue 5: "FFmpeg not found" when rendering final video

**Cause**: FFmpeg not installed or not in PATH

**Solutions**:
1. Check if FFmpeg installed:
   ```python
   !which ffmpeg
   !ffmpeg -version
   ```

2. If missing, install it:
   ```python
   !apt-get update && apt-get install -y ffmpeg
   ```

3. Verify after install:
   ```python
   !ffmpeg -version
   ```

---

## Step 2: Manual Testing

Test individual engines:

```python
# Test scene generation only
from app.scene_engine import SceneEngine

scene_engine = SceneEngine()
result = scene_engine.process({
    "prompt": "a beautiful sunset over mountains, cinematic, 8k",
    "negative_prompt": "low quality, blurry",
    "output_path": "/content/test_scene",
    "scene_num": 0
})
print(result)

# Check if image was created
!ls -lh /content/test_scene/
```

If this works, you have:
- ✓ ComfyUI running
- ✓ Models loaded
- ✓ Image generation working

Then test rendering:
```python
# If you have a test video, try rendering
from app.render_engine import RenderEngine

render_engine = RenderEngine()
result = render_engine.process({
    "scene_videos": ["/content/test_scene/scene_animation.mp4"],
    "output_path": "/content/test_output"
})
print(result)
!ls -lh /content/test_output/
```

---

## Step 3: Batch Generation with Logging

Run generation with verbose logging:

```python
# Generate with detailed logging
from config import DirectorAIConfig
from app.orchestrator import DirectorAIOrchestrator

config = DirectorAIConfig()
orchestrator = DirectorAIOrchestrator(config)

# Single idea first
result = orchestrator.generate_single_short(
    idea="Generate a short about ancient Egypt",
    short_id=0
)

print("Result:", result)

# Check output directory
import os
for root, dirs, files in os.walk("/content/DirectorAI_outputs/short_0"):
    level = root.replace("/content/DirectorAI_outputs/short_0", "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        size = os.path.getsize(os.path.join(root, file)) / (1024*1024)
        print(f"{subindent}{file} ({size:.1f}MB)")
```

---

## Step 4: Check Colab Resources

If workflows timeout or hang:

```python
# Check GPU
!nvidia-smi

# Check memory
!free -h

# Check disk space
!df -h
```

If GPU is at 100% or low free memory:
- Reduce batch size
- Reduce image resolution
- Increase steps delays (add sleep between generations)

---

## Still Stuck?

Check these files for detailed error logs:
- `logs/DirectorAIOrchestrator.log` - main orchestration logs
- `logs/SceneEngine.log` - image generation logs  
- `queue.json` - job queue with error details
- ComfyUI terminal output - workflow execution errors

Common patterns in errors:
- "CUDA out of memory" → Restart runtime, reduce resolution
- "Model not found" → Run Cell 5 again
- "No history found" → ComfyUI workflow crashed, check terminal
- "Connection refused" → ComfyUI crashed, restart Cell 7
