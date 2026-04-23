#!/bin/bash
cd $(dirname "$0")/../../premise

folder=$1
others=""
if [ -z "$folder" ]; then
    folder="res"
fi
if [ "$folder" == "smoke_test" ]; then
    others="--smoke-test"
fi

python premise/experiments.py --results-folder ../out/rq3/$folder $others
