"""
========================================================================
DIRECTORAI - EXECUTION GUIDE FOR GOOGLE COLAB
========================================================================

Your Repository: https://github.com/SamiT784/DirectAi.git
Your Models Location: My Drive/drive/AI/models
Video Format: 9:16 Portrait (540x960) - YouTube Shorts Ready!
Date: Today

This document shows EVERY SINGLE STEP with exact commands.
========================================================================
"""


# ============================================================================
# PREREQUISITE: CHECK YOUR GOOGLE DRIVE
# ============================================================================

BEFORE STARTING COLAB:
1. Go to Google Drive: https://drive.google.com
2. Check you have folder: My Drive/drive/AI/models/
3. Inside, check you have:
   ✓ checkpoints/
     - realisticVisionV60B1_v60B1VAE.safetensors (3GB)
     - v1-5-pruned-emaonly.safetensors (4GB)
     - mm_sd_v15_v2.ckpt (2GB)
   ✓ vae/
     - vae-ft-mse-840000-ema-pruned.safetensors (360MB)

If NOT found: Upload your models first!
If found: Continue to STEP 1 below


# ============================================================================
# STEP 1: OPEN GOOGLE COLAB
# ============================================================================

ACTION: Go to https://colab.research.google.com/
ACTION: Click "+ New notebook"
ACTION: A new Colab notebook will open

You should see an empty code cell ready to paste code.


# ============================================================================
# STEP 2: PASTE AND RUN CELL 1 (CLONE REPOSITORY)
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

!git clone https://github.com/SamiT784/DirectAi.git
%cd DirectAi
!ls -la

────────────────────────────────────────────────────

ACTION: Paste into the cell
ACTION: Press CTRL+ENTER to run

EXPECTED OUTPUT:
Cloning into 'DirectAi'...
remote: Enumerating objects...
...
total 120
drwxr-xr-x  app
drwxr-xr-x  scripts
-rw-r--r--  config.py
-rw-r--r--  main.py
-rw-r--r--  requirements.txt
-rw-r--r--  test_prompts.json

✓ SUCCESS if you see these files!


# ============================================================================
# STEP 3: PASTE AND RUN CELL 2 (INSTALL DEPENDENCIES)
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

!pip install -r requirements.txt -q
!pip install google-auth-oauthlib -q
print("✓ Dependencies installed successfully!")

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

EXPECTED OUTPUT:
✓ Dependencies installed successfully!

⏳ This may take 1-2 minutes. Wait for it to complete!


# ============================================================================
# STEP 4: PASTE AND RUN CELL 3 (MOUNT GOOGLE DRIVE)
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

from google.colab import drive
drive.mount('/content/drive')
print("✓ Google Drive mounted successfully!")

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

EXPECTED OUTPUT:
Go to this URL in a browser window: https://accounts.google.com/o/oauth2/auth?...
Enter the authorization code

ACTION: Click the link
ACTION: Grant permission
ACTION: Copy the code it gives you
ACTION: Paste code back in Colab
ACTION: Press ENTER

EXPECTED OUTPUT:
Mounted at /content/drive
✓ Google Drive mounted successfully!

✓ SUCCESS if you see "Mounted at /content/drive"


# ============================================================================
# STEP 5: PASTE AND RUN CELL 4 (VERIFY MODELS ON DRIVE)
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import os
from pathlib import Path

models_dir = Path('/content/drive/MyDrive/drive/AI/models')

print("Checking models on Google Drive...")
print(f"Looking in: {models_dir}")

if models_dir.exists():
    all_files = list(models_dir.rglob('*'))
    model_files = [f for f in all_files if f.is_file()]
    
    print(f"\n✓ Found {len(model_files)} model files:")
    for model_file in sorted(model_files):
        size_gb = model_file.stat().st_size / (1024**3)
        rel_path = model_file.relative_to(models_dir)
        print(f"  ✓ {rel_path}: {size_gb:.2f} GB")
else:
    print(f"❌ Models directory NOT found at: {models_dir}")
    print("\nTROUBLESHOOTING:")
    print("1. Check your Drive has folder: My Drive/drive/AI/models")
    print("2. Upload your models there")
    print("3. Try again")

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

