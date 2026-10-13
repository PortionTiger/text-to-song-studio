"""Exception hierarchy for the studio.

PipelineError wraps any stage fault. ModelNotFoundError is raised by the
registry when a checkpoint is missing and the user hasn't fetched yet.
"""


class StudioError(Exception):
    """Base for all studio-raised errors."""


class PipelineError(StudioError):
    """A pipeline stage failed."""


class ModelNotFoundError(StudioError):
    """A required checkpoint is not present in the cache dir."""