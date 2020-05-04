#!/bin/sh

find /home/pi/video -name "*.h264" -type f -mtime +14 -exec rm -f {} \;