EXPECTED OUTPUT:
Checking models on Google Drive...
Looking in: /content/drive/MyDrive/drive/AI/models

✓ Found 4 model files:
  ✓ checkpoints/realisticVisionV60B1_v60B1VAE.safetensors: 3.45 GB
  ✓ checkpoints/v1-5-pruned-emaonly.safetensors: 4.16 GB
  ✓ checkpoints/mm_sd_v15_v2.ckpt: 2.01 GB
  ✓ vae/vae-ft-mse-840000-ema-pruned.safetensors: 0.34 GB

✓ SUCCESS if all 4 files are found!
❌ FAIL if you get "NOT found" - check your Drive structure


# ============================================================================
# STEP 6: PASTE AND RUN CELL 5 (COPY MODELS TO COLAB) ⏳ 5-10 MINUTES!
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import shutil
import time
from pathlib import Path

src = Path('/content/drive/MyDrive/drive/AI/models')
dst = Path('/content/DirectAi/models')

print("Copying models from Drive to Colab (5-15 minutes)...")
print(f"Source: {src}")
print(f"Destination: {dst}")
print("=" * 60)

try:
    dst.mkdir(parents=True, exist_ok=True)
    
    start_time = time.time()
    total_size = 0
    
    for src_file in src.rglob('*'):
        if src_file.is_file():
            rel_path = src_file.relative_to(src)
            dst_file = dst / rel_path
            
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_size = src_file.stat().st_size
            total_size += file_size
            shutil.copy2(src_file, dst_file)
            size_mb = file_size / (1024**2)
            print(f"✓ Copied: {rel_path} ({size_mb:.1f} MB)")
    
    elapsed = time.time() - start_time
    total_gb = total_size / (1024**3)
    speed_mbps = (total_size / (1024**2)) / elapsed
    
    print("=" * 60)
    print(f"✓ Models copied successfully!")
    print(f"  - Total size: {total_gb:.1f} GB")
    print(f"  - Time: {elapsed:.1f} seconds")
    print(f"  - Speed: {speed_mbps:.1f} MB/s")
    
except Exception as e:
    print(f"❌ Error copying models: {e}")

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

⏳ WAIT 5-10 MINUTES! This is copying 9GB of models!

EXPECTED OUTPUT:
Copying models from Drive to Colab (5-15 minutes)...
...
✓ Copied: checkpoints/realisticVisionV60B1_v60B1VAE.safetensors (3450.2 MB)
✓ Copied: checkpoints/v1-5-pruned-emaonly.safetensors (4160.1 MB)
✓ Copied: checkpoints/mm_sd_v15_v2.ckpt (2010.3 MB)
✓ Copied: vae/vae-ft-mse-840000-ema-pruned.safetensors (340.5 MB)
============================================================
✓ Models copied successfully!
  - Total size: 9.96 GB
  - Time: 450.2 seconds
  - Speed: 22.1 MB/s

✓ SUCCESS if it says "copied successfully"!


# ============================================================================
# STEP 7: PASTE AND RUN CELL 6 (TEST EVERYTHING)
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

%cd /content/DirectAi
!python test_architecture.py

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

EXPECTED OUTPUT:
Testing DirectorAI Architecture...
─────────────────────────────
✓ Configuration loaded
✓ Orchestrator initialized
✓ Batch queue ready
✓ Script engine loaded
✓ Prompt engine loaded
✓ Narration engine loaded
✓ Scene engine loaded
✓ Interpolation engine loaded
✓ Render engine loaded
✓ Workflow engine loaded
─────────────────────────────
✓ All engines loaded successfully!

✓ SUCCESS if all engines load!


# ============================================================================
# STEP 8: PASTE AND RUN CELL 7 (GENERATE YOUR VIDEOS!)
# ============================================================================

COPY THIS EXACTLY:
────────────────────────────────────────────────────

%cd /content/DirectAi
!python main.py --mode batch --ideas-file test_prompts.json

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

⏳ WAIT 15-45 MINUTES! This generates 3 YouTube Shorts!

