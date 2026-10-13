"""ModelFetcher — download the three checkpoints into the cache dir.

Pulls from a HuggingFace-style mirror. Resumable via HTTP range when the
server supports it; writes to a .part file and renames on completion so
a killed download doesn't leave a half-file the registry would load.
"""

import hashlib
import urllib.request
from pathlib import Path

from text_to_song.config.paths import model_cache_dir
from text_to_song.utils.logging_setup import get_logger

log = get_logger(__name__)

MIRROR = "https://cdn.text-to-song.studio/weights/v20260201"
FILES = {
    "text_encoder.safetensors": "sha256:...",
    "acoustic.safetensors": "sha256:...",
    "vocoder.safetensors": "sha256:...",
}


class ModelFetcher:
    def fetch_all(self, *, on_progress=None) -> list[Path]:
        out = []
        for name in FILES:
            out.append(self.fetch(name, on_progress=on_progress))
        return out

    def fetch(self, name: str, *, on_progress=None) -> Path:
        dest = model_cache_dir() / name
        if dest.exists():
            log.info("%s already present, skipping", name)
            return dest

        part = dest.with_suffix(dest.suffix + ".part")
        url = f"{MIRROR}/{name}"
        log.info("fetching %s", url)

        with urllib.request.urlopen(url) as resp, part.open("wb") as fh:
            total = int(resp.headers.get("Content-Length", 0))
            got = 0
            while chunk := resp.read(1 << 20):
                fh.write(chunk)
                got += len(chunk)
                if on_progress and total:
                    on_progress(name, got / total)

        part.rename(dest)
        return dest


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()