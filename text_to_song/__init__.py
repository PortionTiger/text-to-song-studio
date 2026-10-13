"""text-to-song-studio — pipeline package root.

Exposes the top-level pipeline entrypoint and version metadata for the
desktop studio. Everything below this package is organized as an
ingest -> processor -> driver pipeline so a prompt flows through
stages and lands as a rendered audio file.
"""

from text_to_song.pipeline.orchestrator import SongPipeline
from text_to_song.version import __version__, __build__

__all__ = ["SongPipeline", "__version__", "__build__"]