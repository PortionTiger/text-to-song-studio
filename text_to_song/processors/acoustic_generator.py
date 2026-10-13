"""Stage 3 — the diffusion loop that turns text embeddings into a mel.

Runs `steps` denoising steps at `guidance_scale`. On CUDA this is the
expensive stage (~8s for 30s of audio on a 3060). Writes the raw mel
spectrogram into ctx["artifacts"]["mel"].
"""

from text_to_song.models.model_registry import ModelRegistry
from text_to_song.utils.errors import PipelineError


class AcousticGenerator:
    name = "acoustic_generator"

    def __init__(self):
        self._model = None

    def run(self, ctx: dict) -> dict:
        emb = ctx["artifacts"].get("text_embedding")
        if emb is None:
            raise PipelineError("acoustic_generator needs text_embedding")

        settings = ctx["job"].settings.model
        if self._model is None:
            self._model = ModelRegistry.instance().acoustic_model()

        mel = self._model.generate(
            emb,
            steps=settings.steps,
            guidance_scale=settings.guidance_scale,
            seed=ctx["job"].settings.render.seed,
        )
        ctx["artifacts"]["mel"] = mel
        return ctx