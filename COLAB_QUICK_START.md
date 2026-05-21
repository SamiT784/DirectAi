"""
DIRECTORAI COLAB - QUICK STEPS
Repository: https://github.com/SamiT784/DirectAi.git
Models: My Drive/drive/AI/models
Video: 9:16 Portrait (540x960) - YouTube Shorts!
"""

# ============================================================================
# STEP-BY-STEP COLAB EXECUTION
# ============================================================================

STEP 1: GO TO GOOGLE COLAB
─────────────────────────────
1. Open: https://colab.research.google.com/
2. Create NEW NOTEBOOK
3. Name it: "DirectAI Generation"


STEP 2: COPY-PASTE CELLS IN ORDER
──────────────────────────────────

CELL 1: Clone Repository
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 1]
!git clone https://github.com/SamiT784/DirectAi.git
%cd DirectAi
!ls -la

✓ EXPECTED: See files list with config.py, main.py, etc.


CELL 2: Install Dependencies  
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 2]
!pip install -r requirements.txt -q
!pip install google-auth-oauthlib -q
print("✓ Dependencies installed successfully!")

✓ EXPECTED: No errors, prints success message


CELL 3: Mount Drive
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 3]
from google.colab import drive
drive.mount('/content/drive')
print("✓ Google Drive mounted successfully!")

✓ EXPECTED: Click link → Authorize → "Mounted at /content/drive"


CELL 4: Verify Models Location
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 4]
import os
from pathlib import Path

models_dir = Path('/content/drive/MyDrive/drive/AI/models')
...

✓ EXPECTED: Shows all your model files with sizes
❌ IF NOT FOUND: Check your Drive has folder: My Drive/drive/AI/models/


CELL 5: Copy Models (5-10 MINUTES - WAIT!)
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 5]
import shutil
import time
from pathlib import Path
...

✓ EXPECTED: "Copying models from Drive to Colab..."
             Shows progress
             "✓ Models copied successfully!"
⏳ NOTE: This takes 5-15 minutes. DO NOT INTERRUPT!


CELL 6: Test Everything Works
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 6]
%cd /content/DirectAi
!python test_architecture.py

✓ EXPECTED: Shows "✓ All engines loaded successfully!"
             Lists all 7 engines


CELL 7: Generate Your Videos!
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 7]
%cd /content/DirectAi
!python main.py --mode batch --ideas-file test_prompts.json

✓ EXPECTED: "Processing batch: 3 ideas"
             "Generation started!"


CELL 8: Monitor Progress (OPTIONAL - RUN WHILE CELL 7 IS GENERATING)
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 8]
import json
from pathlib import Path
import time
...

✓ SHOWS: Status of each job
         ✓ COMPLETED, ⏳ PROCESSING, ⏸ QUEUED
         When all done: "✓ All jobs completed!"


CELL 9: Check Videos
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 9]
import os
from pathlib import Path

results_dir = Path('/content/DirectAi/outputs')
...

✓ SHOWS: How many videos generated and their sizes


CELL 10: IMPORTANT! Copy to Google Drive
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 10]
import shutil
from pathlib import Path
import time
...

✓ EXPECTED: "Results copied successfully!"
             Shows location: My Drive/DirectAi_Results/
⚠️ IMPORTANT: Run this BEFORE Colab session ends!


CELL 11: Download Link
[Copy from COLAB_CELLS_GUIDE.md - COLAB CELL 11]
from pathlib import Path

results_dir = Path('/content/drive/MyDrive/DirectAi_Results')
...

✓ SHOWS: Files ready in Google Drive


# ============================================================================
# YOUR GOOGLE DRIVE STRUCTURE
# ============================================================================

✓ Check you have this structure:

My Drive/
├── drive/
│   └── AI/
│       └── models/                    ← YOUR MODELS MUST BE HERE
│           ├── checkpoints/
│           │   ├── realisticVisionV60B1_v60B1VAE.safetensors (3GB)
│           │   ├── v1-5-pruned-emaonly.safetensors (4GB)
│           │   └── mm_sd_v15_v2.ckpt (2GB)
│           └── vae/
│               └── vae-ft-mse-840000-ema-pruned.safetensors (360MB)