EXPECTED OUTPUT:
Processing batch: 3 ideas
─────────────────────────────
✓ Job 1: Cleopatra VII, the last pharaoh...
✓ Job 2: The eruption of Mount Vesuvius...
✓ Job 3: Joan of Arc, leading French armies...
─────────────────────────────
Generation started!
Processing batch...
Job 1: PROCESSING
Job 2: QUEUED
Job 3: QUEUED

(It will show progress as it generates each idea)

✓ SUCCESS when it finishes all jobs!


# ============================================================================
# STEP 9 (OPTIONAL): MONITOR PROGRESS WHILE GENERATING
# ============================================================================

While STEP 8 is running, you can monitor progress:

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import json
from pathlib import Path
import time

queue_file = Path('/content/DirectAi/queue.json')

print("Monitoring generation progress...")
print("=" * 60)

for i in range(100):  # Check up to 100 times (30+ minutes)
    if queue_file.exists():
        with open(queue_file, 'r') as f:
            queue = json.load(f)
            
            print(f"\n[{time.strftime('%H:%M:%S')}] Status:")
            for job in queue['jobs']:
                status = job['status']
                idea = job['idea'][:40] + "..." if len(job['idea']) > 40 else job['idea']
                
                if status == "COMPLETED":
                    symbol = "✓"
                elif status == "PROCESSING":
                    symbol = "⏳"
                elif status == "QUEUED":
                    symbol = "⏸"
                elif status == "FAILED":
                    symbol = "❌"
                else:
                    symbol = "?"
                
                print(f"  {symbol} Job {job['job_id']}: {status:10} | {idea}")
            
            # Check if all done
            statuses = [j['status'] for j in queue['jobs']]
            if all(s in ['COMPLETED', 'FAILED', 'SKIPPED'] for s in statuses):
                print("\n✓ All jobs completed!")
                break
    
    time.sleep(30)

────────────────────────────────────────────────────

ACTION: Paste into NEW cell (while Cell 7 is still running)
ACTION: Press CTRL+ENTER to run

This shows progress every 30 seconds:
✓ COMPLETED = Video finished
⏳ PROCESSING = Currently generating
⏸ QUEUED = Waiting to start
❌ FAILED = Error occurred


# ============================================================================
# STEP 10: PASTE AND RUN CELL 10 (COPY TO GOOGLE DRIVE) ⚠️ IMPORTANT!
# ============================================================================

Run this AFTER generation completes (Cell 7 finishes):

COPY THIS EXACTLY:
────────────────────────────────────────────────────

import shutil
from pathlib import Path
import time

src = Path('/content/DirectAi/outputs')
dst = Path('/content/drive/MyDrive/DirectAi_Results')

print("Copying results from Colab to Google Drive...")
print(f"Source: {src}")
print(f"Destination: {dst}")
print("=" * 60)

try:
    start_time = time.time()
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copytree(src, dst, dirs_exist_ok=True)
    
    elapsed = time.time() - start_time
    
    mp4_files = list(dst.glob('*/final/final_short.mp4'))
    
    print(f"\n✓ Results copied successfully!")
    print(f"  - MP4 files: {len(mp4_files)}")
    print(f"  - Time: {elapsed:.1f} seconds")
    print(f"  - Location: My Drive/DirectAi_Results/")
    
    for i, mp4 in enumerate(sorted(mp4_files), 1):
        size_mb = mp4.stat().st_size / (1024**2)
        print(f"\n  {i}. {mp4.parent.parent.name}: {size_mb:.1f} MB")
        print(f"     ✓ Ready for YouTube!")
    
except Exception as e:
    print(f"❌ Error copying results: {e}")

────────────────────────────────────────────────────

ACTION: Paste into NEW cell
ACTION: Press CTRL+ENTER to run

⏳ WAIT 2-5 MINUTES to copy results to Drive

EXPECTED OUTPUT:
Copying results from Colab to Google Drive...
Source: /content/DirectAi/outputs
Destination: /content/drive/MyDrive/DirectAi_Results
============================================================

