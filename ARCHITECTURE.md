"""
DirectorAI ARCHITECTURE GUIDE
Complete system design documentation
"""

# ============================================================================
# SYSTEM OVERVIEW
# ============================================================================

DirectorAI is a production-grade, modular AI video generation system designed to
automatically create historical cinematic YouTube Shorts from text ideas.

Key Principles:
- Modular: Each engine is independent and testable
- Scalable: Batch process 20+ shorts with queue management
- Colab-Ready: Runs in Google Colab with proper file handling
- External: No modifications to ComfyUI core
- Reliable: Error handling, retries, logging throughout


# ============================================================================
# CORE ARCHITECTURE
# ============================================================================

MAIN PIPELINE:
  Idea → Script → Scenes → Prompts → Images → Animation → Interpolation → Render → Output

MODULAR ENGINES:
1. Script Engine        (app/script_engine/)       - Generate cinematic narratives
2. Prompt Engine        (app/prompt_engine/)       - Create image generation prompts  
3. Narration Engine     (app/narration_engine/)    - Generate voice narration
4. Scene Engine         (app/scene_engine/)        - Generate & animate scenes
5. Interpolation Engine (app/interpolation_engine/)- Smooth video motion
6. Render Engine        (app/render_engine/)       - Combine into final shorts
7. Workflow Engine      (app/workflow_engine/)     - ComfyUI orchestration

ORCHESTRATION:
- DirectorAIOrchestrator: Coordinates all engines for single/batch generation
- BatchQueue: Manages job queue with persistence and retry logic


# ============================================================================
# KEY FILES STRUCTURE
# ============================================================================

DirectorAI/
├── app/
│   ├── __init__.py                 # Module exports
│   ├── base_engine.py              # Abstract base class for all engines
│   ├── orchestrator.py             # Main orchestration system
│   ├── batch_queue.py              # Batch processing queue
│   │
│   ├── script_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # ScriptEngine class
│   │
│   ├── prompt_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # PromptEngine class
│   │
│   ├── narration_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # NarrationEngine class
│   │
│   ├── scene_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # SceneEngine class
│   │
│   ├── interpolation_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # InterpolationEngine class
│   │
│   ├── render_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # RenderEngine class
│   │
│   ├── workflow_engine/
│   │   ├── __init__.py
│   │   └── engine.py               # WorkflowEngine class
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py               # Centralized logging
│       ├── file_manager.py         # File operations
│       └── comfyui_client.py       # ComfyUI API client
│
├── config.py                        # Central configuration system
├── main.py                          # CLI entry point
├── test_architecture.py             # Architecture verification
├── requirements.txt                 # Python dependencies
├── README.md                        # User documentation
├── .gitignore                       # Git ignore rules
├── .env.example                     # Environment variables template
├── example_ideas.json               # Sample ideas for testing
│
├── scripts/
│   ├── __init__.py
│   ├── colab_starter.py             # Google Colab integration
│   └── workflow_templates.py        # ComfyUI workflow templates
│
├── workflows/                       # ComfyUI workflow JSON files
├── models/                          # Model storage (symlinked to ComfyUI)
├── outputs/                         # Generated shorts
│   └── short_001/
│       ├── script/                  # Script metadata
│       ├── audio/                   # Narration WAV files
│       ├── scenes/                  # Generated scene images
│       ├── renders/                 # Interpolated video files
│       ├── metadata/                # JSON metadata
│       └── final/                   # Final YouTube Short MP4
│
├── temp/                            # Temporary processing files
└── comfyui/                         # ComfyUI symbolic link


# ============================================================================
# EXECUTION FLOW
# ============================================================================

SINGLE SHORT GENERATION:
1. orchestrator.generate_single_short(idea, short_id)
   │
   ├─→ Step 1: script_engine.process({"idea": idea})
   │   └─→ Returns: full_script, scenes[]
   │
   ├─→ For each scene:
   │   ├─→ prompt_engine.process({"scene": scene})
   │   │   └─→ Returns: positive_prompt, negative_prompt
   │   │
   │   ├─→ narration_engine.process({"text": scene.narration})
   │   │   └─→ Returns: audio_path, duration_seconds
   │   │
   │   ├─→ scene_engine.process({"prompt": prompt, ...})
   │   │   └─→ Returns: image_path, video_path
   │   │
   │   └─→ interpolation_engine.process({"video_path": ...})
   │       └─→ Returns: interpolated_video
   │
   ├─→ Step 6: render_engine.process({"scene_videos": [...], "audio_path": ...})
   │   └─→ Returns: final_video
   │
   └─→ Save metadata and outputs


BATCH GENERATION:
1. batch_queue.add_batch_ideas(ideas)
   └─→ Creates Job objects, persists to queue.json

2. For each job:
   ├─→ queue.update_job_status(PROCESSING)
   ├─→ orchestrator.generate_single_short(job.idea, job.job_id)
   ├─→ queue.update_job_status(COMPLETED/FAILED)
   └─→ Continue to next job

3. queue.get_stats() returns overall progress


# ============================================================================
# ENGINE INTERFACES
# ============================================================================

All engines inherit from BaseEngine and implement:

class BaseEngine(ABC):
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Must implement actual processing logic"""
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Optional: validate input before processing"""
        return True


# ============================================================================
# CONFIGURATION SYSTEM
# ============================================================================

config.py provides centralized access to:

- Paths: BASE_DIR, APP_DIR, OUTPUTS_DIR, TEMP_DIR, etc.
- Models: Model names, filenames, types
- Generation Parameters: Width, height, steps, guidance_scale
- ComfyUI Configuration: Server URL, websocket URL, timeout
- Batch Configuration: Max concurrent renders, max retries
- Output Structure: Folder organization

