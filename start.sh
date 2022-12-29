#!/bin/bash

venv/bin/python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
venv/bin/python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

if [ ! -d "downloads" ]; then
    mkdir downloads
fi

venv/bin/gunicorn --bind 0.0.0.0:80 web.wserver:app \
& venv/bin/python3 -m bot
