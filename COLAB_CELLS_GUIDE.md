"""
DIRECTORAI - COLAB SETUP GUIDE
Repository: https://github.com/SamiT784/DirectAi.git
Models Location: My Drive/drive/AI/models
Video Ratio: 9:16 (540x960) - YouTube Shorts Ready!
"""

# ============================================================================
# COLAB CELL 1: CLONE REPOSITORY
# ============================================================================

!git clone https://github.com/SamiT784/DirectAi.git
%cd DirectAi
!ls -la

# Expected Output:
# Cloning into 'DirectAi'...
# remote: Enumerating objects...
# total XX
# drwxr-xr-x  app
# drwxr-xr-x  scripts
# -rw-r--r--  config.py
# -rw-r--r--  main.py
# -rw-r--r--  requirements.txt
# -rw-r--r--  test_prompts.json
# ✓ Repository cloned successfully!


# ============================================================================
# COLAB CELL 2: INSTALL DEPENDENCIES
# ============================================================================

!pip install -r requirements.txt -q
!pip install google-auth-oauthlib -q
print("✓ Dependencies installed successfully!")

# Expected Output:
# ✓ Dependencies installed successfully!


# ============================================================================
# COLAB CELL 3: MOUNT GOOGLE DRIVE
# ============================================================================

from google.colab import drive
drive.mount('/content/drive')
print("✓ Google Drive mounted successfully!")

# Expected Output:
# Mounted at /content/drive
# ✓ Google Drive mounted successfully!


# ============================================================================
# COLAB CELL 4: VERIFY MODELS ON DRIVE
# ============================================================================

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
    print("2. Upload your models there (checkpoints & vae)")
    print("3. Refresh and try again")


# ============================================================================
# COLAB CELL 5: COPY MODELS FROM DRIVE TO COLAB
# ============================================================================

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
    # Ensure destination exists
    dst.mkdir(parents=True, exist_ok=True)
    
    # Copy all model files
    start_time = time.time()
    total_size = 0
    
    for src_file in src.rglob('*'):
        if src_file.is_file():
            # Create relative path
            rel_path = src_file.relative_to(src)
            dst_file = dst / rel_path
            
            # Create destination directory
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
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


# ============================================================================
# COLAB CELL 6: TEST ARCHITECTURE
# ============================================================================

%cd /content/DirectAi
!python test_architecture.py

# Expected Output:
# ✓ All engines loaded successfully!
# ✓ Configuration loaded
# ✓ Orchestrator initialized
# ✓ Batch queue ready
# ✓ Script engine loaded
# ✓ Prompt engine loaded
# ✓ Narration engine loaded
# ✓ Scene engine loaded
# ✓ Interpolation engine loaded
# ✓ Render engine loaded
# ✓ Workflow engine loaded


# ============================================================================
# COLAB CELL 7: RUN BATCH GENERATION
# ============================================================================

%cd /content/DirectAi
!python main.py --mode batch --ideas-file test_prompts.json

# Expected Output:
# Processing batch: 3 ideas
# ─────────────────────────────────────
# Job 1: Cleopatra VII...
# Job 2: Mount Vesuvius...
# Job 3: Joan of Arc...
# ─────────────────────────────────────
# Generation started!


# ============================================================================
# COLAB CELL 8: MONITOR PROGRESS (RUN WHILE GENERATING)
# ============================================================================

import json
from pathlib import Path
import time

queue_file = Path('/content/DirectAi/queue.json')

print("Monitoring generation progress...")
print("=" * 60)

while True:
    if queue_file.exists():
        with open(queue_file, 'r') as f:
            queue = json.load(f)
            
            print(f"\n[{time.strftime('%H:%M:%S')}] Status Update:")
            for job in queue['jobs']:
                job_id = job['job_id']
                status = job['status']
                idea = job['idea'][:50] + "..." if len(job['idea']) > 50 else job['idea']
                
                # Status symbols
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
                
                print(f"  {symbol} Job {job_id}: {status:10} | {idea}")
            
            # Check if all done
            statuses = [j['status'] for j in queue['jobs']]
            if all(s in ['COMPLETED', 'FAILED', 'SKIPPED'] for s in statuses):
                print("\n" + "=" * 60)
                print("✓ All jobs completed!")
                completed = sum(1 for s in statuses if s == 'COMPLETED')
                failed = sum(1 for s in statuses if s == 'FAILED')
                print(f"  - Completed: {completed}")
                print(f"  - Failed: {failed}")
                break
        
        print("Checking again in 30 seconds...", end="")
        time.sleep(30)
        print(" done!")
    else:
        print("⏳ Waiting for queue.json...")
        time.sleep(5)


# ============================================================================
# COLAB CELL 9: CHECK GENERATED VIDEOS
# ============================================================================

import os
from pathlib import Path

results_dir = Path('/content/DirectAi/outputs')

print("Generated Videos on Colab:")
print("=" * 60)

