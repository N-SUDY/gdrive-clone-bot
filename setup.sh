#!/bin/bash

if [ -d "venv" ]; then
    rm -r venv
fi

python3 -m venv --upgrade-deps venv \
&& venv/bin/pip3 install --no-cache-dir wheel \
&& venv/bin/pip3 install --no-cache-dir -Ur requirements.txt