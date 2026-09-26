#!/usr/bin/env python3
"""Verify an explicitly selected published SDK, then update local editor pins."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('version', help='Example: 0.1.0-preview.5')
parser.add_argument('--grammar-revision', help='Optional full Tree-sitter commit ID')
args = parser.parse_args()
version = args.version.removeprefix('v')
if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?', version):
    parser.error('Expected a release version, not a URL or branch')
release = json.loads((ROOT/'shared/release.json').read_text())
url = f"https://api.github.com/repos/{release['repository']}/releases/tags/v{version}"
with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'dyn-editors'}),timeout=30) as response:
    remote = json.load(response)
assets = {asset['name']:asset for asset in remote['assets']}
for platform, asset in release['platforms'].items():
    name = asset['asset'].replace(release['version'],version)
    entry = assets[name]
    digest = hashlib.sha256()
    with urllib.request.urlopen(entry['browser_download_url'],timeout=60) as response:
        while chunk := response.read(1024*1024):
            digest.update(chunk)
    expected = entry.get('digest')
    if not expected or expected != 'sha256:' + digest.hexdigest():
        raise SystemExit(f'{name}: missing or mismatched GitHub SHA-256 digest')
    asset.update(asset=name,sha256=digest.hexdigest())
    print('Verified',name)
if args.grammar_revision:
    if not re.fullmatch('[0-9a-f]{40}',args.grammar_revision):
        parser.error('Grammar revision must be a full commit ID')
    release['grammar']['revision'] = args.grammar_revision
release['version'] = version
(ROOT/'shared/release.json').write_text(json.dumps(release,indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'scripts/sync.py')],check=True)
print('Local pins updated. Run checks and review with jj diff before publishing.')
