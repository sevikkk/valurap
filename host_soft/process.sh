#!/bin/sh

ln -f images/snap8.jpg images/snap9.jpg
ln -f images/snap7.jpg images/snap8.jpg
ln -f images/snap6.jpg images/snap7.jpg
ln -f images/snap5.jpg images/snap6.jpg
ln -f images/snap4.jpg images/snap5.jpg
ln -f images/snap3.jpg images/snap4.jpg
ln -f images/snap2.jpg images/snap3.jpg
ln -f images/snap1.jpg images/snap2.jpg
ln -f images/snap0.jpg images/snap1.jpg
mv images/snap.jpg images/snap0.jpg
#mv images/snap.jpg images/snap-`date +%s`.jpg
