#!/usr/bin/env python3
"""Build local editor archives. Never uploads or publishes."""
import hashlib
import json
import sys
from pathlib import Path
import shutil
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'
DIST.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(ROOT/'scripts/sync.py'),'--check'],check=True)
subprocess.run(['npm','ci','--ignore-scripts'],cwd=ROOT/'vscode',check=True)
subprocess.run(['npm','run','package'],cwd=ROOT/'vscode',check=True)
for path in (ROOT/'vscode').glob('*.vsix'):
    shutil.copy2(path,DIST/path.name)
subprocess.run(['cargo','build','--manifest-path',str(ROOT/'zed/Cargo.toml'),'--target','wasm32-wasip2','--release','--locked'],check=True)
with zipfile.ZipFile(DIST/'Dyn.sublime-package','w',zipfile.ZIP_DEFLATED) as archive:
    for path in sorted((ROOT/'sublime').iterdir()):
        if path.is_file(): archive.write(path,path.name)
for editor in ('helix','neovim','mason','zed'):
    with tarfile.open(DIST/f'dyn-{editor}.tar.gz','w:gz') as archive:
        for path in sorted((ROOT/editor).rglob('*')):
            if not path.is_file() or any(part in ('target','__pycache__') for part in path.parts): continue
            archive.add(path,arcname=str(Path(f'dyn-{editor}')/path.relative_to(ROOT/editor)),recursive=False)
        if not (ROOT/editor/'LICENSE').exists():
            archive.add(ROOT/'LICENSE',arcname=f'dyn-{editor}/LICENSE')
        archive.add(ROOT/'README.md',arcname=f'dyn-{editor}/README.md')
        archive.add(ROOT/'shared/debug',arcname=f'dyn-{editor}/shared/debug',filter=lambda info: None if '__pycache__' in info.name else info)
        if editor == 'neovim':
            archive.add(ROOT/'scripts/install-parser.py',arcname='dyn-neovim/scripts/install-parser.py')
            archive.add(ROOT/'shared/release.json',arcname='dyn-neovim/shared/release.json')
        if editor == 'zed':
            archive.add(ROOT/'zed/target/wasm32-wasip2/release/dyn.wasm',arcname='dyn-zed/extension.wasm')
# JSON is generated from the same YAML consumed by the tested file registry.
# The package manifest uses only this deliberately small subset of YAML.
registry = subprocess.check_output(['yq','-o','json',str(ROOT/'mason/packages/dyn/package.yaml')])
registry = json.dumps([json.loads(registry)],indent=2).encode()
with zipfile.ZipFile(DIST/'registry.json.zip','w',zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('registry.json',registry)
    archive.write(ROOT/'LICENSE','LICENSE')
(DIST/'checksums.txt').write_text(hashlib.sha256((DIST/'registry.json.zip').read_bytes()).hexdigest()+'  registry.json.zip\n'+hashlib.sha256(registry).hexdigest()+'  registry.json\n')
with (DIST/'SHA256SUMS').open('w') as output:
    for path in sorted(DIST.iterdir()):
        if path.is_file() and path.name != 'SHA256SUMS':
            output.write(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n')
print('Local artifacts:',DIST)
