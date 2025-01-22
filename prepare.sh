#!/bin/bash

###################################
# Prepare configs for CHiME4 data #
###################################

# Since webMUSHRA needs stereo audio, we convert the monaural audio to stereo.
# if [ ! -L configs/resources/wavs ]; then
#     ln -s "$(realpath ../wavs)" configs/resources/wavs
# fi
./bin/convert_mono_to_stereo.sh configs/resources/wavs/ configs/resources/wavs_stereo/ configs/resources/wavs_norm/


# Generate config
./bin/generate_enh_config.py \
    --sample_audio_path configs/resources/wavs_stereo/Clean/p232_040.wav \
    --seed 777 \
    --language cn \
    --metrics OVL-MOS,SIG-MOS,BAK-MOS \
    --random True \
    --ref_root_wav_dir configs/resources/wavs_stereo/Clean \
    --test_root_wav_dir configs/resources/wavs_stereo/{Noisy,DCCRN,IDR,IterSE,Noise2Noise,NyTT,OMLSA} \
    --outpath ./configs/IterSE_enh_quality_MOS_sample.yaml

echo "Run the following command to launch WebMUSHRA:"
echo -e "   php -S 0.0.0.0:60000\n"
echo "Then you can lauch the evaluation by visiting localhost:60000/?config=enh_quality_MOS_sample.yaml"
