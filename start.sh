#!/bin/sh
timestamp=$(date +'%m-%d-%Y-%H_%M')
python3 /home/pi/moonscale/websocket_server.py 2>&1 | tee scale-$timestamp.log
