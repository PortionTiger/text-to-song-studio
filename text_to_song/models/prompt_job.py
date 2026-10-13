"""PromptJob — the unit of work that flows through the pipeline."""

from dataclasses import dataclass, field


@dataclass
class PromptJob:
    job_id: str
    prompt: str
    preset: str | None
    settings: object  # StudioSettings; kept loose to avoid an import cycle
    artifacts: dict = field(default_factory=dict)