"""Probe host capabilities once at startup.

Returns a frozen RuntimeInfo so downstream stages don't re-query the
GPU / CPU every job.
"""

from dataclasses import dataclass
import platform
import shutil
import sys


@dataclass(frozen=True)
class RuntimeInfo:
    build: str
    python: str
    os: str
    gpu_backend: str  # "cuda" | "directml" | "cpu"
    vram_gb: float
    ffmpeg: bool


def probe_runtime() -> RuntimeInfo:
    gpu_backend = "cpu"
    vram_gb = 0.0

    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            gpu_backend = "cuda"
            vram_gb = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
        elif hasattr(torch, "directml"):
            gpu_backend = "directml"
    except Exception:
        pass

    return RuntimeInfo(
        build=platform.platform(),
        python=sys.version.split()[0],
        os=platform.system(),
        gpu_backend=gpu_backend,
        vram_gb=vram_gb,
        ffmpeg=shutil.which("ffmpeg") is not None,
    )