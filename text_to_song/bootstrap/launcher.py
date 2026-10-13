"""Launcher — decides desktop-shell vs headless based on argv + display.

Inputs: argv list (str). Outputs: process exit code (int).
Side effects: spawns the Qt shell or runs a one-shot render.
"""

import sys

from text_to_song.bootstrap.env_probe import probe_runtime
from text_to_song.config.paths import resolve_data_dir
from text_to_song.utils.logging_setup import get_logger

log = get_logger(__name__)


def launch(argv: list[str]) -> int:
    runtime = probe_runtime()
    data_dir = resolve_data_dir()
    log.info(
        "launch build=%s gpu=%s data_dir=%s",
        runtime.build,
        runtime.gpu_backend,
        data_dir,
    )

    if "--headless" in argv:
        from text_to_song.cli.render_cli import run_headless

        return run_headless(argv)

    try:
        from text_to_song.shell.app import run_shell
    except ImportError as exc:  # PySide6 not installed on build boxes
        log.warning("desktop shell unavailable (%s); falling back to CLI", exc)
        from text_to_song.cli.render_cli import run_headless

        return run_headless(argv)

    return run_shell(argv)