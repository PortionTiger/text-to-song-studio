"""RenderedTrack — the final output descriptor returned to callers."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class RenderedTrack:
    job_id: str
    path: Path
    sample_rate: int
    duration_s: float
    prompt: str

    def __str__(self) -> str:
        return f"{self.path} ({self.duration_s:.1f}s @ {self.sample_rate}Hz)"