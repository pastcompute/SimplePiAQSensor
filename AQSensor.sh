#!/bin/bash

#set -ex
#pwd
ReadSGP30/build/bin/read_sgp30 -s
ReadSGP30/build/bin/read_sgp30 -i

if test -e reset-baseline.flag ; then
  echo Reset baseline
  rm -f reset-baseline.flag
  rm -f $HOME/.lr_read_sgp30/baseline.txt
fi

echo Starting
python3 sgp30_display.py
