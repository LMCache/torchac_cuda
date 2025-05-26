import os
from setuptools import setup, Extension
import torch
from torch.utils import cpp_extension

def _is_hip() -> bool:
        return torch.version.hip is not None or os.environ.get('HIP_PLATFORM') == 'amd'

def _hipify():
    import subprocess
    hipify_files = ["cal_cdf.cu", "main.cpp", "torchac_kernel.cuh",
        "torchac_kernel_dec_new.cu", "torchac_kernel_enc_new.cu"]
    subprocess.run(["rm", "-rf", "hip_output"])
    subprocess.run(["python", "hipify.py", "-p", ".", "-o", "hip_output"] + hipify_files)

is_hip = _is_hip()

source_files = []
if is_hip:
    _hipify()
    source_files.extend(['main_hip.cpp', 'cal_cdf.hip', 'torchac_kernel_dec_new.hip', 'torchac_kernel_enc_new.hip'])
else:
    source_files.extend(['main.cpp', 'cal_cdf.cu', 'torchac_kernel_dec_new.cu', 'torchac_kernel_enc_new.cu'])

extra_compile_args = {}
define_macros = []
name="torchac_cuda"

if is_hip:
    rocm_home = os.environ.get('ROCM_HOME', '/opt/rocm')
    hip_include = os.path.join(rocm_home, 'include')
    hipcub_include = os.path.join(rocm_home, 'include/hipcub')

    extra_compile_args['hip'] = [f'-I{hip_include}', f'-I{hipcub_include}']
    define_macros.append(('__HIP_PLATFORM_HCC__', '1'))
    define_macros.append(('__HIP_PLATFORM_AMD__', '1'))
#else:
    #extra_compile_args['nvcc'] = ['--compiler-options', "'-fPIC'"]
    #extra_compile_args['cxx'] = ['-static-libgcc', '-static-libstdc++'],

setup(
    name = "torchac_cuda",
    version = '0.2.5',
    description = 'GPU based arithmetic coding for LLM KV compression',
    author = 'Yihua Cheng',
    author_email = 'yihua98@uchicago.edu',
    include_package_data = True,
    ext_modules=[
        cpp_extension.CUDAExtension(
            "torchac_cuda",
			source_files,
            extra_compile_args=extra_compile_args,
			include_dirs=['./include', hip_include, hipcub_include] if is_hip else ['./include'],
            define_macros=define_macros
            ),
    ],
    cmdclass={
        'build_ext': cpp_extension.BuildExtension
    },
    install_requires = [
        "torch >= 2.1.0",
    ]
)

