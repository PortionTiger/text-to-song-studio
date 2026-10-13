"""UpdateChecker — hit the release feed and compare to __version__.

Runs on a background thread at shell startup; never blocks the UI. The
feed is a static JSON file so the studio doesn't need a backend.
"""

import json
import urllib.request
from dataclasses import dataclass

from text_to_song.utils.logging_setup import get_logger
from text_to_song.version import __version__

log = get_logger(__name__)
FEED = "https://text-to-song.studio/releases.json"


@dataclass
class UpdateInfo:
    available: bool
    latest: str
    url: str


def check_for_update(timeout: float = 4.0) -> UpdateInfo:
    try:
        with urllib.request.urlopen(FEED, timeout=timeout) as resp:
            data = json.load(resp)
    except Exception as exc:
        log.debug("update check failed: %s", exc)
        return UpdateInfo(False, __version__, "")

    latest = data.get("latest", __version__)
    return UpdateInfo(latest != __version__, latest, data.get("url", ""))