import os
import numpy as np
import soundfile as sf
from pathlib import Path
import argparse

def align_audio_length(audio1_path, audio2_path):
    """
    Align the length of audio2 to match audio1 by trimming or padding.
    """
    audio1, sample_rate = sf.read(audio1_path)
    audio2, _ = sf.read(audio2_path)

    if len(audio1) < len(audio2):
        audio2 = audio2[:len(audio1)]
    elif len(audio1) > len(audio2):
        audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)), mode='constant')

    sf.write(audio2_path, audio2, sample_rate)

def align_all_wavs(clean_dir, other_dirs):
    """
    Align the length of all wav files in `other_dirs` to match the corresponding files in `clean_dir`.
    """
    clean_files = {Path(f).stem: f for f in Path(clean_dir).glob("*.wav")}

    for other_dir in other_dirs:
        print(f"Processing directory: {other_dir}")
        other_files = {Path(f).stem: f for f in Path(other_dir).glob("*.wav")}

        for filename, clean_path in clean_files.items():
            if filename in other_files:
                other_path = other_files[filename]
                print(f"Aligning {other_path} to {clean_path}")
                align_audio_length(clean_path, other_path)
            else:
                print(f"File {filename} not found in {other_dir}")

# Directories
clean_dir = "configs/resources/wavs/Clean"
other_dirs = [
    "configs/resources/wavs/DCCRN",
    "configs/resources/wavs/IDR",
    "configs/resources/wavs/IterSE",
    "configs/resources/wavs/Noise2Noise",
    "configs/resources/wavs/Noisy",
    "configs/resources/wavs/NyTT",
    "configs/resources/wavs/OMLSA"
]

# Align all wavs
align_all_wavs(clean_dir, other_dirs)
