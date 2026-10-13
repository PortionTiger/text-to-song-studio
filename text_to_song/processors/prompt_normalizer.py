"""Stage 1 — normalize the prompt for the text encoder.

Lowercases, expands a few musical shorthands (bpm, key), and splits the
prompt into a style clause and a lyric clause when a `|` separator is
present. Output goes into ctx["artifacts"]["normalized_prompt"].
"""

from text_to_song.utils.errors import PipelineError

_SHORTHAND = {
    "lofi": "lo-fi hip hop, warm vinyl crackle",
    "dnb": "drum and bass, 174 bpm, rolling breaks",
    "synthwave": "synthwave, analog pads, gated reverb drums",
}


class PromptNormalizer:
    name = "prompt_normalizer"

    def run(self, ctx: dict) -> dict:
        job = ctx["job"]
        text = job.prompt

        style, _, lyrics = text.partition("|")
        style = style.strip().lower()
        for key, expansion in _SHORTHAND.items():
            if key in style:
                style = style.replace(key, expansion)

        if not style:
            raise PipelineError("no style clause found in prompt")

        ctx["artifacts"]["normalized_prompt"] = {
            "style": style,
            "lyrics": lyrics.strip() or None,
        }
        return ctx