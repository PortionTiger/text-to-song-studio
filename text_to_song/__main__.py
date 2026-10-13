"""Console entrypoint: `python -m text_to_song`.

Boots the desktop shell when a display is available, otherwise falls
back to the headless render CLI so the same package works on a build
box.
"""

import sys

from text_to_song.bootstrap.launcher import launch
from text_to_song.utils.logging_setup import configure_logging


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    configure_logging(headless="--headless" in argv)
    return launch(argv)


if __name__ == "__main__":
    raise SystemExit(main())