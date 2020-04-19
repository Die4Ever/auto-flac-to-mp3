import sys
import argparse
import glob
import re
import json
import argparse
import subprocess
import os.path
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', help='List of input files')
parser.set_defaults(files=['./'])
args = parser.parse_args()

def calla(cmds):
    print("running "+repr(cmds))
    subprocess.Popen(cmds).wait()

def insensitive_glob(pattern):
    return (
        glob.glob(pattern, recursive=True)
        + glob.glob(pattern+'/**', recursive=True)
        + glob.glob(pattern+'/*', recursive=True)
    )

def exists(file):
    exists = os.path.isfile(file)
    if exists:
        print("file already exists: " + file)
    return exists

def convert(file, mp3):
    p = Path(mp3).parent
    if not p.exists():
        p.mkdir()
    calla(['ffmpeg', '-i', file, '-c:v', 'copy', '-q:a', '0', mp3])

def proc_file(file):
    mp3_path = list(Path(file).parts)
    mp3_path[-2] += " MP3"
    mp3_path[-1] = re.sub( r'.flac$', '.mp3', mp3_path[-1], flags=re.IGNORECASE)
    mp3 = str(Path(*mp3_path))
    if exists(mp3):
        return
    convert(file, mp3)

for arg in args.files:
    for file in insensitive_glob(arg+'*'):
        if(file.endswith('.flac')):
            proc_file(file)
