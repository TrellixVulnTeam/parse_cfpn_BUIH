# !/usr/bin/env bash
# train
python -m experiments.segmentation.train --dataset pcontext \
    --model cfpn_gsf --aux --base-size 520 --crop-size 520 \
    --backbone resnest101 --checkname cfpn_gsf_resnest101_pcontext

#test [single-scale]
python -m experiments.segmentation.test_whole --dataset pcontext \
    --model cfpn_gsf --aux --base-size 520 --crop-size 520 \
    --backbone resnest101 --resume experiments/segmentation/runs/pcontext/cfpn_gsf/cfpn_gsf_resnest101_pcontext/model_best.pth.tar --split val --mode testval

#test [multi-scale]
python -m experiments.segmentation.test_whole --dataset pcontext \
    --model cfpn_gsf --aux --base-size 520 --crop-size 520 \
    --backbone resnest101 --resume experiments/segmentation/runs/pcontext/cfpn_gsf/cfpn_gsf_resnest101_pcontext/model_best.pth.tar --split val --mode testval --ms