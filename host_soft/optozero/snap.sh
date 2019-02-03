#!/bin/sh

#sudo ifconfig wlan0 down

mkdir -p images
uvccapture -v -x1600 -y1200 -t1 -w -c./process.sh -oimages/snap.jpg
