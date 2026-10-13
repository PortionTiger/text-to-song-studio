"""Resolve per-user data directories.

On Windows: %APPDATA%/text-to-song-studio. On POSIX (build boxes):
~/.local/share/text-to-song-studio. Overridable via TTS_DATA_DIR.
"""

import os
from pathlib import Path

APP_DIRNAME = "text-to-song-studio"


def resolve_data_dir() -> Path:
    override = os.environ.get("TTS_DATA_DIR")
    if override:
        root = Path(override)
    elif os.name == "nt":
        root = Path(os.environ.get("APPDATA", Path.home())) / APP_DIRNAME
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / APP_DIRNAME

    for sub in ("models", "cache", "renders", "logs", "presets"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root


def model_cache_dir() -> Path:
    return resolve_data_dir() / "models"


def render_output_dir() -> Path:
    return resolve_data_dir() / "renders"