#!/usr/bin/env bash
# MuseTalk 1.5 (TMElyralab, MIT; README: code and trained models free for commercial use) on CPU, for RAM's free
# "real-video twin" route (Ralph OK 2026-10-29: "let's do 1 and 2"). Installs into /root/.ram-tools/musetalk:
# src/ (repo @ pinned commit), venv/ (Python 3.11, torch 2.0.1 CPU, mmcv 2.0.1 CPU wheel), src/models/ (V1.5 weights only).
# Skips what inference doesn't need: V1.0 weights, syncnet (training), tensorflow, gradio. Official Hugging Face, not the mirror.
# Usage: bash musetalk_setup.sh -> prints MUSETALK_SETUP_OK
set -euo pipefail
R=/root/.ram-tools/musetalk; COMMIT=0a89dec; export UV_NO_CACHE=1
mkdir -p $R && cd $R
[ -d src ] || git clone -q https://github.com/TMElyralab/MuseTalk src
git -C src fetch -q --depth 50 origin main 2>/dev/null || true; git -C src checkout -q $COMMIT
[ -x venv/bin/python ] || uv venv -q -p 3.11 venv
P=venv/bin/python
uv pip install -q -p $P torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu
uv pip install -q -p $P diffusers==0.30.2 accelerate==0.28.0 numpy==1.23.5 opencv-python==4.9.0.80 soundfile==0.12.1 \
  transformers==4.39.2 huggingface_hub==0.30.2 librosa==0.11.0 einops==0.8.1 omegaconf==2.3.0 ffmpeg-python==0.2.0 \
  moviepy==1.0.3 imageio[ffmpeg]==2.34.0 gdown==5.2.0 requests mmengine==0.10.4 "setuptools<70"
uv pip install -q -p $P mmcv==2.0.1 -f https://download.openmmlab.com/mmcv/dist/cpu/torch2.0/index.html
uv pip install -q -p $P pip && uv pip install -q -p $P --no-build-isolation chumpy==0.70   # mmpose dep; its build needs pip
uv pip install -q -p $P mmdet==3.1.0 mmpose==1.1.0
cd src; M=models; mkdir -p $M/musetalkV15 $M/dwpose $M/face-parse-bisent $M/sd-vae $M/whisper
HF="../venv/bin/huggingface-cli download"
$HF TMElyralab/MuseTalk --local-dir $M --include "musetalkV15/musetalk.json" "musetalkV15/unet.pth" >/dev/null
$HF stabilityai/sd-vae-ft-mse --local-dir $M/sd-vae --include config.json diffusion_pytorch_model.bin >/dev/null
$HF openai/whisper-tiny --local-dir $M/whisper --include config.json pytorch_model.bin preprocessor_config.json >/dev/null
$HF yzd-v/DWPose --local-dir $M/dwpose --include dw-ll_ucoco_384.pth >/dev/null
[ -s $M/face-parse-bisent/79999_iter.pth ] || ../venv/bin/gdown -q --id 154JgKpzCPW82qINcVieuPH3fZ2e0P812 -O $M/face-parse-bisent/79999_iter.pth
[ -s $M/face-parse-bisent/resnet18-5c106cde.pth ] || curl -sSL -o $M/face-parse-bisent/resnet18-5c106cde.pth https://download.pytorch.org/models/resnet18-5c106cde.pth
rm -rf /root/.cache/huggingface/hub/models--TMElyralab* 2>/dev/null || true
du -sh $R; echo MUSETALK_SETUP_OK
