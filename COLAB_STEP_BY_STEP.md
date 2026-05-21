"""
DIRECTORAI COLAB - COMPLETE STEP-BY-STEP GUIDE
Copy and paste each cell into Google Colab in order
"""

# ============================================================================
# BEFORE YOU START (IMPORTANT!)
# ============================================================================

PREREQUISITE 1: Upload Models to Google Drive
1. Create folder: My Drive → DirectorAI_Models
2. Inside, create two folders:
   - checkpoints/
   - vae/
3. Upload your model files:
   ├── checkpoints/
   │   ├── realisticVisionV60B1_v60B1VAE.safetensors
   │   ├── v1-5-pruned-emaonly.safetensors
   │   └── mm_sd_v15_v2.ckpt
   └── vae/
       └── vae-ft-mse-840000-ema-pruned.safetensors
4. Wait for uploads to complete (can take 30-60 minutes for large files)

PREREQUISITE 2: Push Code to GitHub
1. Create repo: github.com/YOUR_USERNAME/DirectorAI
2. Clone DirectorAI locally
3. Push to GitHub (git add . && git commit -m "Initial" && git push)

Now you're ready for Colab!


# ============================================================================
# COPY-PASTE THESE CELLS INTO GOOGLE COLAB IN ORDER
# ============================================================================

=== COLAB CELL 1: Clone Repository ===

!git clone https://github.com/YOUR_USERNAME/DirectorAI.git
%cd DirectorAI
!ls -la


=== COLAB CELL 2: Install Dependencies ===

!pip install -r requirements.txt -q
!pip install google-auth-oauthlib -q
print("✓ All dependencies installed")


=== COLAB CELL 3: Mount Google Drive ===

from google.colab import drive
drive.mount('/content/drive')

# Verify mount
import os
print("\nDrive contents:")
os.system('ls -lah "/content/drive/MyDrive/"')


=== COLAB CELL 4: Verify Models on Drive ===

from pathlib import Path

drive_models = Path('/content/drive/MyDrive/DirectorAI_Models')

print("Checking models on Drive...\n")

required_models = {
    'checkpoints/realisticVisionV60B1_v60B1VAE.safetensors': 'Primary checkpoint',
    'checkpoints/v1-5-pruned-emaonly.safetensors': 'Secondary checkpoint',
    'checkpoints/mm_sd_v15_v2.ckpt': 'AnimateDiff model',
    'vae/vae-ft-mse-840000-ema-pruned.safetensors': 'VAE model'
}

all_found = True
for model_path, description in required_models.items():
    full_path = drive_models / model_path
    if full_path.exists():
        size_gb = full_path.stat().st_size / (1024**3)
        print(f"✓ {description}: {size_gb:.2f} GB")
    else:
        print(f"✗ {description} NOT FOUND")
        print(f"  Expected at: {full_path}")
        all_found = False

if all_found:
    print("\n✓ All models found on Drive!")
else:
    print("\n✗ Some models missing. Upload them first.")


=== COLAB CELL 5: Copy Models from Drive to Colab ===

import shutil
from pathlib import Path

print("Copying models from Drive to Colab (this may take 5-15 minutes)...\n")

drive_models = Path('/content/drive/MyDrive/DirectorAI_Models')
local_models = Path('/content/DirectorAI/models')

# Create directories
(local_models / 'checkpoints').mkdir(parents=True, exist_ok=True)
(local_models / 'vae').mkdir(parents=True, exist_ok=True)

# Copy checkpoint models
checkpoint_files = [
    'realisticVisionV60B1_v60B1VAE.safetensors',
    'v1-5-pruned-emaonly.safetensors',
    'mm_sd_v15_v2.ckpt'
]

for model_file in checkpoint_files:
    src = drive_models / 'checkpoints' / model_file
    dst = local_models / 'checkpoints' / model_file
    
    if src.exists():
        size_gb = src.stat().st_size / (1024**3)
        print(f"Copying {model_file} ({size_gb:.2f} GB)...")
        shutil.copy2(src, dst)
        print(f"✓ Done\n")
    else:
        print(f"⚠ {model_file} not found on Drive\n")

# Copy VAE
vae_src = drive_models / 'vae' / 'vae-ft-mse-840000-ema-pruned.safetensors'
vae_dst = local_models / 'vae' / 'vae-ft-mse-840000-ema-pruned.safetensors'

if vae_src.exists():
    size_gb = vae_src.stat().st_size / (1024**3)
    print(f"Copying VAE model ({size_gb:.2f} GB)...")
    shutil.copy2(vae_src, vae_dst)
    print(f"✓ Done\n")

