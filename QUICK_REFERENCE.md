"""
DIRECTORAI QUICK START REFERENCE
Print this or keep it open while setting up Colab
"""

# ============================================================================
# BEFORE COLAB (DO THIS FIRST - 1 HOUR)
# ============================================================================

STEP 1: Upload Models to Google Drive
□ Create: My Drive/DirectorAI_Models/checkpoints/
□ Create: My Drive/DirectorAI_Models/vae/
□ Upload models (files are 2-7GB each):
  ├─ realisticVisionV60B1_v60B1VAE.safetensors (3GB)
  ├─ v1-5-pruned-emaonly.safetensors (4GB)
  ├─ mm_sd_v15_v2.ckpt (2GB)
  └─ vae-ft-mse-840000-ema-pruned.safetensors (360MB)

STEP 2: Push to GitHub
□ Create GitHub repo: DirectorAI
□ Clone locally
□ Push DirectorAI files
□ Copy repo URL


# ============================================================================
# IN GOOGLE COLAB (DO IN ORDER)
# ============================================================================

CELL 1: Clone Repository
!git clone https://github.com/YOUR_USERNAME/DirectorAI.git
%cd DirectorAI

CELL 2: Install Dependencies
!pip install -r requirements.txt -q
!pip install google-auth-oauthlib -q

CELL 3: Mount Drive
from google.colab import drive
drive.mount('/content/drive')

CELL 4: Verify Models
# Check models exist on Drive
drive_models = Path('/content/drive/MyDrive/DirectorAI_Models')
# See COLAB_STEP_BY_STEP.md for full code

CELL 5: Copy Models
# Copy models from Drive to Colab
# See COLAB_STEP_BY_STEP.md for full code

CELL 6: Test
%cd /content/DirectorAI
!python test_architecture.py

CELL 7: Create Prompts
# Create prompts.json with your ideas
# See PROMPTS_GUIDE.md for examples

CELL 8: Single Test
!python main.py --mode single --idea "Your idea here"

CELL 9: Batch Generation
!python main.py --mode batch --ideas-file prompts.json

CELL 10: Copy Results to Drive
# Copies outputs to Google Drive
# See COLAB_STEP_BY_STEP.md for full code


# ============================================================================
# PROMPT FORMAT (IN PROMPTS.JSON)
# ============================================================================

{
  "ideas": [
    "Cleopatra VII ruling ancient Egypt against Rome",
    "The eruption of Mount Vesuvius in 79 AD",
    "Joan of Arc leading French armies"
  ]
}


# ============================================================================
# YOUR IDEAS CHECKLIST
# ============================================================================

Each idea should have:
□ Specific person or group
□ Specific event (rise, fall, battle, etc.)
□ Time period
□ Emotional context
□ 100-300 characters total
□ 1-3 sentences max

Good example:
"Cleopatra VII, the last pharaoh of ancient Egypt, navigating complex political 
intrigue and diplomacy to maintain her kingdom's independence against Rome"

Bad example:
"Ancient stuff"


# ============================================================================
# FILES YOU NEED
# ============================================================================

□ GitHub repo URL (for cloning)
□ Models uploaded to Drive (in DirectorAI_Models/)
□ prompts.json file (your ideas)


# ============================================================================
# TYPICAL GENERATION TIME
# ============================================================================

Setup (first time):       15-20 minutes
Single short:            5-15 minutes
Batch of 5:              25-75 minutes
Batch of 10:             50-150 minutes
Batch of 20:             100-300 minutes


# ============================================================================
# COLAB RESOURCE LIMITS
# ============================================================================

GPU Memory:        12.7 GB (K80/T4)
RAM:               ~13-25 GB
Storage:           ~100 GB
Session timeout:   12 hours of inactivity
Session duration:  max 24 hours


# ============================================================================
# OUTPUT STRUCTURE
# ============================================================================

outputs/
└── short_001/
    ├── script/         (narrative)
    ├── audio/          (narration.wav)
    ├── scenes/         (images)
    ├── renders/        (videos)
    ├── metadata/       (metadata.json)
    └── final/          (final_short.mp4)


# ============================================================================
# USEFUL COLAB CELLS TO RUN ANYTIME
# ============================================================================

CHECK PROGRESS:
import json
from pathlib import Path
queue_file = Path('/content/DirectorAI/queue.json')
with open(queue_file, 'r') as f:
    for job in json.load(f)['jobs']:
        print(f"{job['job_id']}: {job['status']}")

CHECK GPU:
!nvidia-smi

CHECK DISK SPACE:
!df -BG /content/

LIST RESULTS:
!ls -lah /content/DirectorAI/outputs/


# ============================================================================
# TROUBLESHOOTING QUICK FIXES
# ============================================================================

Problem: "ModuleNotFoundError: No module named 'config'"
Fix:     %cd /content/DirectorAI

Problem: "Models not found"
Fix:     !ls /content/DirectorAI/models/checkpoints/

Problem: "Out of memory"
Fix:     Reduce IMAGE_STEPS in config.py (30 → 20)

Problem: "Drive not mounting"
Fix:     Re-run mount cell, grant permission

Problem: "JSON error"
Fix:     Validate JSON: https://jsonlint.com/


# ============================================================================
# AFTER GENERATION
# ============================================================================

□ Copy results to Google Drive (Cell 10)
□ Download MP4s from Colab Files
□ Edit/process with your tools
□ Upload to YouTube
□ Adjust prompts for next batch
□ Increase batch size for production


# ============================================================================
# DOCUMENTATION FILES
# ============================================================================

COLAB_GUIDE.md             - Overview of Colab setup
COLAB_STEP_BY_STEP.md      - Copy-paste cells for Colab
PROMPTS_GUIDE.md           - How to write effective prompts
README.md                  - Project overview
ARCHITECTURE.md            - Technical architecture


# ============================================================================
# QUICK LINKS
# ============================================================================

Google Colab:           https://colab.research.google.com/
GitHub:                 https://github.com/
JSON Validator:         https://jsonlint.com/
DirectorAI Repo:        https://github.com/YOUR_USERNAME/DirectorAI


# ============================================================================
# SUPPORT
# ============================================================================

If generation fails:
1. Check error in Colab output
2. Read error message carefully
3. Check COLAB_STEP_BY_STEP.md troubleshooting section
4. Verify prompt format
5. Try with simpler prompts first


# ============================================================================
# REMEMBER
# ============================================================================

✓ Models stay on Drive, copied to Colab for speed
✓ Results saved to Drive automatically
✓ Start with 3-5 ideas to test
✓ Increase batch size once working
✓ Colab sessions last 12 hours max
✓ Your files persist on Drive even after session ends


# ============================================================================
# YOU'RE READY!
# ============================================================================

1. Upload models to Drive (if not already done)
2. Push to GitHub
3. Open Google Colab
4. Follow COLAB_STEP_BY_STEP.md
5. Create your prompts.json
6. Start generation!

Good luck! 🚀🎬
