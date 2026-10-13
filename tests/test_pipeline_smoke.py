"""Smoke test: a full pipeline run produces a wav file on disk.

Uses the stub models in the registry so no real checkpoints are needed.
"""

import os
import tempfile
from pathlib import Path


def test_pipeline_writes_wav(tmp_path, monkeypatch):
    monkeypatch.setenv("TTS_DATA_DIR", str(tmp_path))
    # create fake checkpoints so the registry's _require passes
    models = tmp_path / "models"
    models.mkdir(parents=True)
    for name in ("text_encoder.safetensors", "acoustic.safetensors", "vocoder.safetensors"):
        (models / name).write_bytes(b"stub")

    from text_to_song.pipeline.orchestrator import SongPipeline

    track = SongPipeline().run("lofi beat | verse one, take it slow")
    assert Path(track.path).exists()
    assert Path(track.path).suffix == ".wav"
    assert Path(track.path).stat().st_size > 0


def test_empty_prompt_rejected(tmp_path, monkeypatch):
    monkeypatch.setenv("TTS_DATA_DIR", str(tmp_path))
    from text_to_song.pipeline.orchestrator import SongPipeline

    try:
        SongPipeline().run("   ")
    except ValueError:
        return
    raise AssertionError("empty prompt should raise ValueError")