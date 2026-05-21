"""
GOOGLE COLAB SETUP GUIDE FOR DIRECTORAI
Complete step-by-step instructions
"""

# ============================================================================
# OVERVIEW
# ============================================================================

This guide walks you through:
1. Preparing models on Google Drive
2. Cloning DirectorAI to Colab
3. Installing dependencies
4. Mounting Drive and models
5. Creating your prompts file
6. Running batch generation
7. Downloading results


# ============================================================================
# STEP 1: PREPARE MODELS ON GOOGLE DRIVE (DO THIS FIRST)
# ============================================================================

BEFORE YOU GO TO COLAB:

1. Create this folder structure on Google Drive:
   
   My Drive/DirectorAI_Models/
   ├── checkpoints/
   │   ├── realisticVisionV60B1_v60B1VAE.safetensors
   │   ├── v1-5-pruned-emaonly.safetensors
   │   └── mm_sd_v15_v2.ckpt
   │
   └── vae/
       └── vae-ft-mse-840000-ema-pruned.safetensors

2. Upload all your model files to these folders

3. Note the exact paths (you'll need them in Colab)

IMPORTANT: Model files are large (2-7GB each)
- This step may take 30-60 minutes
- Use a stable internet connection


# ============================================================================
# STEP 2: PREPARE YOUR GITHUB REPOSITORY (DO THIS SECOND)
# ============================================================================

On your GitHub:

1. Create a new repository called "DirectorAI"

2. Initialize and push the DirectorAI files:
   
   cd DirectorAI
   git init
   git add .
   git commit -m "Initial DirectorAI setup"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/DirectorAI.git
   git push -u origin main

3. Copy your repository URL (you'll use this in Colab)


# ============================================================================
# STEP 3: GOOGLE COLAB - COMPLETE WALKTHROUGH
# ============================================================================

NOW OPEN GOOGLE COLAB: https://colab.research.google.com/

=== CELL 1: Clone Repository ===

!git clone https://github.com/YOUR_USERNAME/DirectorAI.git
%cd DirectorAI


=== CELL 2: Install Dependencies ===

!pip install -r requirements.txt -q


=== CELL 3: Mount Google Drive ===

from google.colab import drive
drive.mount('/content/drive')

# Verify mount
!ls "/content/drive/MyDrive/"


=== CELL 4: Copy Models from Drive to Colab ===

# This copies models to Colab's fast storage
import shutil
from pathlib import Path

# Create model directory in Colab
model_dir = Path('/content/DirectorAI/models/checkpoints')
model_dir.mkdir(parents=True, exist_ok=True)

# Copy from Drive
drive_models = Path('/content/drive/MyDrive/DirectorAI_Models')

# Copy checkpoint models
for model_file in ['realisticVisionV60B1_v60B1VAE.safetensors', 'v1-5-pruned-emaonly.safetensors', 'mm_sd_v15_v2.ckpt']:
    src = drive_models / 'checkpoints' / model_file
    dst = model_dir / model_file
    if src.exists():
        print(f"Copying {model_file}...")
        shutil.copy2(src, dst)
        print(f"✓ {model_file} copied")
    else:
        print(f"⚠ {model_file} not found at {src}")

# Copy VAE
vae_src = drive_models / 'vae' / 'vae-ft-mse-840000-ema-pruned.safetensors'
vae_dst = Path('/content/DirectorAI/models/vae') / 'vae-ft-mse-840000-ema-pruned.safetensors'
vae_dst.parent.mkdir(parents=True, exist_ok=True)
if vae_src.exists():
    print(f"Copying VAE model...")
    shutil.copy2(vae_src, vae_dst)
    print(f"✓ VAE model copied")


=== CELL 5: Create Your Prompts File ===

# Create the prompts file with your historical ideas
prompts_content = '''
{
  "ideas": [
    "The rise of Cleopatra VII, the last pharaoh of ancient Egypt ruling with intelligence and charm",
    "The eruption of Mount Vesuvius in 79 AD, a catastrophe that froze Pompeii in time",
    "Joan of Arc leading French armies during the Hundred Years' War with divine faith",
    "The Battle of Thermopylae where 300 Spartans held off a Persian army",
    "Hannibal's daring march across the Alps with war elephants to attack Rome"
  ]
}
'''

# Save to file
with open('/content/DirectorAI/prompts.json', 'w') as f:
    f.write(prompts_content)

print("✓ Prompts file created at /content/DirectorAI/prompts.json")


=== CELL 6: Test System ===

%cd /content/DirectorAI
!python test_architecture.py


=== CELL 7: Generate Single Test Short ===

!python main.py --mode single --idea "The rise of Cleopatra VII, the last pharaoh of ancient Egypt"


=== CELL 8: Generate Batch ===

!python main.py --mode batch --ideas-file prompts.json


=== CELL 9: Check Results ===

import os
import subprocess

# List all generated shorts
result = subprocess.run(['ls', '-lah', '/content/DirectorAI/outputs/'], 
                       capture_output=True, text=True)
print(result.stdout)

# Check a specific short
result = subprocess.run(['ls', '-lah', '/content/DirectorAI/outputs/short_001/'], 
                       capture_output=True, text=True)
print(result.stdout)


=== CELL 10: Copy Results to Drive ===

import shutil

source = '/content/DirectorAI/outputs'
destination = '/content/drive/MyDrive/DirectorAI_Results'

print("Copying results to Google Drive...")
shutil.copytree(source, destination, dirs_exist_ok=True)
print("✓ Results copied to Drive")

# Verify
!ls -lah "/content/drive/MyDrive/DirectorAI_Results/"


# ============================================================================
# STEP 4: CREATING YOUR PROMPTS/IDEAS FILE
# ============================================================================

Your prompts file should be JSON format with this structure:

{
  "ideas": [
    "Detailed historical idea 1",
    "Detailed historical idea 2",
    "Detailed historical idea 3"
  ]
}

TIPS FOR GOOD PROMPTS:

✓ Be specific about:
  - Who: "Cleopatra VII", "300 Spartans", "Joan of Arc"
  - What: "the rise", "a betrayal", "a great battle"
  - When: "79 AD", "ancient Egypt", "Hundred Years' War"
  - Why: "to rule", "to defend", "to inspire"

✓ Example good prompts:
  - "Cleopatra VII navigating political intrigue in ancient Egypt, using diplomacy and charm to maintain power"
  - "The eruption of Mount Vesuvius in 79 AD as it destroys Pompeii, capturing the final moments of Roman citizens"
  - "Joan of Arc leading French forces during the Hundred Years' War, driven by her unwavering faith in divine destiny"

✗ Avoid vague prompts:
  - "Ancient history"
  - "A war"
  - "Something about emperors"

MAXIMUM IDEAS: Start with 3-5 for first test, then increase


# ============================================================================
# STEP 5: MONITORING PROGRESS
# ============================================================================

While generation is running, you can check progress:

=== In Colab Cell ===

import json
from pathlib import Path

# Check queue status
queue_file = Path('/content/DirectorAI/queue.json')
if queue_file.exists():
    with open(queue_file, 'r') as f:
        queue_data = json.load(f)
    
    jobs = queue_data.get('jobs', [])
    print(f"Total jobs: {len(jobs)}")
    
    for job in jobs:
        print(f"  Job {job['job_id']}: {job['status']} - {job['idea'][:50]}")


# ============================================================================
# STEP 6: COMMON ISSUES & SOLUTIONS
# ============================================================================

ISSUE: "ModuleNotFoundError: No module named 'config'"
SOLUTION: Make sure you're in the DirectorAI directory
  %cd /content/DirectorAI

ISSUE: "Models not found"
SOLUTION: Check they were copied correctly
  !ls -lah /content/DirectorAI/models/checkpoints/

ISSUE: "Out of memory"
SOLUTION: Reduce batch size or image resolution in config.py
  - Reduce IMAGE_STEPS from 30 to 20
  - Reduce IMAGE_WIDTH from 768 to 512

ISSUE: "ComfyUI server not responding"
SOLUTION: This is expected - ComfyUI integration is for phase 2
  - The system will create placeholder outputs for now

ISSUE: "Permission denied"
SOLUTION: Grant Colab access to Drive
  - When prompted, click "Connect to Google Drive"


# ============================================================================
# STEP 7: COLAB BEST PRACTICES
# ============================================================================

1. SAVE YOUR NOTEBOOKS
   - File → Save (Ctrl+S)
   - Colab saves automatically every few minutes

2. RUNTIME LIMITS
   - Colab sessions timeout after 12 hours of inactivity
   - Your files stay on Drive, so you can resume

3. BATCH GENERATION STRATEGY
   - Start with 3-5 ideas for testing
   - Once working, increase to 10-20
   - For 20+ ideas, split into multiple batches

4. GPU USAGE
   - You get 12.7GB GPU memory (K80/T4)
   - Monitor usage in Colab
   - If running out: restart runtime

5. STORAGE
   - Colab gives 100GB free storage
   - DirectorAI outputs can be 50-200MB per short
   - Copy completed results to Drive regularly

6. COST
   - Completely free with Colab
   - Just respect the usage limits


# ============================================================================
# STEP 8: FULL WORKFLOW SUMMARY
# ============================================================================

1. ✓ Upload models to Drive (30-60 min, one time)
2. ✓ Push code to GitHub (5 minutes, one time)
3. ✓ Open Google Colab (free, need Google account)
4. ✓ Clone repository in Colab (2 minutes)
5. ✓ Install dependencies (3-5 minutes)
6. ✓ Mount Google Drive (1 minute)
7. ✓ Copy models from Drive (5-10 minutes)
8. ✓ Create prompts.json file (2 minutes)
9. ✓ Test architecture (2 minutes)
10. ✓ Generate batch (varies by number of ideas)
11. ✓ Copy results back to Drive (2-5 minutes)
12. ✓ Download from Drive to local computer


# ============================================================================
# NEXT STEPS AFTER INITIAL SETUP
# ============================================================================

Once you have the basic workflow running:

1. Integrate LLM for better script generation
   - Update ScriptEngine
   - Add your API keys (OpenAI/Claude/Groq)

2. Load XTTS model for narration
   - Update NarrationEngine

3. Setup ComfyUI connection
   - Can run in Colab or connect to local instance
   - Update ComfyUIClient

4. Fine-tune prompts
   - Experiment with different historical ideas
   - See what generates best results

5. Optimize batch processing
   - Adjust resolution/steps in config.py
   - Find sweet spot between quality and speed


# ============================================================================
# READY TO START?
# ============================================================================

Follow the STEP 3 cells in Google Colab in order.

Any questions? Check the logs in each cell for details.

Good luck with your historical shorts! 🎬
