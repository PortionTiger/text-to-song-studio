"""Stage 4 — decode the mel spectrogram back to a waveform.

The vocoder is a separate checkpoint from the acoustic model; loading it
here keeps the diffusion stage's memory footprint from spiking.
"""

from text_to_song.models.model_registry import ModelRegistry
from text_to_song.utils.errors import PipelineError


class VocoderDecode:
    name = "vocoder_decode"

    def __init__(self):
        self._vocoder = None

    def run(self, ctx: dict) -> dict:
        mel = ctx["artifacts"].get("mel")
        if mel is None:
            raise PipelineError("vocoder_decode needs mel")

        if self._vocoder is None:
            self._vocoder = ModelRegistry.instance().vocoder()

        audio = self._vocoder.decode(mel, sample_rate=ctx["job"].settings.render.sample_rate)
        ctx["artifacts"]["waveform"] = audio
        return ctx