"""Load a named preset from the presets dir and merge over defaults.

Presets are JSON. Unknown keys are ignored with a warning so an old
preset doesn't crash a newer build.
"""

import json
from dataclasses import replace

from text_to_song.config.paths import resolve_data_dir
from text_to_song.utils.logging_setup import get_logger

log = get_logger(__name__)


def load_preset(name: str, *, base):
    path = resolve_data_dir() / "presets" / f"{name}.json"
    if not path.exists():
        log.warning("preset %s not found, using defaults", name)
        return base

    raw = json.loads(path.read_text(encoding="utf-8"))
    render = replace(base.render, **{
        k: v for k, v in raw.get("render", {}).items()
        if hasattr(base.render, k)
    })
    model = replace(base.model, **{
        k: v for k, v in raw.get("model", {}).items()
        if hasattr(base.model, k)
    })
    return replace(base, render=render, model=model)