import soundfile as sf
import os
import fnmatch
import random
from pathlib import Path
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

test_root_wav_dir = ['configs/resources/wavs_stereo/voicebank', 'configs/resources/wavs_stereo/demucs_voicebank', 'configs/resources/wavs_stereo/metricgan-plus_voicebank', 'configs/resources/wavs_stereo/DCCRN_voicebank', 'configs/resources/wavs_stereo/FRCRN_voicebank', 'configs/resources/wavs_stereo/DB-AIAT_voicebank', 'configs/resources/wavs_stereo/TripleSE_TNet_5c1_voicebank']

wav_path_list = sorted(find_files('configs/resources/wavs_stereo/clean'))
ref_wavs = {Path(p).stem: p for p in wav_path_list}
uttids = ref_wavs.keys()
for utid in uttids:
      length = sf.info(os.path.join('configs/resources/wavs_stereo/clean', utid+'.wav')).duration
      for subset in test_root_wav_dir[1:]:
            if length != sf.info(os.path.join(subset, utid+'.wav')).duration:
                  print( sf.info(os.path.join(subset, utid+'.wav')), length)