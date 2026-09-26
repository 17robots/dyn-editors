#!/usr/bin/env python3
"""Build the pinned Tree-sitter parser into a Neovim runtime directory."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime', type=Path, required=True)
args = parser.parse_args()
grammar = json.loads((ROOT/'shared/release.json').read_text())['grammar']
with tempfile.TemporaryDirectory(prefix='dyn-parser-') as directory:
    source = Path(directory)
    subprocess.run(['git','init','--quiet',str(source)],check=True)
    subprocess.run(['git','-C',str(source),'fetch','--quiet','--depth=1',grammar['repository'],grammar['revision']],check=True)
    subprocess.run(['git','-C',str(source),'checkout','--quiet','FETCH_HEAD'],check=True)
    output = args.runtime.resolve()/('parser/dyn.dll' if os.name == 'nt' else 'parser/dyn.so')
    output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([*shlex.split(os.environ.get('CC','clang' if os.name == 'nt' else 'cc')),'-O2',*([] if os.name == 'nt' else ['-fPIC']),'-shared','-I',str(source/'src'),
                    str(source/'src/parser.c'),str(source/'src/scanner.c'),'-o',str(output)],check=True)
    print(output)
