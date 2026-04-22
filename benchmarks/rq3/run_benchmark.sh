#!/bin/bash
set -x

cd $(dirname "$0")/../../premise
python premise/experiments.py --results-folder ../out/rq3/res/
