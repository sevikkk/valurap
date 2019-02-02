#!/bin/sh

mkdir -p images
uvccapture -v -x1600 -y1200 -t1 -c./process.sh -oimages/snap.jpg
