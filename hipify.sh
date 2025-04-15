#!/bin/bash

rm -rf hip_output
mkdir hip_output
python hipify.py -p . -o hip_output/ cal_cdf.cu main.cpp torchac_kernel.cuh torchac_kernel_dec_new.cu torchac_kernel_enc_new.cu
