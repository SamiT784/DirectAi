"""
DIRECTORAI - COMPLETE SETUP CHECKLIST
Print this out and check items as you go!
"""

# ============================================================================
# COLAB SETUP CHECKLIST
# ============================================================================

BEFORE STARTING:
═════════════════════════════════════════

□ Downloaded DirectorAI from GitHub
□ Read: START_HERE.md (5 minutes)
□ Have Google account
□ Have model files ready (or know where to download)


PHASE 1: PREPARE MODELS (1 HOUR)
═════════════════════════════════════════

□ Create folder: My Drive/DirectorAI_Models
□ Create subfolder: My Drive/DirectorAI_Models/checkpoints
□ Create subfolder: My Drive/DirectorAI_Models/vae
□ Upload: realisticVisionV60B1_v60B1VAE.safetensors (3GB)
□ Upload: v1-5-pruned-emaonly.safetensors (4GB)
□ Upload: mm_sd_v15_v2.ckpt (2GB)
□ Upload: vae-ft-mse-840000-ema-pruned.safetensors (360MB)

VERIFY:
□ All models visible in Drive folders
□ Uploads complete (100%)


PHASE 2: GITHUB SETUP (5-10 MINUTES)
═════════════════════════════════════════

□ Create GitHub repo: DirectorAI
□ Initialize locally:
   git init
   git add .
   git commit -m "Initial setup"
   git branch -M main
   git remote add origin https://github.com/USERNAME/DirectorAI.git
   git push -u origin main

□ Copy GitHub repo URL
□ Verified code is on GitHub


PHASE 3: COLAB SETUP (30 MINUTES)
═════════════════════════════════════════

COLAB CELL 1 - Clone Repository
□ Open: https://colab.research.google.com
□ New notebook created
□ Pasted & ran:
   !git clone https://github.com/YOUR_USERNAME/DirectorAI.git
   %cd DirectorAI
   !ls -la

COLAB CELL 2 - Install Dependencies
□ Ran:
   !pip install -r requirements.txt -q
   !pip install google-auth-oauthlib -q
□ No errors

COLAB CELL 3 - Mount Drive
□ Ran:
   from google.colab import drive
   drive.mount('/content/drive')
□ Granted permission when prompted
□ Verified mount successful

COLAB CELL 4 - Verify Models
□ Ran model verification
□ All 4 models found on Drive ✓
□ File sizes confirmed (2-7GB each)

COLAB CELL 5 - Copy Models to Colab
□ Ran model copy script
□ Waited 5-10 minutes for models to copy
□ Verified copied to /content/DirectorAI/models/

COLAB CELL 6 - Test Architecture
□ Ran:
   %cd /content/DirectorAI
   !python test_architecture.py
□ Output shows: "✓ All engines loaded successfully!"


PHASE 4: CREATE PROMPTS (5 MINUTES)
═════════════════════════════════════════

COLAB CELL 7 - Create Prompts File
□ Created prompts.json with my historical ideas
□ Used format:
   {
     "ideas": [
       "Idea 1",
       "Idea 2"
     ]
   }
□ Validated JSON format

PROMPTS QUALITY CHECK:
□ Each idea 1-3 sentences
□ Specific person/group mentioned
□ Specific event mentioned
□ Time period included
□ 100-300 characters per idea
□ At least 3 ideas
□ No generic descriptions


PHASE 5: TEST GENERATION (15 MINUTES)
═════════════════════════════════════════

COLAB CELL 8 - Single Short Test
□ Ran:
   !python main.py --mode single --idea "Cleopatra VII..."
□ Generation started
□ Waited 5-15 minutes

COLAB CELL 9 - Check Output
□ Ran:
   !ls -lah /content/DirectorAI/outputs/short_001/
□ Output structure verified:
   ✓ script/ directory exists
   ✓ audio/ directory exists
   ✓ scenes/ directory exists
   ✓ renders/ directory exists
   ✓ metadata/ directory exists
   ✓ final/ directory exists


