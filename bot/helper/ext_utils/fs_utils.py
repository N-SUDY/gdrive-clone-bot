from os import remove as osremove, path as ospath, walk
from shutil import rmtree

from bot import LOGGER

def clean_target(path: str):
    if ospath.exists(path):
        LOGGER.info(f"Cleaning Target: {path}")
        if ospath.isdir(path):
            try:
                rmtree(path)
            except:
                pass
        elif ospath.isfile(path):
            try:
                osremove(path)
            except:
                pass

def clean_download(path: str):
    if ospath.exists(path):
        LOGGER.info(f"Cleaning Download: {path}")
        try:
            rmtree(path)
        except:
            pass

def get_path_size(path: str):
    if ospath.isfile(path):
        return ospath.getsize(path)
    total_size = 0
    for root, dirs, files in walk(path):
        for f in files:
            abs_path = ospath.join(root, f)
            total_size += ospath.getsize(abs_path)
    return total_size
    