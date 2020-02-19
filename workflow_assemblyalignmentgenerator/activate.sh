#!/bin/bash


cd /project/ClinicalMicrobio/faststorage/10carl/urecomb

# load conda
eval "$(~/miniconda3/bin/conda shell.bash hook)"

# certain go scripts should be included in path
export PATH=$PATH:$HOME/go/bin:$HOME/.local/bin


conda activate urecomb2
