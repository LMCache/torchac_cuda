# TorchAC CUDA/ROCm

For now this is a fork of [torchac_cuda
Github](https://github.com/LMCache/torchac_cuda.git)

This library is needed by LMCache repositories.

## Setup
### CUDA
```bash
python3 setup.py develop
```

### ROCm
Prerequisite:
- Installed Pytorch 2.6.0+rocm6.2
```bash
$ export ROCM_HOME=<path to rocm> [in dev /opt/rocm-6.2.0]
$ ./hipify.sh
$ PYTORCH_ROCM_ARCH=<HIP_ARCHITECTURE> python3 setup.py develop
> # e.g. MI210 MI250
> $ PYTORCH_ROCM_ARCH=gfx90a python3 setup.py develop
```
