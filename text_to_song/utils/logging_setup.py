"""Central logging config. One call at process start, then get_logger."""

import logging
import sys

from text_to_song.config.paths import resolve_data_dir

_configured = False


def configure_logging(*, headless: bool = False, level: int = logging.INFO) -> None:
    global _configured
    if _configured:
        return
    log_file = resolve_data_dir() / "logs" / "studio.log"
    handlers: list[logging.Handler] = [logging.FileHandler(log_file, encoding="utf-8")]
    if not headless:
        handlers.append(logging.StreamHandler(sys.stderr))
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=handlers,
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)