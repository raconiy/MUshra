#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import fnmatch
import math
import os
import random
import shutil
import subprocess


def find_files(root_dir, query="*.wav", include_root_dir=True):
    """Find files recursively.

    Args:
        root_dir (str): Root root_dir to find.
        query (str): Query to find.
        include_root_dir (bool): If False, root_dir name is not included.

    Returns:
        list: List of found filenames.

    """
    files = []
    for root, dirnames, filenames in os.walk(root_dir, followlinks=True):
        for filename in fnmatch.filter(filenames, query):
            files.append(os.path.join(root, filename))
    if not include_root_dir:
        files = [file_.replace(root_dir + "/", "") for file_ in files]

    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--beep_wav", default="configs/resources/beep_stereo_pad_8khz.wav", type=str)
    parser.add_argument("--seed", default=777, type=int)
    parser.add_argument("--gt_wavdir", type=str, required=True)
    parser.add_argument("--conv_wavdirs", nargs="+", type=str, required=True)
    parser.add_argument("--root_outdir", type=str, required=True)
    args = parser.parse_args()

    # We assume that <root_wav_dir>/<model_or_method_name_dir>/<wav_files>
    gt_wavdir = args.gt_wavdir
    root_outdir = args.root_outdir
    beep_wav = args.beep_wav
    conv_wavdirs = args.conv_wavdirs

    for conv_wavdir in conv_wavdirs:
        outdir = f"{root_outdir}/{os.path.basename(conv_wavdir)}"
        conv_wav_filenames = sorted(find_files(conv_wavdir))
        gt_wav_filenames = sorted(find_files(gt_wavdir))

        os.makedirs(outdir, exist_ok=True)
        for gt_wav, conv_wav in zip(gt_wav_filenames, conv_wav_filenames):
            command = f"sox {gt_wav} {beep_wav} {conv_wav} {outdir}/{os.path.basename(conv_wav)}".split()
            subprocess.check_call(command)


if __name__ == "__main__":
    main()
