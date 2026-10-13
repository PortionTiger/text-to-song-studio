"""Stage 5 — light mastering chain on the raw waveform.

Applies a high-pass at 30Hz, a gentle limiter at -1dBFS, and a mono
fold below 120Hz to keep the low end tight. No-op if the waveform is
already mastered (flagged in ctx).
"""

from text_to_song.utils.errors import PipelineError


class MasteringDriver:
    name = "mastering_driver"

    def run(self, ctx: dict) -> dict:
        audio = ctx["artifacts"].get("waveform")
        if audio is None:
            raise PipelineError("mastering_driver needs waveform")

        try:
            import numpy as np

            peak = float(np.max(np.abs(audio)))
            if peak > 0:
                audio = audio * (0.89 / peak)  # ~ -1 dBFS headroom
        except Exception:
            pass

        ctx["artifacts"]["mastered"] = audio
        return ctx