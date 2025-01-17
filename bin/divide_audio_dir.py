#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import fnmatch
import math
import os
import random
import shutil


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
    parser.add_argument("--seed", default=777, type=int)
    parser.add_argument("--num_wavs_in_each_subset", default=5, type=int)
    parser.add_argument("root_wav_dir", type=str)
    parser.add_argument("outdir", type=str)
    args = parser.parse_args()

    # We assume that <root_wav_dir>/<model_or_method_name_dir>/<wav_files>
    # E.g.
    #   root_wav_dir = "configs/resources/samples_stereo"
    #   outdir = "configs/resources/samples_stereo_subset"
    seed = args.seed
    num_wavs_in_each_subset = args.num_wavs_in_each_subset
    outdir = args.outdir
    root_wav_dir = args.root_wav_dir

    wav_filenames = sorted(find_files(root_wav_dir, include_root_dir=False))
    model_dirs = sorted(list(set([os.path.dirname(f) for f in wav_filenames])))

    # check all models have the same number of utterances
    prev_num_model_wavs = None
    wav_filename_dict = {}
    for model in model_dirs:
        wav_filename_dict[model] = sorted([f for f in wav_filenames if f"{model}" == os.path.dirname(f)])
        num_model_wavs = len(wav_filename_dict[model])
        print(f"{model} has {num_model_wavs} wav files.")
        if prev_num_model_wavs is not None:
            assert prev_num_model_wavs == num_model_wavs, "{model} has different number of wavfiles."
        prev_num_model_wavs = num_model_wavs

    # make each subset
    offset = 0
    idxs = list(range(num_model_wavs))
    random.seed(seed)
    random.shuffle(idxs)
    num_subsets = math.ceil(num_model_wavs / num_wavs_in_each_subset)
    for i in range(num_subsets):
        print(f"making subset {i}...")
        subset_outdir = f"{outdir}/subset_{i}"
        for model, wavs in wav_filename_dict.items():
            subset_wavs = [wavs[j] for j in idxs[offset: offset + num_wavs_in_each_subset]]
            subset_model_outdir = f"{subset_outdir}/{model}"
            os.makedirs(subset_model_outdir, exist_ok=True)
            for wav in subset_wavs:
                shutil.copy(f"{root_wav_dir}/{wav}", subset_model_outdir)
        offset += num_wavs_in_each_subset

    print("successfully finshed making subsets.")


if __name__ == "__main__":
    main()