print("✓ All models copied to Colab!")


=== COLAB CELL 6: Test Architecture ===

%cd /content/DirectorAI
!python test_architecture.py

print("\n✓ Architecture test complete - all modules loaded successfully!")


=== COLAB CELL 7: Create Your Prompts File ===

# MODIFY THIS WITH YOUR OWN IDEAS!
# Each idea should be a detailed historical description (2-3 sentences)

prompts = {
    "ideas": [
        "Cleopatra VII, the last pharaoh of ancient Egypt, ruling with intelligence and diplomatic skill during the tumultuous period when Rome threatened to consume her kingdom",
        "The eruption of Mount Vesuvius in 79 AD, a catastrophic volcanic event that buried the Roman cities of Pompeii and Herculaneum, preserving their citizens in volcanic ash",
        "Joan of Arc, a peasant girl in medieval France, leading armies during the Hundred Years' War, driven by her unwavering faith in divine destiny to save her nation",
        "The Battle of Thermopylae in 480 BC, where 300 elite Spartan warriors made their legendary last stand against a massive Persian army",
        "Hannibal Barca, the brilliant Carthaginian general, leading war elephants across the Alps to attack Rome during the Second Punic War"
    ]
}

import json

with open('/content/DirectorAI/prompts.json', 'w') as f:
    json.dump(prompts, f, indent=2)

print("✓ Prompts file created with", len(prompts['ideas']), "ideas")
print("\nYour ideas:")
for i, idea in enumerate(prompts['ideas'], 1):
    print(f"{i}. {idea[:70]}...")


=== COLAB CELL 8: Generate Single Test Short ===

# Test with just one idea first
test_idea = "The rise of Cleopatra VII, the last pharaoh of ancient Egypt"

print(f"Generating test short: {test_idea}\n")
!python main.py --mode single --idea "{test_idea}"

print("\n✓ Single short generation complete")


=== COLAB CELL 9: Check Test Output ===

import os
from pathlib import Path

output_dir = Path('/content/DirectorAI/outputs/short_001')

print("Checking output structure...\n")

if output_dir.exists():
    print(f"✓ Output directory created: {output_dir}\n")
    
    for subdir in ['script', 'audio', 'scenes', 'renders', 'metadata', 'final']:
        path = output_dir / subdir
        if path.exists():
            files = list(path.glob('*'))
            print(f"✓ {subdir}/ - {len(files)} files")
        else:
            print(f"○ {subdir}/ - (empty)")
else:
    print("✗ Output directory not created yet")


=== COLAB CELL 10: Generate Batch (YOUR IDEAS) ===

# Now generate with your own ideas from prompts.json
print("Starting batch generation with your ideas...\n")
!python main.py --mode batch --ideas-file prompts.json


=== COLAB CELL 11: Monitor Progress ===

# Run this while batch is generating to check progress
import json
from pathlib import Path

queue_file = Path('/content/DirectorAI/queue.json')

if queue_file.exists():
    with open(queue_file, 'r') as f:
        queue_data = json.load(f)
    
    jobs = queue_data['jobs']
    
    print(f"Total jobs: {len(jobs)}\n")
    
    status_counts = {}
    for job in jobs:
        status = job['status']
        status_counts[status] = status_counts.get(status, 0) + 1
        print(f"Job {job['job_id']:2d}: {status:12s} - {job['idea'][:50]}...")
    
    print(f"\nSummary:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
else:
    print("Queue not created yet - generation may not have started")


=== COLAB CELL 12: Copy Results to Google Drive ===

import shutil
from pathlib import Path

source = Path('/content/DirectorAI/outputs')
destination = Path('/content/drive/MyDrive/DirectorAI_Results')

print("Copying results to Google Drive...\n")

if source.exists():
    shutil.copytree(source, destination, dirs_exist_ok=True)
    print(f"✓ Results copied to: {destination}")
    
    # Verify copy
    result_shorts = list(destination.glob('short_*'))
    print(f"✓ Found {len(result_shorts)} shorts in Drive")
else:
    print("✗ No outputs to copy")


=== COLAB CELL 13: List Results ===

import os
from pathlib import Path

results_dir = Path('/content/drive/MyDrive/DirectorAI_Results')

print("Results on Google Drive:\n")
os.system(f'ls -lah "{results_dir}"')

print("\n\nShorts generated:")
for short_dir in sorted(results_dir.glob('short_*')):
    print(f"\n{short_dir.name}:")
    os.system(f'ls -lah "{short_dir}"')


=== COLAB CELL 14: Download Final MP4s (Optional) ===

# Use this to download final shorts to your computer
from pathlib import Path
import shutil

results_dir = Path('/content/DirectorAI/outputs')
final_shorts = list(results_dir.glob('*/final/*.mp4'))

print(f"Found {len(final_shorts)} final shorts:\n")

for short in final_shorts:
    print(f"✓ {short.parent.parent.name}/final/{short.name}")
    # Right-click on files in left panel to download

print("\nGo to Files panel (left sidebar) → outputs → short_XXX → final → .mp4 files")
print("Right-click to download")


=== COLAB CELL 15: Check Resource Usage ===

import psutil
import subprocess

# CPU
cpu_percent = psutil.cpu_percent()
print(f"CPU Usage: {cpu_percent}%")

# RAM
ram = psutil.virtual_memory()
print(f"RAM Usage: {ram.percent}% ({ram.used / (1024**3):.1f}GB / {ram.total / (1024**3):.1f}GB)")

# GPU
try:
    gpu_output = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,nounits,noheader'], 
                               capture_output=True, text=True, timeout=5)
    if gpu_output.returncode == 0:
        used, total = gpu_output.stdout.strip().split()
        print(f"GPU Memory: {int(used)/1024:.1f}GB / {int(total)/1024:.1f}GB")