Access globally:
    from config import config
    print(config.OUTPUTS_DIR)
    print(config.MODELS['primary']['filename'])


# ============================================================================
# BATCH QUEUE SYSTEM
# ============================================================================

Persistent queue with automatic persistence to queue.json:

Job States:
- QUEUED: Waiting to process
- PROCESSING: Currently generating
- COMPLETED: Successfully generated
- FAILED: Error during generation
- SKIPPED: Manually skipped

Features:
- Survives process interruptions
- Automatic retry logic (max_retries)
- Statistics tracking
- Error message capture

Usage:
    queue = BatchQueue()
    job = queue.add_job("Historical idea")
    queue.update_job_status(job.job_id, JobStatus.PROCESSING)
    queue.update_job_status(job.job_id, JobStatus.COMPLETED, output_path="...")
    stats = queue.get_stats()


# ============================================================================
# INTEGRATION POINTS (PLACEHOLDERS)
# ============================================================================

1. LLM Integration (Script Engine)
   Location: app/script_engine/engine.py → _generate_script_template()
   TODO: Replace with OpenAI/Claude/Groq API call
   Input: Historical idea (string)
   Output: Full script with scenes

2. XTTS Integration (Narration Engine)
   Location: app/narration_engine/engine.py → _generate_placeholder_audio()
   TODO: Load XTTS model, generate speech
   Input: Text narration
   Output: WAV audio file

3. ComfyUI Workflows (Scene Engine)
   Location: app/workflow_engine/engine.py → _execute_workflow()
   TODO: Load workflow JSON, inject params, execute via API
   Workflows: scripts/workflow_templates.py
   Uses: app/utils/comfyui_client.py

4. RIFE Interpolation (Interpolation Engine)
   Location: app/interpolation_engine/engine.py → _interpolate_frames()
   TODO: Load RIFE model, interpolate video
   Input: Video file
   Output: 2x interpolated video

5. FFmpeg Rendering (Render Engine)
   Location: app/render_engine/engine.py → _compose_with_ffmpeg()
   TODO: Build FFmpeg command for scene composition
   Input: Scene videos, audio, music
   Output: Final MP4 short


# ============================================================================
# GOOGLE COLAB COMPATIBILITY
# ============================================================================

Ready for Colab with:
- Proper working directory handling
- Google Drive mounting support (scripts/colab_starter.py)
- Relative import structure
- Temporary file cleanup
- Batch processing optimization

Colab Setup:
    !git clone https://github.com/user/DirectorAI.git
    %cd DirectorAI
    !pip install -r requirements.txt
    !python scripts/colab_starter.py


# ============================================================================
# LOGGING SYSTEM
# ============================================================================

Centralized logging via app/utils/logger.py:

    from app.utils import get_logger
    logger = get_logger("ModuleName")
    logger.info("Message")
    logger.error("Error message")

Features:
- Singleton pattern (one logger per module)
- Console output with timestamps
- Optional file logging
- DEBUG, INFO, WARNING, ERROR, CRITICAL levels


# ============================================================================
# FILE MANAGEMENT
# ============================================================================

Safe file operations via app/utils/file_manager.py:

    FileManager.ensure_dir(path)           # Create directory
    FileManager.clean_dir(path)            # Empty directory
    FileManager.copy_file(src, dst)        # Copy safely
    FileManager.list_files(path)           # List directory
    FileManager.get_file_size(path)        # Check size
    FileManager.safe_remove(path)          # Delete safely


# ============================================================================
# COMFYUI INTEGRATION
# ============================================================================

ComfyUI API client via app/utils/comfyui_client.py:

    client = ComfyUIClient("http://127.0.0.1:8188")
    
    # Check health
    if client.check_server_health():
        # Queue workflow
        prompt_id = client.queue_prompt(workflow_dict)
        
        # Wait for completion
        client.wait_for_completion(prompt_id)
        
        # Get history
        history = client.get_history(prompt_id)


# ============================================================================
# DEVELOPMENT WORKFLOW
# ============================================================================

1. PHASE 1: Architecture (COMPLETE)
   ✓ Modular structure
   ✓ Base engine interface
   ✓ Configuration system
   ✓ Batch queue
   ✓ Orchestration
   ✓ Logging & utils

2. PHASE 2: Integration (TODO)
   → LLM API integration
   → XTTS model loading
   → ComfyUI workflow execution
   → RIFE interpolation
   → FFmpeg rendering

3. PHASE 3: Testing (TODO)
   → Unit tests for each engine
   → Integration tests
   → Colab testing
   → Performance optimization

4. PHASE 4: Production (TODO)
   → Model caching
   → Batch optimization
   → Webhook notifications
   → Analytics


# ============================================================================
# NEXT STEPS
# ============================================================================

1. Run: python test_architecture.py (verify system loads)

2. Implement LLM integration in ScriptEngine

3. Load XTTS model in NarrationEngine

4. Create ComfyUI workflows (JSON files in workflows/)

5. Implement ComfyUIClient calls in SceneEngine

6. Test single short generation end-to-end

7. Optimize batch processing

8. Deploy to Colab


# ============================================================================
# PRODUCTION CONSIDERATIONS
# ============================================================================

✓ Error handling throughout
✓ Logging for debugging
✓ Modular, testable code
✓ Configuration-driven
✓ Batch queue persistence
✓ Graceful failure recovery
✓ Colab compatibility

⏳ Model caching/loading optimization
⏳ Async/concurrent processing
⏳ Webhook notifications
⏳ Performance monitoring