if results_dir.exists():
    video_files = list(results_dir.glob('*/final/final_short.mp4'))
    
    if video_files:
        print(f"✓ Found {len(video_files)} YouTube Shorts:\n")
        for i, video in enumerate(sorted(video_files), 1):
            size_mb = video.stat().st_size / (1024**2)
            duration_sec = int(video.stat().st_size / (1024*100))  # rough estimate
            short_name = video.parent.parent.name
            print(f"{i}. {short_name}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"   Path: {video}")
            print()
    else:
        print("No videos found yet. Still generating?")
else:
    print(f"❌ outputs directory not found at {results_dir}")


# ============================================================================
# COLAB CELL 10: COPY RESULTS TO GOOGLE DRIVE
# ============================================================================

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
    
    # Create destination if it doesn't exist
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy all outputs
    shutil.copytree(src, dst, dirs_exist_ok=True)
    
    elapsed = time.time() - start_time
    
    # Count files
    mp4_files = list(dst.glob('*/final/final_short.mp4'))
    
    print(f"\n✓ Results copied successfully!")
    print(f"  - MP4 files: {len(mp4_files)}")
    print(f"  - Time: {elapsed:.1f} seconds")
    print(f"  - Location: My Drive/DirectAi_Results/")
    
    for i, mp4 in enumerate(sorted(mp4_files), 1):
        size_mb = mp4.stat().st_size / (1024**2)
        print(f"\n  {i}. {mp4.parent.parent.name}")
        print(f"     Size: {size_mb:.1f} MB")
        print(f"     Ready for YouTube upload! 🎬")
    
except Exception as e:
    print(f"❌ Error copying results: {e}")


# ============================================================================
# COLAB CELL 11: LIST FILES ON DRIVE FOR DOWNLOAD
# ============================================================================

from pathlib import Path

results_dir = Path('/content/drive/MyDrive/DirectAi_Results')

print("YouTube Shorts Ready for Download:")
print("=" * 60)

if results_dir.exists():
    mp4_files = sorted(results_dir.glob('*/final/final_short.mp4'))
    
    print(f"✓ Found {len(mp4_files)} videos in My Drive\n")
    print("Location: My Drive → DirectAi_Results → short_XXX → final → final_short.mp4\n")
    
    for i, mp4 in enumerate(mp4_files, 1):
        size_mb = mp4.stat().st_size / (1024**2)
        short_name = mp4.parent.parent.name
        print(f"{i}. {short_name}: {size_mb:.1f} MB")
        print(f"   Download and upload to YouTube!")
        print()
else:
    print("❌ Results not found. Did you run Cell 10?")


# ============================================================================
# COLAB CELL 12: CREATE YOUR CUSTOM PROMPTS (OPTIONAL)
# ============================================================================

# Replace the test_prompts.json with your own ideas!

import json

custom_ideas = {
    "ideas": [
        "Your historical idea 1",
        "Your historical idea 2",
        "Your historical idea 3"
    ]
}

# Save to Colab
with open('/content/DirectAi/custom_prompts.json', 'w') as f:
    json.dump(custom_ideas, f, indent=2)

print("✓ Custom prompts saved!")
print("\nThen run this command to generate with your ideas:")
print("!python main.py --mode batch --ideas-file custom_prompts.json")


# ============================================================================
# DIRECTORY STRUCTURE REFERENCE
# ============================================================================

"""
MY GOOGLE DRIVE STRUCTURE:
My Drive/
├── drive/AI/models/              ← YOUR MODELS HERE
│   ├── checkpoints/
│   │   ├── realisticVisionV60B1_v60B1VAE.safetensors
│   │   ├── v1-5-pruned-emaonly.safetensors
│   │   └── mm_sd_v15_v2.ckpt
│   └── vae/
│       └── vae-ft-mse-840000-ema-pruned.safetensors
└── DirectAi_Results/            ← YOUR GENERATED VIDEOS HERE
    ├── short_001/
    │   ├── script/
    │   ├── audio/
    │   ├── scenes/
    │   ├── renders/
    │   └── final/
    │       └── final_short.mp4  ← DOWNLOAD THIS!
    ├── short_002/
    └── short_003/


COLAB STORAGE STRUCTURE:
/content/
├── DirectAi/                     ← Cloned repository
│   ├── app/
│   ├── scripts/
│   ├── config.py
│   ├── main.py
│   ├── test_prompts.json
│   └── models/                   ← Models copied here (5-10min)
│       ├── checkpoints/
│       └── vae/
└── drive/                        ← Your Google Drive (mounted)
    └── MyDrive/
        ├── drive/AI/models/      ← Source of models
        └── DirectAi_Results/     ← Destination for results
"""


# ============================================================================
# IMPORTANT NOTES
# ============================================================================

"""
✓ Video Format: 9:16 Portrait (540x960) - YOUTUBE SHORTS READY!
✓ Aspect Ratio: Perfect for vertical viewing
✓ Repository: https://github.com/SamiT784/DirectAi.git
✓ Models: Stored in My Drive/drive/AI/models (won't be deleted)
✓ Results: Automatically copied to My Drive/DirectAi_Results

TIPS:
1. Run cells in order (1-10)
2. Cells 1-6: Setup (first time only)
3. Cells 7-10: Generate and download (repeat each session)
4. Cell 8: Optional - only if you want to monitor progress
5. Cell 10: Important - copies results to Drive before Colab session ends

NEXT SESSION (if Colab times out):
1. Run Cell 1: Clone again (fast)
2. Run Cell 2: Install again (fast)
3. Run Cell 3: Mount Drive again
4. Run Cell 5: Copy models again (only if you deleted them)
5. Run Cell 7: Generate again

OPTIMIZATION:
- To make generation faster: Edit config.py, change steps: 30 → 20
- To make generation higher quality: Change steps: 30 → 50
- To generate more ideas at once: Use larger test_prompts.json
"""
