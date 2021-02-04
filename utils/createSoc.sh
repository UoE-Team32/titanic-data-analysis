#!/bin/bash

if [[ $(uname) = *Darwin* ]]; then
    socat -V > /dev/null
    printf "Running socat...\n"
    socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"
else
  printf "Only required on macOS\n"
  exit 1
fi