✓ After generation, you'll have:

My Drive/
└── DirectAi_Results/                  ← AUTO-CREATED
    ├── short_001/
    │   └── final/
    │       └── final_short.mp4  ← DOWNLOAD THIS!
    ├── short_002/
    │   └── final/
    │       └── final_short.mp4  ← DOWNLOAD THIS!
    └── short_003/
        └── final/
            └── final_short.mp4  ← DOWNLOAD THIS!


# ============================================================================
# VIDEO SPECIFICATIONS
# ============================================================================

FORMAT: 9:16 PORTRAIT (YouTube Shorts Ready!)
────────────────────
Resolution: 540 x 960 pixels
Aspect Ratio: 9:16
Duration: 1-2 minutes (can be edited)
Format: MP4 (H.264 codec)
Status: READY FOR YOUTUBE UPLOAD!


# ============================================================================
# GENERATION TIMINGS
# ============================================================================

Cell 1 (Clone): 30 seconds
Cell 2 (Install): 1-2 minutes
Cell 3 (Mount): 10 seconds
Cell 4 (Check): 5 seconds
Cell 5 (Copy Models): 5-10 MINUTES ⏳
Cell 6 (Test): 30 seconds
Cell 7 (Generate 3 ideas): 15-45 minutes ⏳
  - Per idea: 5-15 minutes each
Cell 8 (Monitor): Optional, shows progress
Cell 9 (Check): 5 seconds
Cell 10 (Copy to Drive): 2-5 minutes
Cell 11 (Links): 5 seconds

TOTAL FIRST TIME: ~30-60 minutes (including model copy)
TOTAL GENERATION: Depends on number of ideas


# ============================================================================
# IF SOMETHING GOES WRONG
# ============================================================================

PROBLEM: "git: command not found"
→ This shouldn't happen in Colab. Try Cell 1 again.

PROBLEM: "ModuleNotFoundError: No module named 'config'"
→ Make sure you're in correct directory: %cd DirectAi

PROBLEM: Models not found in Cell 4
→ Check: My Drive/drive/AI/models exists
→ Check: Files are actually there
→ If not there, upload them!

PROBLEM: "Permission denied" when copying models
→ Colab may need to restart
→ Runtime → Restart all runtimes

PROBLEM: Generation very slow
→ Normal! Can be 15 minutes per idea
→ Check Cell 8 monitor - should show progress

PROBLEM: Out of memory error
→ Runtime → Restart runtime
→ Try generating fewer ideas (2 instead of 3)

PROBLEM: Can't find results in Drive
→ Make sure you ran Cell 10!
→ Check: My Drive/DirectAi_Results/


# ============================================================================
# CHEAT SHEET - QUICK COMMANDS
# ============================================================================

Generate with test prompts:
!python main.py --mode batch --ideas-file test_prompts.json

Generate single idea:
!python main.py --mode single --idea "Your historical idea here"

Check if files exist:
!ls -lah /content/DirectAi/outputs/

See what's in Drive:
!ls -lah /content/drive/MyDrive/

Count generated videos:
!find /content/DirectAi/outputs -name "final_short.mp4" | wc -l


# ============================================================================
# NEXT STEPS
# ============================================================================

1. ✅ Open Google Colab
2. ✅ Run Cells 1-11 in order
3. ✅ Wait for generation (15-45 min for 3 videos)
4. ✅ Download MP4s from My Drive/DirectAi_Results/
5. ✅ Upload to YouTube as Shorts!

THAT'S IT! Your historical YouTube Shorts are ready! 🎬📹✨


# ============================================================================
# REFERENCE LINKS
# ============================================================================

Repository: https://github.com/SamiT784/DirectAi.git
Google Colab: https://colab.research.google.com/
YouTube Shorts Info: https://support.google.com/youtube/answer/7126552
Full Guide: See COLAB_CELLS_GUIDE.md for detailed explanations
"""