except:
    print("GPU info not available")

# Storage
storage = subprocess.run(['df', '-BG', '/content/'], capture_output=True, text=True)
print(f"\nStorage:\n{storage.stdout}")


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

ISSUE: "ModuleNotFoundError: No module named 'config'"
FIX: Make sure you're in the DirectorAI directory
  %cd /content/DirectorAI

ISSUE: "Models not found in /content/DirectorAI/models"
FIX: Check models were copied from Drive
  !ls -lah /content/DirectorAI/models/checkpoints/

ISSUE: "Not enough GPU memory"
FIX: Reduce batch size or image resolution
  - Edit config.py
  - Change IMAGE_STEPS from 30 to 20
  - Change IMAGE_WIDTH from 768 to 512

ISSUE: "Drive mount permission denied"
FIX: Grant Colab permission to access Drive
  - Run mount cell again
  - Click "Connect to Google Drive" when prompted

ISSUE: "Colab session timed out"
FIX: Colab sessions last max 12 hours
  - Your files stay on Drive
  - Restart runtime and re-run from where you left off
  - Check queue.json to see what was completed


# ============================================================================
# TIPS FOR BEST RESULTS
# ============================================================================

1. PROMPT QUALITY
   ✓ Be specific about time period, people, and events
   ✓ Include emotional context (rise, fall, victory, tragedy)
   ✓ 2-3 sentences per idea
   
   Good: "Joan of Arc, a peasant girl, leading French armies during the Hundred Years' War"
   Bad: "Medieval stuff"

2. BATCH SIZE
   ✓ Start with 3-5 ideas for testing
   ✓ Increase to 10 once working
   ✓ Then up to 20+ for production

3. MONITORING
   ✓ Run Cell 11 while generation happens
   ✓ Check queue.json regularly
   ✓ Copy results to Drive periodically

4. GPU OPTIMIZATION
   ✓ Close other Colab tabs
   ✓ Use Premium GPU if available (faster generation)
   ✓ Monitor Cell 15 to check resources

5. COLAB TIME LIMITS
   ✓ Colab gives 12 hours per session
   ✓ One short takes ~5-15 minutes (depending on optimization)
   ✓ 20 shorts = 100-300 minutes = 2-5 hours


# ============================================================================
# WORKFLOW SUMMARY
# ============================================================================

1. ✓ Models uploaded to Drive (ONE TIME - 30-60 min)
2. ✓ Repository pushed to GitHub (ONE TIME - 5 min)
3. ✓ Open Google Colab (new notebook)
4. ✓ Run CELLS 1-7 for setup (15-20 minutes)
5. ✓ Run CELL 8 to test single short (5 minutes)
6. ✓ Run CELL 10 to generate batch (10-300+ minutes depending on size)
7. ✓ Run CELL 12 to copy results to Drive
8. ✓ Download from Drive or leave on Drive

TOTAL FIRST RUN: 1-2 hours setup + 10-300 minutes generation


# ============================================================================
# NEXT STEPS AFTER FIRST RUN
# ============================================================================

1. Create more prompts
2. Experiment with prompt styles
3. Adjust generation parameters in config.py
4. Integrate LLM for better scripts
5. Load XTTS for real narration
6. Setup ComfyUI integration
7. Scale to 50+ ideas


# ============================================================================
# READY? START WITH CELL 1!
# ============================================================================

Good luck generating your historical shorts! 🎬📹
