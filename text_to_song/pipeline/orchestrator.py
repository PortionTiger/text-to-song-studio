"""SongPipeline — runs a prompt through ingest -> process -> render.

Inputs: a PromptJob (see models.prompt_job). Outputs: a RenderedTrack
with the final file path. Raises PipelineError on any stage failure and
cleans up intermediates unless keep_intermediates is set.

Concurrency: one SongPipeline instance per worker thread. The model
handles inside are NOT thread-safe; callers must not share an instance
across threads.
"""

from __future__ import annotations

from text_to_song.ingest.prompt_intake import build_prompt_job
from text_to_song.models.prompt_job import PromptJob
from text_to_song.models.rendered_track import RenderedTrack
from text_to_song.pipeline.stage_registry import build_default_stages
from text_to_song.utils.errors import PipelineError
from text_to_song.utils.logging_setup import get_logger

log = get_logger(__name__)


class SongPipeline:
    def __init__(self, settings=None, keep_intermediates: bool = False):
        self.settings = settings
        self.keep_intermediates = keep_intermediates
        self._stages = build_default_stages()

    def run(self, raw_prompt: str, *, preset: str | None = None) -> RenderedTrack:
        job: PromptJob = build_prompt_job(raw_prompt, preset=preset, settings=self.settings)
        log.info("pipeline start job=%s stages=%d", job.job_id, len(self._stages))

        ctx = {"job": job, "artifacts": {}}
        try:
            for stage in self._stages:
                log.debug("stage=%s", stage.name)
                ctx = stage.run(ctx)
        except PipelineError:
            raise
        except Exception as exc:  # wrap unknown stage faults
            raise PipelineError(f"stage failure: {exc}") from exc

        track: RenderedTrack = ctx["artifacts"]["rendered_track"]
        if not self.keep_intermediates:
            self._cleanup(ctx)
        return track

    def _cleanup(self, ctx: dict) -> None:
        for path in ctx["artifacts"].get("intermediates", []):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                log.warning("could not remove intermediate %s", path)