#!/bin/bash

if (( `pgrep -f 'selenium-server-standalone' | wc -l` > 0 ))
then
  exit 0
else
  exit 1
fi
