#!/usr/bin/env bash

OWNDIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

python3 ${OWNDIR}/doRecon.py
python3 ${OWNDIR}/webscanfromelastic.py
