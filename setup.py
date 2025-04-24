from setuptools import setup, Extension
from torch.utils import cpp_extension

setup(
    name = 'torchac_cuda',
    version = '0.2.5',
    description = 'GPU based arithmetic coding for LLM KV compression',
    author = 'Yihua Cheng',
    author_email = 'yihua98@uchicago.edu',
    include_package_data = True,
    ext_modules=[
        cpp_extension.CUDAExtension(
            'torchac_cuda',
            [
                'main.cpp',
                'torchac_kernel_enc_new.cu',
                'torchac_kernel_dec_new.cu',
                'cal_cdf.cu',
            ],
            extra_compile_args={
                #'cxx': ['-static-libgcc', '-static-libstdc++'],
                #'nvcc': ['--compiler-options', "'-fPIC'"]
            },
            include_dirs=['./include']
            ),

    ],
    cmdclass={
        'build_ext': cpp_extension.BuildExtension
    },
    install_requires = [
        "torch == 2.6.0",
    ]
)
