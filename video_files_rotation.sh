#!/bin/sh

find /home/pi/video -name "*.h264" -type f -mtime +10 -exec rm -f {} \;
