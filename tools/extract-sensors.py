#!/usr/bin/env python3
"""Copy only SHA-pinned exact619F sensor inputs, without binary fixups."""
from pathlib import Path
import argparse
import hashlib
import shutil

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--stock-system', type=Path, required=True)
p.add_argument('--output', type=Path)
a = p.parse_args()
base = Path(__file__).resolve().parent.parent
output = a.output or base / 'proprietary/vendor'
for line in (base / 'config/manifests/sensors/stock.sha256').read_text().splitlines():
    expected, relative = line.split()
    assert relative.startswith('vendor/') and '..' not in Path(relative).parts
    source = a.stock_system / relative
    actual = hashlib.file_digest(source.open('rb'), 'sha256').hexdigest()
    assert actual == expected, 'wrong stock sensor input: ' + relative
    dest = output / relative.removeprefix('vendor/')
    assert not dest.exists(), 'refuse sensor payload overwrite: ' + str(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    dest.chmod(0o755 if relative.startswith('vendor/bin/') else 0o644)
print('PASS exact stock sensor inputs; no executable or factory-data fixup')
