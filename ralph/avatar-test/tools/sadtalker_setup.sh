#!/usr/bin/env bash
# SadTalker (OpenTalker, Apache-2.0; its LICENSE lists no restricted third-party parts; the v0.0.2-rc models no longer
# need BFM) on CPU: animates ONE photo from audio, for RAM's free photo-only route (Ralph OK 2026-10-29).
# Shares the MuseTalk venv to save disk (run musetalk_setup.sh first). 256 px model only, no GFPGAN enhancer.
# Usage: bash sadtalker_setup.sh -> SADTALKER_SETUP_OK
set -euo pipefail
R=/root/.ram-tools/sadtalker; COMMIT=cd4c046; P=/root/.ram-tools/musetalk/venv/bin/python; export UV_NO_CACHE=1
mkdir -p $R && cd $R
[ -d src ] || git clone -q https://github.com/OpenTalker/SadTalker src
git -C src fetch -q --depth 50 origin main 2>/dev/null || true; git -C src checkout -q $COMMIT
uv pip install -q -p $P --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match torch==2.0.1+cpu torchvision==0.15.2+cpu face_alignment==1.3.5 kornia==0.6.8 yacs==0.1.8 pydub==0.25.1 resampy==0.3.1 scikit-image==0.19.3 \
  basicsr==1.4.2 facexlib==0.3.0 gfpgan==1.3.8 av safetensors joblib==1.1.0 scipy==1.10.1
# librosa 0.10+ takes mel() arguments by keyword only (the MuseTalk venv has 0.11)
sed -i 's/librosa.filters.mel(hp.sample_rate, hp.n_fft, n_mels=hp.num_mels,/librosa.filters.mel(sr=hp.sample_rate, n_fft=hp.n_fft, n_mels=hp.num_mels,/' src/src/utils/audio.py
# torchvision 0.15 moved functional_tensor; basicsr still imports the old path
F=$($P -c "import basicsr,os;print(os.path.dirname(basicsr.__file__))")/data/degradations.py
sed -i 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/' $F
cd src; mkdir -p checkpoints
B=https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc
for f in mapping_00109-model.pth.tar mapping_00229-model.pth.tar SadTalker_V0.0.2_256.safetensors; do
  [ -s checkpoints/$f ] || curl -sSL -C - --retry 3 -o checkpoints/$f $B/$f; done
du -sh $R; echo SADTALKER_SETUP_OK
