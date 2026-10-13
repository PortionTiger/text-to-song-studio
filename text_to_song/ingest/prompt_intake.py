"""Normalize raw prompt text + preset into a PromptJob.

Handles: stripping control chars, collapsing whitespace, applying a
preset's overrides, and stamping a job id. Rejects empty prompts with
a ValueError the CLI converts to exit code 2.
"""

import re
import uuid

from text_to_song.config.defaults import DEFAULT_SETTINGS
from text_to_song.ingest.preset_loader import load_preset
from text_to_song.models.prompt_job import PromptJob

_WS = re.compile(r"\s+")
_CTRL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def build_prompt_job(raw_prompt: str, *, preset: str | None = None, settings=None) -> PromptJob:
    cleaned = _CTRL.sub("", raw_prompt or "")
    cleaned = _WS.sub(" ", cleaned).strip()
    if not cleaned:
        raise ValueError("prompt is empty after normalization")

    merged = settings or DEFAULT_SETTINGS
    if preset:
        merged = load_preset(preset, base=merged)

    return PromptJob(
        job_id=uuid.uuid4().hex[:12],
        prompt=cleaned,
        preset=preset,
        settings=merged,
    )