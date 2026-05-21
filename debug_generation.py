#!/usr/bin/env python3
"""
Debug script to diagnose video generation issues
Checks ComfyUI connectivity, model loading, and workflow execution
"""

import requests
import json
import time
import sys
from pathlib import Path
from app.utils.comfyui_client import ComfyUIClient
from app.utils.logger import get_logger

logger = get_logger("DebugGeneration")

def check_comfyui_health():
    """Check if ComfyUI server is running"""
    logger.info("=" * 60)
    logger.info("1. CHECKING COMFYUI SERVER")
    logger.info("=" * 60)
    
    client = ComfyUIClient()
    is_healthy = client.check_server_health()
    
    if is_healthy:
        logger.info("✓ ComfyUI server is RUNNING at http://127.0.0.1:8188")
        return True
    else:
        logger.error("✗ ComfyUI server is NOT responding!")
        logger.error("   Make sure you ran: python /content/ComfyUI/main.py")
        logger.error("   Or: cd /content/ComfyUI && python -m main")
        return False

def check_model_paths():
    """Check if model files exist"""
    logger.info("\n" + "=" * 60)
    logger.info("2. CHECKING MODEL PATHS")
    logger.info("=" * 60)
    
    # Check both possible locations
    locations = [
        Path("/content/drive/MyDrive/AI/models"),
        Path("./models"),
        Path("./ComfyUI/models"),
    ]
    
    found_models = False
    for loc in locations:
        if loc.exists():
            logger.info(f"✓ Found models directory: {loc}")
            
            # Check for specific models
            models_to_find = {
                "checkpoints/realisticVisionV60B1_v60B1VAE.safetensors": "Checkpoint",
                "checkpoints/v1-5-pruned-emaonly.safetensors": "Checkpoint", 
                "animatediff/mm_sd_v15_v2.ckpt": "AnimateDiff",
                "vae/vae-ft-mse-840000-ema-pruned.safetensors": "VAE",
            }
            
            for model_path, model_type in models_to_find.items():
                full_path = loc / model_path
                if full_path.exists():
                    size_gb = full_path.stat().st_size / (1024**3)
                    logger.info(f"  ✓ {model_type}: {model_path} ({size_gb:.2f}GB)")
                    found_models = True
                else:
                    logger.warning(f"  ✗ Missing {model_type}: {model_path}")
    
    if not found_models:
        logger.error("✗ No models found in any location!")
        logger.error("   Check that you copied models to Colab in Cell 5")
        
    return found_models

def test_simple_workflow():
    """Test a simple workflow with ComfyUI"""
    logger.info("\n" + "=" * 60)
    logger.info("3. TESTING SIMPLE WORKFLOW")
    logger.info("=" * 60)
    
    client = ComfyUIClient()
    
    if not client.check_server_health():
        logger.error("✗ Cannot test - ComfyUI not responding")
        return False
    
    # Create a very simple workflow - just loading a checkpoint
    workflow = {
        "1": {
            "inputs": {
                "ckpt_name": "realisticVisionV60B1_v60B1VAE.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"},
        }
    }
    
    logger.info("Queueing test workflow...")
    prompt_id = client.queue_prompt(workflow)
    
    if not prompt_id:
        logger.error("✗ Failed to queue workflow")
        return False
    
    logger.info(f"✓ Workflow queued with ID: {prompt_id}")
    logger.info("  Waiting for completion (max 60 seconds)...")
    
    start = time.time()
    while time.time() - start < 60:
        history = client.get_history(prompt_id)
        if history and prompt_id in history:
            logger.info("✓ Workflow completed successfully!")
            return True
        time.sleep(2)
    
    logger.error("✗ Workflow did not complete within 60 seconds")
    return False

def check_output_directories():
    """Check if output directories are accessible"""
    logger.info("\n" + "=" * 60)
    logger.info("4. CHECKING OUTPUT DIRECTORIES")
    logger.info("=" * 60)
    
    output_dirs = [
        Path("/content/ComfyUI/output"),
        Path("./ComfyUI/output"),
        Path("./outputs"),
        Path("./DirectorAI_outputs"),
    ]
    
    found = False
    for out_dir in output_dirs:
        if out_dir.exists():
            logger.info(f"✓ Found output directory: {out_dir}")
            files = list(out_dir.glob("**/*"))
            if files:
                logger.info(f"  Contains {len(files)} items:")
                for f in files[:5]:  # Show first 5
                    logger.info(f"    - {f.name}")
            else:
                logger.info(f"  (empty)")
            found = True
    
    if not found:
        logger.error("✗ No output directories found")
        logger.error("  ComfyUI should save outputs to /content/ComfyUI/output")
    
    return found

def check_recent_logs():
    """Check for error messages in recent operations"""
    logger.info("\n" + "=" * 60)
    logger.info("5. CHECKING BATCH QUEUE STATUS")
    logger.info("=" * 60)
    
    queue_file = Path("queue.json")
    if queue_file.exists():
        with open(queue_file) as f:
            queue_data = json.load(f)
        
        jobs = queue_data.get("jobs", [])
        if jobs:
            logger.info(f"Found {len(jobs)} jobs in queue:")
            for job in jobs[-3:]:  # Last 3 jobs
                logger.info(f"\n  Job {job['job_id']}: {job['status']}")
                logger.info(f"    Idea: {job['idea'][:50]}...")
                if job.get('error'):
                    logger.error(f"    Error: {job['error']}")
                logger.info(f"    Timestamps: {job['timestamps']}")
        else:
            logger.info("Queue is empty")
    else:
        logger.warning("No queue.json found - no jobs have been processed yet")

def main():
    """Run all diagnostics"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " DIRECTORAI VIDEO GENERATION DEBUG".center(58) + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    results = {
        "ComfyUI Health": check_comfyui_health(),
        "Model Paths": check_model_paths(),
        "Output Directories": check_output_directories(),
    }
    
    check_recent_logs()
    
    # Only test workflow if ComfyUI is healthy
    if results["ComfyUI Health"]:
        results["Workflow Test"] = test_simple_workflow()
    
    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {check}")
    
    # Recommendations
    logger.info("\n" + "=" * 60)
    logger.info("NEXT STEPS")
    logger.info("=" * 60)
    
    if not results["ComfyUI Health"]:
        logger.error("Priority 1: Start ComfyUI server")
        logger.error("  In a Colab cell, run:")
        logger.error("  %cd /content/ComfyUI")
        logger.error("  !python main.py --listen 127.0.0.1")
        logger.error("  (IMPORTANT: Keep this cell running during generation!)")
    
    if not results["Model Paths"]:
        logger.error("Priority 2: Copy models to Colab")
        logger.error("  Run Cell 5 in EXECUTION_STEPS.md")
    
    if results["ComfyUI Health"] and results["Model Paths"]:
        if results["Workflow Test"]:
            logger.info("✓ Everything looks good!")
            logger.info("  Try running: python main.py --mode single --ideas-file test_prompts.json")
        else:
            logger.error("Workflow test failed - check ComfyUI logs for errors")
    
    logger.info("\nDebug diagnostics complete.\n")

if __name__ == "__main__":
    main()
