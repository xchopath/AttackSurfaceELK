#!/usr/bin/env bash

OWNDIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

python3 ${OWNDIR}/autorecon.py
python3 ${OWNDIR}/webscan.py
