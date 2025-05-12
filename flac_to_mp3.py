import argparse
import glob
import argparse
import subprocess
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

def convert(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix == '.mp3':
        calla(['ffmpeg', '-i', str(src), '-c:v', 'copy', '-q:a', '0', str(dest)])
    else:
        calla(['ffmpeg', '-i', str(src), '-c:a', dest.suffix[1:], str(dest)])

def proc_file(src, new_format:str):
    src = Path(src)
    dest_path = list(src.parts)
    dest_path[-2] += " " + new_format.upper()
    dest_path[-1] = src.stem +'.'+ new_format.lower()
    dest: Path = Path(*dest_path)
    if dest.exists():
        return
    convert(src, dest)
    return dest

for arg in args.files:
    for file in insensitive_glob(arg+'*'):
        if(file.endswith('.flac')):
            proc_file(file, 'mp3')
        if(file.endswith('.aiff')):
            result = proc_file(file, 'flac')
            proc_file(result, 'mp3')
