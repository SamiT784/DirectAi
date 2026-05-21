"""
Queue System - Manages batch processing of historical shorts
Handles queueing, prioritization, and error recovery
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum
from pathlib import Path
from datetime import datetime


class JobStatus(Enum):
    """Job status enumeration"""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Job:
    """Represents a single short generation job"""

    job_id: int
    idea: str
    status: str = JobStatus.QUEUED.value
    created_at: str = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    output_path: Optional[str] = None
    retries: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class BatchQueue:
    """Manages batch processing queue"""

    def __init__(self, queue_file: Path = None):
        self.queue_file = queue_file or Path("queue.json")
        self.jobs: List[Job] = []
        self._load_queue()

    def add_job(self, idea: str) -> Job:
        """Add new job to queue"""
        job_id = max([j.job_id for j in self.jobs], default=0) + 1
        job = Job(job_id=job_id, idea=idea)
        self.jobs.append(job)
        self._save_queue()
        return job

    def add_batch_ideas(self, ideas: List[str]) -> List[Job]:
        """Add multiple ideas at once"""
        jobs = []
        for idea in ideas:
            jobs.append(self.add_job(idea))
        return jobs

    def get_next_job(self) -> Optional[Job]:
        """Get next queued job"""
        for job in self.jobs:
            if job.status == JobStatus.QUEUED.value:
                return job
        return None

    def update_job_status(
        self, job_id: int, status: JobStatus, error: str = None, output_path: str = None
    ) -> bool:
        """Update job status"""
        for job in self.jobs:
            if job.job_id == job_id:
                job.status = status.value
                if status == JobStatus.PROCESSING:
                    job.started_at = datetime.now().isoformat()
                elif status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                    job.completed_at = datetime.now().isoformat()
                if error:
                    job.error_message = error
                if output_path:
                    job.output_path = output_path
                self._save_queue()
                return True
        return False

    def retry_job(self, job_id: int, max_retries: int = 3) -> bool:
        """Retry failed job"""
        for job in self.jobs:
            if job.job_id == job_id and job.retries < max_retries:
                job.status = JobStatus.QUEUED.value
                job.retries += 1
                self._save_queue()
                return True
        return False

    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics"""
        stats = {
            "total": len(self.jobs),
            "queued": sum(1 for j in self.jobs if j.status == JobStatus.QUEUED.value),
            "processing": sum(1 for j in self.jobs if j.status == JobStatus.PROCESSING.value),
            "completed": sum(1 for j in self.jobs if j.status == JobStatus.COMPLETED.value),
            "failed": sum(1 for j in self.jobs if j.status == JobStatus.FAILED.value),
        }
        return stats

    def _save_queue(self) -> None:
        """Save queue to file"""
        data = {"jobs": [job.to_dict() for job in self.jobs]}
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.queue_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_queue(self) -> None:
        """Load queue from file"""
        if self.queue_file.exists():
            with open(self.queue_file, "r") as f:
                data = json.load(f)
            self.jobs = [Job(**job_data) for job_data in data.get("jobs", [])]


__all__ = ["BatchQueue", "Job", "JobStatus"]
