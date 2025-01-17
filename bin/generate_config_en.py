#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate config with English instruction."""

import argparse
import fnmatch
import os
import random

import yaml


def response_template():
    return [
        {
            "value": 1,
            "label": "1: Bad",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 2,
            "label": "2: Poor",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 3,
            "label": "3: Fair",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 4,
            "label": "4: Good",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 5,
            "label": "5: Excellent",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
    ]


def make_page(idx, total_idx, wav_path):
    wav_dir_id = os.path.basename(os.path.dirname(wav_path))
    wav_file_id = os.path.basename(wav_path)
    wav_id = f"{wav_dir_id}_{wav_file_id}"
    return {
        "type": "likert_single_stimulus",
        "id": wav_id,
        "content": "Listen to a given sample and rate the naturalness with 5-point scale."
                   "<br>"
                   "Note that the naturalness means how the sample sound like real-human speech "
                   "and real-human speech is corresponding to 5.",
        "name": f"MOS on Naturalness ({idx}/{total_idx})",
        "mustRate": True,
        "mustPlayback": True,
        "reference": wav_path,
        "stimuli": {
            "C1": wav_path,
        },
        "response": response_template(),
    }


def make_first_page():
    return {
        "type": "generic",
        "content": "Welcome to audio naturalness evaluation."
                   "<br>"
                   "Please click [Next] button.",
        "id": "welcome",
        "name": "Audio naturalness evaluation",
    }


def make_explanation_page():
    return {
        "type": "generic",
        "content": "Listen to a given sample and rate the naturalness with 5-point scale."
                   "<br>"
                   "Note that the naturalness means how the sample sound like real-human speech "
                   "and real-human speech is corresponding to 5."
                   "<br>"
                   "After that, we provide the sample of real-human speech as a reference."
                   "<br>"
                   "<br>"
                   "<strong>DO NOT CLOSE AND RELOAD THIS PAGE UNTIL THE END OF THIS EVALUATION.</strong>"
                   "<br>"
                   "<br>"
                   "Please click [Next] button.",
        "id": "explanation",
        "name": "Explanation",
    }


def make_volume_page(sample_wav_path):
    volume_page = {
        "type": "volume",
        "content": "This is a sample of real-human speech.<br>"
                   "Listen to the sample and adjust your volume.<br>"
                   "<br>"
                   "<strong>DURING THE EVALUATION, PLEASE USE HEADPHONES AND WORK IN A QUIET ROOM.</strong>",
        "id": "Volume check",
        "stimulus": sample_wav_path,
        "defaultVolume": 1.0,
    }
    return volume_page


def make_finish_page():
    return {
        "type": "finish",
        "content": "The evaluation was finished.<br>"
                   "Please enter your <strong>WORKER ID</strong> in Amazon mechanical turk. <br>"
                   "Please click [send Results] button.",
        "id": "finish",
        "name": "Finshed evaluation",
        "popupContent": "The results were recorded. Thank you for your cooperation.",
        "showResults": False,
        "writeResults": True,
        "questionnaire": [
            {
                "type": "text",
                "label": "worker id",
                "name": "name",
                "optional": False,
            },
        ]
    }


def similarity_response_template():
    return [
        {
            "value": 1,
            "label": "1: Different (sure)",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 2,
            "label": "2: Different (not sure)",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 3,
            "label": "3: Same (not sure)",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 4,
            "label": "4: Same (sure)",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
    ]


def make_similarity_page(idx, total_idx, wav_path):
    wav_dir_id = os.path.basename(os.path.dirname(wav_path))
    wav_file_id = os.path.basename(wav_path)
    wav_id = f"{wav_dir_id}_{wav_file_id}"
    return {
        "type": "likert_single_stimulus",
        "id": wav_id,
        "content": "Listen to continuous two samples and evaluate whether the "
                   "speakers of two samples are same or not."
                   "<br>"
                   "Note that a beep sound is inserted between two samples.",
        "name": f"Speaker similarity ({idx}/{total_idx})",
        "mustRate": True,
        "mustPlayback": True,
        "reference": wav_path,
        "stimuli": {
            "C1": wav_path,
        },
        "response": similarity_response_template(),
    }


def make_similarity_first_page():
    return {
        "type": "generic",
        "content": "Next, speaker similarity evaluation."
                   "<br>"
                   "Please click [Next] button.",
        "id": "welcome",
        "name": "Speaker similarity evaluation",
    }


def make_similarity_explanation_page():
    return {
        "type": "generic",
        "content": "Listen to continuous two samples and evaluate whether the "
                   "speakers of two samples are same or not."
                   "<br>"
                   "<br>"
                   "<strong>DO NOT CLOSE AND RELOAD THIS PAGE UNTIL THE END OF THIS EVALUATION.</strong>"
                   "<br>"
                   "<br>"
                   "Please click [Next] button.",
        "id": "explanation",
        "name": "Explanation",
    }


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
    parser.add_argument("--sample_audio_path", default=None, type=str, nargs="+")
    parser.add_argument("--seed", default=777, type=int)
    parser.add_argument("--similarity_root_wav_dir", default=None, type=str)
    parser.add_argument("root_wav_dir")
    parser.add_argument("outpath")
    args = parser.parse_args()

    config = {
        "testname": "Subjective evaluation",
        "testId": "subjective_evalaution",
        "bufferSize": 2048,
        "stopOnErrors": True,
        "showButtonPreviousPage": False,
        "remoteService": "service/write.php",
        "pages": [],
    }

    wav_path_list = sorted(find_files(args.root_wav_dir))
    random.seed(args.seed)
    random.shuffle(wav_path_list)
    config["pages"] += [make_first_page()]
    config["pages"] += [make_explanation_page()]
    if args.sample_audio_path is not None:
        for sample_wav in args.sample_audio_path:
            config["pages"] += [make_volume_page(sample_wav)]
    for idx, wav_path in enumerate(wav_path_list, 1):
        config["pages"] += [make_page(idx, len(wav_path_list), wav_path)]

    if args.similarity_root_wav_dir is not None:
        wav_path_list = sorted(find_files(args.similarity_root_wav_dir))
        random.seed(args.seed)
        random.shuffle(wav_path_list)
        config["pages"] += [make_similarity_first_page()]
        config["pages"] += [make_similarity_explanation_page()]
        for idx, wav_path in enumerate(wav_path_list, 1):
            config["pages"] += [make_similarity_page(idx, len(wav_path_list), wav_path)]

    config["pages"] += [make_finish_page()]

    with open(args.outpath, "w") as f:
        yaml.safe_dump(config, f, allow_unicode=True, encoding="utf-8", line_break=True)


if __name__ == "__main__":
    main()
