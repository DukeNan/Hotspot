#!/bin/bash

proj_dir=$(cd $(dirname $0); pwd)
cd $proj_dir
source $HOME/.envs/spider_py3/bin/activate
python3 run.py
deactivate
