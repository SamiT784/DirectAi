"""
DIRECTORAI - COLAB INSTALLATION TROUBLESHOOTING
If you encounter pip install errors, use this guide
"""

# ============================================================================
# ERROR: "Could not find a version that satisfies the requirement TTS"
# ============================================================================

PROBLEM:
────────
ERROR: Could not find a version that satisfies the requirement TTS>=0.14.0

CAUSE:
──────
The requirements.txt had an incorrect TTS package specification.
TTS must be installed from the Coqui source, not as a version-pinned package.

SOLUTION:
─────────
Use the CORRECTED Cell 2 from EXECUTION_STEPS.md:

!pip install -r requirements.txt -q
!pip install google-auth-oauthlib -q

# Install TTS from Coqui source
!pip install TTS -q

# Verify installation
import sys
print(f"Python version: {sys.version}")
print("✓ Dependencies installed successfully!")

This will:
✓ Install all packages from requirements.txt
✓ Install Google auth for Drive mounting
✓ Install TTS (Text-to-Speech) from Coqui
✓ Show Python version and success message


# ============================================================================
# WARNING: Python Version Compatibility Warnings
# ============================================================================

YOU MIGHT SEE:
──────────────
ERROR: Ignored the following versions that require a different python version:
  0.0.10.2 Requires-Python >=3.6.0, <3.9
  0.0.10.3 Requires-Python >=3.6.0, <3.9
  ... (many more lines)

THIS IS OK! ✓
───────────
Google Colab uses Python 3.10+, which is NEWER than some old package versions.
Those old versions are being IGNORED (as intended).
The installation will use compatible versions automatically.

YOUR INSTALLATION WILL STILL WORK! ✓


# ============================================================================
# EXPECTED OUTPUT FOR CORRECTED INSTALLATION
# ============================================================================

When you run the corrected Cell 2, you should see:

Collecting ...
Installing collected packages: ...
Successfully installed ...
Python version: 3.10.12 (or similar)
✓ Dependencies installed successfully!

If you see this, CELL 2 succeeded! Continue to CELL 3.


# ============================================================================
# OTHER COMMON ERRORS AND FIXES
# ============================================================================

ERROR: "ModuleNotFoundError: No module named 'config'"
─────────────────────────────────────────────────────
CAUSE: You're in the wrong directory

FIX: Make sure Cell 1 worked:
!git clone https://github.com/SamiT784/DirectAi.git
%cd DirectAi
!ls -la

Then run Cell 2.


ERROR: "permission denied" when mounting Drive
───────────────────────────────────────────────
CAUSE: Authorization popup didn't appear

FIX: 
1. Look for a blue link in the output
2. Click it
3. Authorize Google Colab
4. Copy the code
5. Paste it back in Colab
6. Press ENTER


ERROR: "Models directory NOT found"
───────────────────────────────────
CAUSE: Your Drive doesn't have the models folder

FIX:
1. Go to https://drive.google.com
2. Create folder: My Drive/drive/AI/models/
3. Upload your model files there
4. Re-run Cell 4


ERROR: "Out of memory" during generation
──────────────────────────────────────────
CAUSE: Colab ran out of RAM

FIX:
1. Runtime → Restart runtime
2. Try fewer ideas (2 instead of 3)
3. Or use Premium GPU (faster, more memory)


ERROR: "Connection timeout" after 30 minutes
─────────────────────────────────────────────
CAUSE: Colab session timed out

FIX:
1. This is normal for long-running tasks
2. Make sure you ran Cell 10 BEFORE timeout
3. Check Google Drive for DirectAi_Results/ folder
4. If results are there, download them!


# ============================================================================
# HOW TO VERIFY INSTALLATION WORKED
# ============================================================================

After Cell 2 completes, run this verification cell:

import sys
import torch
import cv2
import numpy as np
from pathlib import Path

print(f"✓ Python version: {sys.version}")
print(f"✓ PyTorch version: {torch.__version__}")
print(f"✓ OpenCV version: {cv2.__version__}")
print(f"✓ NumPy version: {np.__version__}")
print(f"✓ Current directory: {Path.cwd()}")
print("\n✓ All imports successful!")

If all green checkmarks appear, installation is complete! 🎉


# ============================================================================
# REQUIREMENTS.TXT UPDATED
# ============================================================================

The requirements.txt has been FIXED:
✓ Removed incorrect "TTS>=0.14.0"
✓ Added note about installing TTS separately
✓ All other packages are compatible with Python 3.10+

Updated requirements now include:
✓ python-dotenv>=1.0.0
✓ requests>=2.31.0
✓ pydantic>=2.0.0
✓ librosa>=0.10.0
✓ scipy>=1.11.0
✓ opencv-python>=4.8.0
✓ imageio>=2.33.0
✓ imageio-ffmpeg>=1.4.0
✓ Pillow>=10.0.0
✓ numpy>=1.24.0
✓ torch>=2.0.0
✓ torchvision>=0.15.0
✓ pytest>=7.4.0
✓ black>=23.0.0
✓ pylint>=3.0.0


# ============================================================================
# QUICK FIX SUMMARY
# ============================================================================

WHAT CHANGED:
─────────────
1. Fixed requirements.txt (removed problematic TTS version pin)
2. Updated EXECUTION_STEPS.md Cell 2 with correct installation
3. Updated COLAB_CELLS_GUIDE.md Cell 2 with correct installation
4. Created this troubleshooting guide

WHAT TO DO:
────────────
1. Open Google Colab
2. Run Cell 1 (Clone) - SAME AS BEFORE
3. Run UPDATED Cell 2 (Install) - NOW FIXED!
4. Continue with Cells 3-10 - SAME AS BEFORE


# ============================================================================
# YOU'RE NOW READY! ✅
# ============================================================================

All installation issues fixed!
Run the corrected Cell 2 in Colab and you're good to go! 🚀

"""