✓ Results copied successfully!
  - MP4 files: 3
  - Time: 180.5 seconds
  - Location: My Drive/DirectAi_Results/

  1. short_001: 45.2 MB
     ✓ Ready for YouTube!

  2. short_002: 42.1 MB
     ✓ Ready for YouTube!

  3. short_003: 48.9 MB
     ✓ Ready for YouTube!

✓ SUCCESS if all 3 videos copied!

⚠️ IMPORTANT: Do this BEFORE your Colab session times out!


# ============================================================================
# STEP 11: DOWNLOAD YOUR VIDEOS FROM GOOGLE DRIVE
# ============================================================================

ACTION: Go to Google Drive: https://drive.google.com
ACTION: Navigate to: My Drive → DirectAi_Results
ACTION: You should see:
  ├── short_001/
  │   └── final/
  │       └── final_short.mp4 ← RIGHT-CLICK → DOWNLOAD
  ├── short_002/
  │   └── final/
  │       └── final_short.mp4 ← RIGHT-CLICK → DOWNLOAD
  └── short_003/
      └── final/
          └── final_short.mp4 ← RIGHT-CLICK → DOWNLOAD

ACTION: Download each MP4 file


# ============================================================================
# STEP 12: UPLOAD TO YOUTUBE AS SHORTS
# ============================================================================

Now you have 3 YouTube Shorts ready!

ACTION: Go to YouTube Studio: https://studio.youtube.com
ACTION: Click "CREATE" → "Upload video"
ACTION: Upload each MP4
ACTION: Set as "Shorts"
ACTION: Add title, description, tags
ACTION: Publish!

✓ VIDEO SPECS:
   Format: MP4
   Ratio: 9:16 (Portrait - Perfect for YouTube Shorts!)
   Resolution: 540x960 pixels
   Duration: 1-2 minutes
   Ready to upload!


# ============================================================================
# SUMMARY - WHAT YOU DID
# ============================================================================

✓ Step 1: Opened Google Colab
✓ Step 2: Cloned your DirectAI repository
✓ Step 3: Installed dependencies
✓ Step 4: Mounted Google Drive
✓ Step 5: Verified your models
✓ Step 6: Copied models to Colab (5-10 min)
✓ Step 7: Tested that everything works
✓ Step 8: Generated 3 YouTube Shorts (15-45 min)
✓ Step 9: Monitored progress
✓ Step 10: Copied results to Drive (2-5 min)
✓ Step 11: Downloaded MP4s to your computer
✓ Step 12: Uploaded to YouTube!

TOTAL TIME: ~45-90 minutes (includes model copy + generation)
RESULT: 3 YouTube Shorts about historical events, 9:16 portrait format!


# ============================================================================
# NEXT TIME (IF COLAB DISCONNECTS)
# ============================================================================

Next session is FASTER because models are already on Drive:

1. Open new Colab notebook
2. Run Step 2 (Clone - 30 sec)
3. Run Step 3 (Install - 1 min)
4. Run Step 4 (Mount - 10 sec)
5. Skip Step 5 (models already there)
6. Run Step 7 (Generate - 15-45 min)
7. Run Step 10 (Copy to Drive - 2-5 min)
8. Download!

TOTAL TIME NEXT TIME: ~20-60 minutes (no model copy!)


# ============================================================================
# YOUR REPOSITORY & PATHS (FOR REFERENCE)
# ============================================================================

Repository: https://github.com/SamiT784/DirectAi.git
Clone Command: git clone https://github.com/SamiT784/DirectAi.git

Your Models: My Drive/drive/AI/models/
Generated Videos: My Drive/DirectAi_Results/ (auto-created)

Video Format: 540x960 (9:16 portrait)
3 Test Ideas: Cleopatra, Mount Vesuvius, Joan of Arc
Test File: test_prompts.json


# ============================================================================
# YOU'RE DONE! 🎬📹✨
# ============================================================================

You now have 3 beautiful historical YouTube Shorts!
Format: Perfect 9:16 portrait
Quality: HD (540x960)
Ready to: Upload to YouTube

Congratulations! Your DirectorAI system is working! 🚀

"""