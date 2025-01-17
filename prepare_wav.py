# Jiang Wenbin, 2023.02.05
import numpy as np
import shutil
from pathlib import Path
from omegaconf import OmegaConf
import soundfile as sf

def prepare_wav(conf):
    id_list = ['p257_235', 'p232_084', 'p232_072', 'p257_395', 'p257_074', 
               'p257_050', 'p232_390', 'p232_048', 'p232_044', 'p232_275', 
               'p232_316', 'p232_076', 'p257_038', 'p257_062', 'p232_414', 
               'p257_255', 'p232_174', 'p232_399']
    assert len(id_list) > conf.n_wav
    ref_root = Path(conf.wav_dir).joinpath(conf.get('ref_wav', 'clean'))
    wav_id_list = id_list[:conf.n_wav]
    for sub_dir in Path(conf.wav_dir).iterdir():
        out_path = Path(conf.out_dir).joinpath(sub_dir.stem)
        out_path.mkdir(parents=True, exist_ok=True)
        for wav_id in wav_id_list:
            wav_path = sub_dir.joinpath(f"{wav_id}.wav")
            dest_path = out_path.joinpath(f"{wav_id}.wav")
            ref_path = ref_root.joinpath(f"{wav_id}.wav")
            ref_info = sf.info(ref_path)
            wav_info = sf.info(wav_path)
            if ref_info.frames != wav_info.frames:
                print(f"{wav_path}:", ref_info.frames, wav_info.frames)
                ref_wav, fs = sf.read(ref_path)
                wav = np.zeros(len(ref_wav))                
                _wav, _ = sf.read(wav_path)
                wav[ : min(len(ref_wav),len(_wav))] = _wav[ : min(len(ref_wav),len(_wav))]
                sf.write(dest_path, wav, fs)
            else:                
                print("{} -- > {}".format(wav_path, dest_path))
                shutil.copyfile(wav_path, dest_path)

if __name__ == "__main__":
    conf = OmegaConf.create({         
         "cmd": "prepare_wav",
         "wav_dir": "../shared/wav",
         "out_dir": "./configs/resources/wavs", 
         "n_wav": 15})
    conf.merge_with_cli()    
    eval(conf.cmd)(conf)