#!/usr/bin/env bash

# number of parallel gpus
GPUS=0

# path to config file
CONFIG=configs/coco/instance-segmentation/maskformer2_aff_small_bs64_50ep.yaml

# checkpoint path for resume
RESUME=checkpoints/aff_small.pth

# output folder
OUTPUT=outputs/

python train_net.py --num-gpus $GPUS \
  --config-file $CONFIG \
  --dist-url tcp://127.0.0.1:12345 \
  --resume \
  --eval-only \
  MODEL.WEIGHTS $RESUME \
  OUTPUT_DIR $OUTPUT

# Remove '--resume', '--eval-only' and 'MODEL.WEIGHTS' to start training from fresh.
# Note that if '--resume' is on, the 'MODEL.WEIGHTS' option will be overwritten by the last_checkpoint file in the output folder (auto-resume), if the file exists.
# The KEY VALUE pairs must be at the end, after all the flags.
