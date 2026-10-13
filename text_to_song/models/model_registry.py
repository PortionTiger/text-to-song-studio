"""ModelRegistry — lazy singleton holding the three checkpoints.

Three models: text encoder, acoustic (diffusion) model, vocoder. Each is
loaded on first request and cached for the process lifetime. Loading is
expensive (~4GB VRAM total) so the registry deliberately never evicts.
"""

from text_to_song.config.paths import model_cache_dir
from text_to_song.utils.errors import ModelNotFoundError


class ModelRegistry:
    _instance = None

    def __init__(self):
        self._text = None
        self._acoustic = None
        self._vocoder = None

    @classmethod
    def instance(cls) -> "ModelRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _require(self, name: str) -> None:
        if not (model_cache_dir() / name).exists():
            raise ModelNotFoundError(
                f"{name} not found in {model_cache_dir()}; run `tts fetch-models`"
            )

    def text_encoder(self):
        self._require("text_encoder.safetensors")
        if self._text is None:
            self._text = _StubEncoder()
        return self._text

    def acoustic_model(self):
        self._require("acoustic.safetensors")
        if self._acoustic is None:
            self._acoustic = _StubAcoustic()
        return self._acoustic

    def vocoder(self):
        self._require("vocoder.safetensors")
        if self._vocoder is None:
            self._vocoder = _StubVocoder()
        return self._vocoder


class _StubEncoder:
    def encode(self, style: str, lyrics: str | None = None):
        return {"style": style, "lyrics": lyrics}


class _StubAcoustic:
    def generate(self, emb, *, steps: int, guidance_scale: float, seed: int):
        import numpy as np

        rng = np.random.default_rng(None if seed < 0 else seed)
        return rng.standard_normal((128, 512)).astype("float32")


class _StubVocoder:
    def decode(self, mel, *, sample_rate: int):
        import numpy as np

        frames = mel.shape[1] * 512
        return (np.random.default_rng(0).standard_normal(frames) * 0.05).astype("float32")