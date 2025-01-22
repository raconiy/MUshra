#!/bin/bash

rootdir=$1
outdir=$2
normdir=$3

# check arguments
if [ $# != 3 ]; then
    echo "Usage: $0 <monorual_audio_root_dir> <output_dir> <norm_dir>"
    exit 1
fi

set -euo pipefail

# normalization
find "${rootdir}" -name "*.wav" | while read -r wavfile; do
    echo "${wavfile}"
    outwavfile=$(echo "${wavfile}" | sed -e "s;${rootdir};${normdir};g")
    dir=$(dirname "${outwavfile}")
    [ ! -e "${dir}" ] && mkdir -p "${dir}"
    sox --norm=-1 "${wavfile}" "${outwavfile}"
done

# stereo
find "${normdir}" -name "*.wav" | while read -r wavfile; do
    echo "${wavfile}"
    outwavfile=$(echo "${wavfile}" | sed -e "s;${normdir};${outdir};g")
    dir=$(dirname "${outwavfile}")
    [ ! -e "${dir}" ] && mkdir -p "${dir}"
    sox -M "${wavfile}" "${wavfile}" -c 2 "${outwavfile}" pad 0 0.1 pad 0.1
done
