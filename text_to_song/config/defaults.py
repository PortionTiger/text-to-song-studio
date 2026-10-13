"""Default render + model settings.

These are the values a fresh install gets. User presets layer over the
top; anything not present in a preset falls back here.
"""

from dataclasses import dataclass, field


@dataclass
class RenderSettings:
    sample_rate: int = 44100
    channels: int = 2
    bit_depth: int = 16
    duration_s: float = 30.0
    seed: int = -1
    tempo_bpm: int = 0  # 0 = let the model infer from the prompt
    key: str = "auto"
    output_format: str = "wav"


@dataclass
class ModelSettings:
    weights_rev: int = 20260201
    device: str = "auto"
    precision: str = "fp16"
    guidance_scale: float = 3.5
    steps: int = 48


@dataclass
class StudioSettings:
    render: RenderSettings = field(default_factory=RenderSettings)
    model: ModelSettings = field(default_factory=ModelSettings)
    autosave_presets: bool = True
    keep_intermediates: bool = False


DEFAULT_SETTINGS = StudioSettings()