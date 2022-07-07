#!/bin/bash
find /data/wwwroot/Hotspot/logs/ -mtime +7 -name "*.log" -exec rm -rf {} \;
