"""Stage 6 — write the mastered waveform to disk.

Output path: <renders>/<job_id>.wav. Uses soundfile when available,
falls back to the stdlib wave module so a bare Python install can still
produce a file.
"""

from pathlib import Path

from text_to_song.config.paths import render_output_dir
from text_to_song.models.rendered_track import RenderedTrack
from text_to_song.utils.errors import PipelineError


class FileWriter:
    name = "file_writer"

    def run(self, ctx: dict) -> dict:
        audio = ctx["artifacts"].get("mastered")
        if audio is None:
            raise PipelineError("file_writer needs mastered audio")

        job = ctx["job"]
        out = render_output_dir() / f"{job.job_id}.wav"
        sr = job.settings.render.sample_rate

        try:
            import soundfile as sf

            sf.write(str(out), audio, sr)
        except ImportError:
            self._write_stdlib(out, audio, sr)

        ctx["artifacts"]["rendered_track"] = RenderedTrack(
            job_id=job.job_id,
            path=out,
            sample_rate=sr,
            duration_s=job.settings.render.duration_s,
            prompt=job.prompt,
        )
        return ctx

    @staticmethod
    def _write_stdlib(path: Path, audio, sr: int) -> None:
        import wave

        import numpy as np

        pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype("<i2")
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1 if pcm.ndim == 1 else pcm.shape[1])
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(pcm.tobytes())