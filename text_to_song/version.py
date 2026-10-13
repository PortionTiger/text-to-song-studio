"""Version + build metadata for text-to-song-studio.

Kept in a dedicated module so the desktop shell, the CLI, and the
update checker can all agree on one source of truth.
"""

__version__ = "0.9.4"
__build__ = "2026.02.17-rc3"
__channel__ = "beta"

# Minimum model weights revision the runtime will accept. Bumping this
# forces a re-download in the model registry instead of silently loading
# stale tensors.
MIN_WEIGHTS_REV = 20260201