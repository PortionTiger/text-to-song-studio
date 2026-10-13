"""RenderHandler — the one call the UI makes to render a song.

Wraps SongPipeline with progress callbacks so the Qt shell can update a
progress bar without touching pipeline internals.
"""

from collections.abc import Callable

from text_to_song.pipeline.orchestrator import SongPipeline
from text_to_song.utils.errors import PipelineError

ProgressCb = Callable[[str, float], None]


class RenderHandler:
    def __init__(self, settings=None):
        self._settings = settings

    def render(self, prompt: str, *, preset: str | None = None,
               on_progress: ProgressCb | None = None):
        pipe = SongPipeline(settings=self._settings)

        def _tick(name: str, frac: float) -> None:
            if on_progress:
                on_progress(name, frac)

        _tick("intake", 0.0)
        try:
            track = pipe.run(prompt, preset=preset)
        except PipelineError as exc:
            _tick(f"error: {exc}", 0.0)
            raise
        _tick("done", 1.0)
        return track