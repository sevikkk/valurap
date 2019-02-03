#!/bin/sh

echo
nice -n 10 python get_current_pos.py | tee images/snap.txt

ln -f images/snap8.jpg images/snap9.jpg
ln -f images/snap7.jpg images/snap8.jpg
ln -f images/snap6.jpg images/snap7.jpg
ln -f images/snap5.jpg images/snap6.jpg
ln -f images/snap4.jpg images/snap5.jpg
ln -f images/snap3.jpg images/snap4.jpg
ln -f images/snap2.jpg images/snap3.jpg
ln -f images/snap1.jpg images/snap2.jpg
ln -f images/snap0.jpg images/snap1.jpg
ln -f images/snap8.txt images/snap9.txt
ln -f images/snap7.txt images/snap8.txt
ln -f images/snap6.txt images/snap7.txt
ln -f images/snap5.txt images/snap6.txt
ln -f images/snap4.txt images/snap5.txt
ln -f images/snap3.txt images/snap4.txt
ln -f images/snap2.txt images/snap3.txt
ln -f images/snap1.txt images/snap2.txt
ln -f images/snap0.txt images/snap1.txt

mv images/snap.txt images/snap0.txt
mv images/snap.jpg images/snap0.jpg

#mv images/snap.txt images/snap-`date +%s`.txt
echo -n Done
