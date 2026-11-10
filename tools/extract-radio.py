#!/usr/bin/env python3
"""Select SHA-pinned exact619F radio inputs; never read NV or alter protocols.

Keep proprietary results private. Verify every input before creating output,
and refuse existing output rather than overwrite a working selection.
"""
from pathlib import Path
import argparse
import hashlib
from peripheral_parcel import transform as peripheral_parcel_transform
from peripheral_owner import transform as peripheral_owner_transform

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stock-system', required=True, type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent.parent
output = args.output or base/'proprietary/vendor'
assert not output.exists(), 'refuse existing radio selection: '+str(output)
records = []
for line in ((base/'config/manifests/radio-stock.sha256').read_text()+(base/'config/manifests/radio-ril-stock.sha256').read_text()).splitlines():
    expected, relative = line.split()
    assert relative.startswith('vendor/') and '..' not in Path(relative).parts
    source = args.stock_system/relative
    data = source.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert actual == expected, 'wrong exact619F radio input: '+relative
    if relative == 'vendor/lib64/libperipheral_client.so':
        data = peripheral_parcel_transform(data)
    elif relative == 'vendor/bin/pm-service':
        data = peripheral_owner_transform(data)
    records.append((data,relative.removeprefix('vendor/')))
assert records, 'empty radio selection'
for data,relative in records:
    target = output/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    target.chmod(0o755 if relative.startswith('bin/') else 0o644)
print('PASS exact619F radio selection; guarded PM Parcel/heap-owner ABI; no NV/calibration/protocol fixup')
