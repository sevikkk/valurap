#!/bin/sh

echo 'char *build_timestamp="built '`date +%Y/%m/%d\ %H:%M:%S`'";' > timestamp.c