PHASE 6: BATCH GENERATION (5-300 MINUTES)
═════════════════════════════════════════

COLAB CELL 10 - Batch Generation
□ Ran:
   !python main.py --mode batch --ideas-file prompts.json
□ Generation started
□ Number of ideas processed: ___ (3? 5? 10?)
□ Watched progress

COLAB CELL 11 - Monitor Progress (Optional)
□ Ran progress check cell:
   import json
   from pathlib import Path
   queue_file = Path('/content/DirectorAI/queue.json')
   with open(queue_file, 'r') as f:
       for job in json.load(f)['jobs']:
           print(f"Job {job['job_id']}: {job['status']}")
□ Checked multiple times during generation
□ Noted completion status


PHASE 7: COPY TO DRIVE (5 MINUTES)
═════════════════════════════════════════

COLAB CELL 12 - Copy Results
□ Ran:
   import shutil
   shutil.copytree('/content/DirectorAI/outputs', 
                   '/content/drive/MyDrive/DirectorAI_Results', 
                   dirs_exist_ok=True)
□ Results copied to Google Drive
□ No errors

COLAB CELL 13 - Verify Results
□ Checked Google Drive:
   My Drive → DirectorAI_Results → short_001/ etc.
□ Each short has subdirectories with files


PHASE 8: DOWNLOAD (5 MINUTES)
═════════════════════════════════════════

□ Option 1 - Download from Colab Files:
   Left panel → Files → outputs/ → short_XXX/final → final_short.mp4
   Right-click → Download

□ Option 2 - Download from Google Drive:
   DirectorAI_Results/ → short_XXX/final/ → final_short.mp4
   Right-click → Download

□ Downloaded all MP4s


QUALITY CHECK:
═════════════════════════════════════════

For each generated short:
□ File size > 1MB (real file, not empty)
□ Playable in media player
□ Duration: 1-2 minutes (expected for shorts)
□ Video quality reasonable
□ No glitches or corruption


FINAL VERIFICATION:
═════════════════════════════════════════

□ All setup steps completed successfully
□ At least one short generated
□ Results saved to Google Drive
□ MP4 files downloaded locally
□ No blocking errors

Ready for production batch generation:
□ Code is on GitHub (can pull in future sessions)
□ Models are on Drive (persistent storage)
□ Process is documented (can repeat anytime)
□ Output format is consistent (ready for YouTube)


NEXT STEPS (OPTIONAL):
═════════════════════════════════════════

For future sessions:

□ Generate 10+ ideas next time
□ Experiment with different historical periods
□ Adjust prompts based on results
□ Optimize config.py for faster/higher quality
□ Integrate LLM for better script generation
□ Load XTTS for real voice narration
□ Setup ComfyUI integration
□ Scale to 50+ batch generation


NOTES:
═════════════════════════════════════════

Session 1:
- Date: ___________
- Number of shorts generated: ___
- Notes: ________________________________

Session 2:
- Date: ___________
- Number of shorts generated: ___
- Notes: ________________________________

Session 3:
- Date: ___________
- Number of shorts generated: ___
- Notes: ________________________________


TROUBLESHOOTING LOG:
═════════════════════════════════════════

Any issues encountered:
□ Issue: ______________________
  Solution: ___________________

□ Issue: ______________________
  Solution: ___________________

□ Issue: ______________________
  Solution: ___________________


✅ COMPLETE - YOU'RE READY TO GENERATE!
═════════════════════════════════════════

Congratulations! Your DirectorAI system is set up and working.

Next time you want to generate shorts:
1. Open Google Colab
2. Clone DirectorAI again: !git clone ...
3. Run cells 2-7 for setup (models already on Drive)
4. Create/update prompts.json
5. Run Cell 10 for batch generation
6. Download results

Total time: 20 minutes setup + generation time


SAVE THIS CHECKLIST:
Print or screenshot this checklist for future reference!

═════════════════════════════════════════════════════════════════════
Good luck generating your historical YouTube Shorts! 🚀🎬📹
═════════════════════════════════════════════════════════════════════
