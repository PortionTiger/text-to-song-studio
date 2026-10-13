"""Builds the ordered stage list for the default pipeline.

Order matters: intake -> normalize -> embed -> generate -> decode ->
master -> write. Each stage is a small object with a .name and a
.run(ctx) -> ctx.
"""

from text_to_song.processors.prompt_normalizer import PromptNormalizer
from text_to_song.processors.text_embedder import TextEmbedder
from text_to_song.processors.acoustic_generator import AcousticGenerator
from text_to_song.processors.vocoder_decode import VocoderDecode
from text_to_song.drivers.mastering_driver import MasteringDriver
from text_to_song.drivers.file_writer import FileWriter


def build_default_stages():
    return [
        PromptNormalizer(),
        TextEmbedder(),
        AcousticGenerator(),
        VocoderDecode(),
        MasteringDriver(),
        FileWriter(),
    ]