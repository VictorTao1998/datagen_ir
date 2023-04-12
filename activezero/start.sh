#!/bin/sh

/root/miniconda3/bin/conda init && source /root/miniconda3/etc/profile.d/conda.sh && conda activate activezero2 && cd /code/datagen_ir/activezero/ && ulimit -c 0