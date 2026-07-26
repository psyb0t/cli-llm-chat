# Third-Party Notices

This repo's own code is WTFPL — do whatever the fuck you want with it (see `LICENSE`).
That freedom doesn't extend to the third-party stuff pulled in at runtime via
`requirements.txt`. The published runtime environment / container image bundles
some dependencies under their own licenses, listed below for the pedants and the
lawyers.

Full license texts for anything with a copyleft license live in `LICENSES/`.

| Component | Kind | License (SPDX) | Source | Where it lives | Note |
|---|---|---|---|---|---|
| python-telegram-bot | runtime dependency | LGPL-3.0-only | https://github.com/python-telegram-bot/python-telegram-bot | installed via `requirements.txt` / published env | Dynamically-linked runtime dep — weak copyleft, your code stays WTFPL. Full text: `LICENSES/LGPL-3.0.txt`. |
| nvidia-*-cu12 wheels (cublas, cuda-cupti, cuda-nvrtc, cuda-runtime, cudnn, cufft, curand, cusolver, cusparse, nccl, nvjitlink, nvtx) | runtime dependency | Proprietary (NVIDIA) | https://pypi.org/project/nvidia-cublas-cu12/ (and sibling `nvidia-*-cu12` packages) | installed via `requirements.txt` / published env | Runtime deps of torch's CUDA backend, proprietary NVIDIA license — not redistributable/modifiable under an OSI license, use governed by NVIDIA's own EULA. |
| torch | runtime dependency | BSD-3-Clause | https://github.com/pytorch/pytorch | installed via `requirements.txt` / published env | Permissive, attribution only. |
| transformers | runtime dependency | Apache-2.0 | https://github.com/huggingface/transformers | installed via `requirements.txt` / published env | Permissive, attribution only. |
