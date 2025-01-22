# Classify wav files, align their lengths, and modify the configuration in yaml 

from pathlib import Path
import shutil
import soundfile as sf
import numpy as np
import yaml
import re

def align_audio_length(audio1_path, audio2_path):
    audio1, sample_rate = sf.read(audio1_path)
    audio2, _ = sf.read(audio2_path)

    if len(audio1) < len(audio2):
        audio2 = audio2[:len(audio1)]
    elif len(audio1) > len(audio2):
        audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)), mode='constant')

    sf.write(audio2_path, audio2, sample_rate)
    # print(f"对齐完成并已保存到原文件中: {audio2_path}")

# classify
wav_folder = Path("/mnt/d/phpstudy_pro/WWW/webMushra/configs/resources/wavs_stereo")
idx_list = []
method_list = []
for file_path in wav_folder.joinpath('Clean').glob('*.wav'):
    idx_list.append(file_path.stem)

for method_path in wav_folder.glob('*'):
    if method_path.is_dir() and method_path.name not in idx_list:
        method_list.append(method_path.name)
    
# for i, wav_idx in enumerate(idx_list):
#     wav_class = wav_folder.joinpath(wav_idx)
#     wav_class.mkdir(parents=True, exist_ok=True)
#     for method in method_list:
#         shutil.copyfile(wav_folder.joinpath(method, wav_idx).with_suffix('.wav'), wav_class.joinpath(f"{wav_idx}_{method}.wav"))
#     print(f"第{i+1}条: {wav_class.name}所有样本已根据处理方法分类完毕")

# print("\n======================== 分 类 完 毕 =============================\n\n")

# align
class_list = []
for wav_idx in idx_list:
    class_list.append(wav_folder.joinpath(wav_idx))
for i, wav_class in enumerate(class_list):
    for wav in wav_class.glob('*.wav'):
        align_audio_length(wav_class.joinpath(f"{wav_class.name}_Clean.wav"), wav)
    print(f"第{i+1}条: {wav_class.name}所有样本已参照Clean样本对齐完毕")

print("\n======================== 长 度 对 齐 完 毕 =============================\n\n")

# # yaml
# print("生成yaml文件中...")
# shutil.copyfile('example.yaml', 'MOS_IterSE.yaml')
# yaml_path = Path('/mnt/d/phpstudy_pro/WWW/webMushra/configs') / 'MOS_IterSE.yaml'

# with open(yaml_path, 'r', encoding='UTF-8') as f:
#     yaml_data = yaml.safe_load(f)

# single_test = yaml_data['pages'][3][1]

# n_sample = len(idx_list)
# method_list.remove('Clean')
# for i, idx in enumerate(idx_list):
#     single_test_copy = single_test.copy()
#     # id: clean_p232_003
#     single_test_copy['id'] = f"clean_{idx}"

#     # name: 语音增强质量评测 (2/10)
#     single_test_copy['name'] = f"语音增强质量评测 ({i+1}/{n_sample})"

#     # reference: ./configs/resources/samples/p232_001/mono_ref.wav
#     single_test_copy['reference'] = f"./configs/resources/IterSE_samples/{idx}/{idx}_Clean.wav"

#     # stimuli:
#     #   d2former: ./configs/resources/samples/p232_003/mono_c1.wav
#     #   dccrn: ./configs/resources/samples/p232_003/mono_c2.wav
#     #   dprnn: ./configs/resources/samples/p232_003/mono_c3.wav
#     #   metric+: ./configs/resources/samples/p232_003/mono_c4.wav
#     #   mpset: ./configs/resources/samples/p232_003/mono_c5.wav
#     single_test_copy['stimuli'] = {}
#     for method in method_list:
#         single_test_copy['stimuli'][method] = f"./configs/resources/IterSE_samples/{idx}/{idx}_{method}.wav"
#     if i==0:
#         yaml_data['pages'][3][1] = single_test_copy
#     else:
#         yaml_data['pages'][3].append(single_test_copy)

# with open(yaml_path, "w", encoding="utf-8") as f:
#     yaml.safe_dump(yaml_data, f, allow_unicode=True, default_flow_style=False)
#     print("yaml文件已创建完毕")
