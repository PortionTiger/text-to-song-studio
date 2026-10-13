"""Stage 2 — embed the normalized prompt into the model's text space.

Loads the text encoder weights (cached on first call). Returns a
tensor of shape [1, seq_len, d_text]. Kept separate from the acoustic
generator so a future version can swap encoders without touching the
diffusion loop.
"""

from text_to_song.models.model_registry import ModelRegistry
from text_to_song.utils.errors import PipelineError


class TextEmbedder:
    name = "text_embedder"

    def __init__(self):
        self._encoder = None

    def run(self, ctx: dict) -> dict:
        norm = ctx["artifacts"].get("normalized_prompt")
        if norm is None:
            raise PipelineError("text_embedder ran before prompt_normalizer")

        if self._encoder is None:
            self._encoder = ModelRegistry.instance().text_encoder()

        emb = self._encoder.encode(norm["style"], lyrics=norm["lyrics"])
        ctx["artifacts"]["text_embedding"] = emb
        return ctx