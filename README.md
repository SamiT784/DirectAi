# DirectorAI - Modular AI Video Generation System

A production-grade system for automatically generating historical cinematic YouTube Shorts using Python, ComfyUI, and advanced AI models.

## Features

- **Modular Architecture**: Seven independent engines for different aspects of short generation
- **Batch Processing**: Generate 20+ shorts automatically with queue management
- **Google Colab Compatible**: Runs in Google Colab with proper folder management
- **External Orchestration**: No modifications to ComfyUI core files
- **Structured Output**: Organized folders for scripts, audio, scenes, renders, and metadata
- **Error Handling**: Automatic retry logic and graceful failure handling

## Architecture

```
DirectorAI/
├── app/
│   ├── script_engine/          # Generate scripts from ideas
│   ├── prompt_engine/          # Create cinematic prompts
│   ├── narration_engine/       # Generate XTTS voice narration
│   ├── scene_engine/           # Generate images + AnimateDiff animation
│   ├── interpolation_engine/   # Smooth with RIFE
│   ├── render_engine/          # FFmpeg composition
│   ├── workflow_engine/        # ComfyUI workflow management
│   ├── utils/                  # Logging, file management
│   ├── orchestrator.py         # Main orchestration
│   └── batch_queue.py          # Batch processing queue
│
├── workflows/                  # ComfyUI workflow JSON templates
├── models/                     # Model storage
├── outputs/                    # Generated shorts (organized by ID)
├── temp/                       # Temporary processing files
├── config.py                   # System configuration
├── main.py                     # Entry point
└── requirements.txt            # Python dependencies
```

## Installation

### Prerequisites
- Python 3.9+
- ComfyUI running locally or remotely
- CUDA-capable GPU (recommended)

### Setup

```bash
# Clone the repository
cd DirectorAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Single Short Generation

```bash
python main.py --mode single --idea "The rise of Cleopatra VII, the last pharaoh of ancient Egypt"
```

### Batch Processing

Create `ideas.json`:
```json
{
  "ideas": [
    "The rise of Cleopatra VII",
    "The Battle of Thermopylae",
    "Joan of Arc and the Hundred Years' War"
  ]
}
```

Generate batch:
```bash
python main.py --mode batch --ideas-file ideas.json
```

## Modular Engines

### 1. Script Engine
- Generates cinematic historical narratives
- Splits scripts into individual scenes
- *Ready for LLM integration (OpenAI/Claude/Groq)*

### 2. Prompt Engine
- Creates detailed cinematic image prompts
- Applies historical accuracy and lighting specifications
- Prevents unwanted elements

### 3. Narration Engine
- Generates voice narration using XTTS
- Deep, cinematic male voice
- *Ready for XTTS model integration*

### 4. Scene Engine
- Generates images via ComfyUI + Stable Diffusion
- Animates with AnimateDiff
- *Ready for workflow execution*

### 5. Interpolation Engine
- Smooths video motion using RIFE
- 2x frame interpolation
- *Ready for RIFE model integration*

### 6. Render Engine
- Combines all scenes with FFmpeg
- Syncs narration and background music
- Adds transitions

### 7. Workflow Engine
- Manages ComfyUI workflow execution
- Creates and injects parameters into workflows
- Monitors execution status

## Configuration

Edit `config.py` to customize:
- Model selections
- Generation parameters (resolution, steps, FPS)
- Batch processing limits
- ComfyUI server URL
- Output structure

## Output Structure

Each generated short creates:
```
outputs/
└── short_001/
    ├── script/              # Generated script JSON
    ├── audio/               # Narration WAV files
    ├── scenes/              # Generated images per scene
    ├── renders/             # Interpolated video files
    ├── metadata/            # JSON metadata
    └── final/               # Final YouTube Short MP4
```

## Batch Queue System

The system includes a persistent queue (`queue.json`) that:
- Survives interruptions
- Tracks job status (queued, processing, completed, failed)
- Supports automatic retries
- Provides statistics

Check queue status:
```python
from app.batch_queue import BatchQueue
queue = BatchQueue()
print(queue.get_stats())
```

## Google Colab Setup

```python
# In Colab cell
!git clone https://github.com/yourusername/DirectorAI.git
%cd DirectorAI
!pip install -r requirements.txt

# Mount Google Drive for outputs
from google.colab import drive
drive.mount('/content/drive')

# Start generation
!python main.py --mode batch --ideas-file ideas.json --output-dir /content/drive/MyDrive/DirectorAI_outputs
```

## Models Used

- **Text-to-Image**: `realisticVisionV60B1_v60B1VAE.safetensors`
- **Fallback**: `v1-5-pruned-emaonly.safetensors`
- **VAE**: `vae-ft-mse-840000-ema-pruned.safetensors`

## Integration Points (Next Steps)

1. **LLM Integration** (Script Engine)
   - Replace template with actual OpenAI/Claude/Groq calls
   - Use streaming for long scripts

2. **XTTS Integration** (Narration Engine)
   - Load XTTS model
   - Generate high-quality narration

3. **ComfyUI Workflows** (Scene Engine)
   - Create Stable Diffusion workflow templates
   - Create AnimateDiff workflow templates
   - Execute via ComfyUIClient

4. **RIFE Integration** (Interpolation Engine)
   - Load RIFE model
   - Interpolate video frames

5. **FFmpeg Integration** (Render Engine)
   - Build FFmpeg command-line calls
   - Compose audio, video, transitions

## Production Considerations

- ✅ Modular design for easy testing
- ✅ Error handling and retry logic
- ✅ Logging system for debugging
- ✅ Configuration-driven parameters
- ✅ Queue persistence
- ✅ Colab compatibility
- ⏳ Model caching for efficiency
- ⏳ Webhook notifications for batch completion

## Troubleshooting

**ComfyUI not responding?**
- Ensure ComfyUI is running: `python main.py` in ComfyUI directory
- Check server URL in config.py

**Out of memory?**
- Reduce image resolution in config.py
- Lower batch size

**Generator stuck?**
- Check `queue.json` for failed jobs
- Retry manually: `queue.retry_job(job_id)`

## License

MIT

## Support

For issues and feature requests, please open an issue on GitHub.
