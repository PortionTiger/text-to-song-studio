"""Unit tests for prompt normalization + preset loading."""

import json

from text_to_song.ingest.prompt_intake import build_prompt_job


def test_control_chars_stripped():
    job = build_prompt_job("  lofi\x00 beat  ")
    assert job.prompt == "lofi beat"


def test_shorthand_expanded(tmp_path, monkeypatch):
    monkeypatch.setenv("TTS_DATA_DIR", str(tmp_path))
    from text_to_song.processors.prompt_normalizer import PromptNormalizer

    job = build_prompt_job("dnb track")
    ctx = {"job": job, "artifacts": {}}
    PromptNormalizer().run(ctx)
    assert "drum and bass" in ctx["artifacts"]["normalized_prompt"]["style"]


def test_preset_overrides_seed(tmp_path, monkeypatch):
    monkeypatch.set