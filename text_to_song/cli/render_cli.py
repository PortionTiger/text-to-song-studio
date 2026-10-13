"""Headless render CLI.

Usage:
    python -m text_to_song --headless "lofi beat | verse one..."
    python -m text_to_song --headless --batch prompts.txt
    python -m text_to_song --headless --fetch-models
"""

import sys
from pathlib import Path

from text_to_song.handlers.batch_handler import BatchHandler
from text_to_song.handlers.render_handler import RenderHandler
from text_to_song.services.model_fetcher import ModelFetcher
from text_to_song.utils.errors import StudioError


def run_headless(argv: list[str]) -> int:
    if "--fetch-models" in argv:
        ModelFetcher().fetch_all(
            on_progress=lambda name, frac: print(f"\r{name}: {frac*100:5.1f}%", end=""),
        )
        print()
        return 0

    if "--batch" in argv:
        idx = argv.index("--batch")
        listing = Path(argv[idx + 1])
        prompts = [ln.strip() for ln in listing.read_text(encoding="utf-8").splitlines() if ln.strip()]
        results = BatchHandler().run_batch(prompts)
        for r in results:
            status = r.path or f"ERROR: {r.error}"
            print(f"{r.prompt[:40]:40} -> {status}")
        return 0 if all(r.error is None for r in results) else 1

    prompt = " ".join(a for a in argv if not a.startswith("--"))
    if not prompt:
        print("usage: python -m text_to_song --headless \"<prompt>\"", file=sys.stderr)
        return 2

    try:
        track = RenderHandler().render(prompt)
    except (StudioError, ValueError) as exc:
        print(f"render failed: {exc}", file=sys.stderr)
        return 1

    print(str(track))
    return 0