"""BatchHandler — render a list of prompts sequentially.

Sequential on purpose: the acoustic model holds ~4GB of VRAM and running
two jobs at once OOMs on 8GB cards. A future queue worker can swap this
for a bounded pool.
"""

from dataclasses import dataclass

from text_to_song.handlers.render_handler import RenderHandler


@dataclass
class BatchResult:
    prompt: str
    path: str | None
    error: str | None


class BatchHandler:
    def __init__(self, settings=None):
        self._render = RenderHandler(settings=settings)

    def run_batch(self, prompts: list[str], *, preset: str | None = None):
        results: list[BatchResult] = []
        for p in prompts:
            try:
                track = self._render.render(p, preset=preset)
                results.append(BatchResult(p, str(track.path), None))
            except Exception as exc:
                results.append(BatchResult(p, None, str(exc)))
        return results