#!/bin/bash

proj_dir=$(cd $(dirname $0) || exit; pwd)

ts=$(date +%Y%m%d)

file="save_data.py"

if [ $# -eq 1 ]; then
  cd "$proj_dir" || exit
  /home/shaun/.envs/spider_py3/bin/python3 $file >> "$proj_dir"/logs/${file}."${ts}".log 2>&1 &
fi