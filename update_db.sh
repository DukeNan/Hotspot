#!/bin/bash

proj_dir=$(cd $(dirname $0); pwd)

ts=`date +%Y%m%d`

file="save_data.py"

if [ $# -eq 1 ]; then
    ps -ef | grep "$proj_dir/$file" | grep -v "grep" | awk '{print $2}' | while read pid; do kill -9 $pid; done
    sleep 1
fi

cnt=$(ps -ef | grep  "proj_dir/$file" | grep -v "grep"| wc -l)

if [ $cnt -eq 0 ];then
    /home/shaun/.envs/spider_py3/bin/python3 $proj_dir/$file >> ./logs/${file}.${ts}.log 2>&1 &
fi