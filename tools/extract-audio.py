#!/usr/bin/env python3
"""Exact619F audio extraction; bounded metadata/property/path fixups, no code patch."""
from pathlib import Path
import argparse
import hashlib
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--stock-system', required=True, type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent.parent
tree = base.parents[2]
output = args.output or base/'proprietary/vendor'
patchelf = tree/'prebuilts/extract-tools/linux-x86/bin/patchelf-0_17_2'

def sections(data):
    assert data[:5] == b'\x7fELF\x01'
    offset = struct.unpack_from('<I', data, 32)[0]
    size, count, names_index = struct.unpack_from('<HHH', data, 46)
    names_offset, names_size = struct.unpack_from('<II', data, offset+size*names_index+16)
    names = data[names_offset:names_offset+names_size]
    result = {}
    for i in range(count):
        header = offset+size*i
        index = struct.unpack_from('<I', data, header)[0]
        name = names[index:].split(b'\0', 1)[0].decode()
        start, length = struct.unpack_from('<II', data, header+16)
        if name in ('.text', '.plt'):
            result[name] = data[start:start+length]
    assert set(result) == {'.text', '.plt'}
    return result

properties = {
    'ro.bsp.device': 'ro.vendor.ple',
    'persist.smartamp.enable': 'persist.vendor.amp.en',
    'persist.smartamp.callenable': 'persist.vendor.amp.call',
    'audio.smartamp.init': 'vendor.amp.init',
    'audio.smartamp.mode': 'vendor.amp.mode',
    'audio.smartamp.stream': 'vendor.amp.stream',
    'audio.smartamp.parameter': 'vendor.amp.param',
}
records = []
for line in (base/'config/manifests/audio/stock.sha256').read_text().splitlines():
    digest, source = line.split()
    data = (args.stock_system/source).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, 'stock hash mismatch: '+source
    relative = source.removeprefix('vendor/')
    if source.startswith('lib/'):
        relative = source
    if source.endswith('/audio.primary.msm8937.so'):
        relative = 'lib/hw/audio.primary.ple.so'
    destination = output/relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    fixups = []
    original = data
    if data.startswith(b'\x7fELF'):
        for old, new in properties.items():
            old, new = old.encode()+b'\0', new.encode()+b'\0'
            if old in data:
                assert len(new) <= len(old)
                data = data.replace(old, new+b'\0'*(len(old)-len(new)))
                fixups.append(new[:-1].decode())
        old, new = b'/system/etc/NXPsmartamp/settings/', b'/vendor/etc/NXPsmartamp/settings/'
        if old in data:
            assert len(old) == len(new) and data.count(old) == 1
            data = data.replace(old, new)
            fixups.append('vendor NXP config path')
        if source == 'vendor/lib/libacdbloader.so':
            # HMD3.18 proc/asound/acdbdir returned the read-only DTS value PLE.
            # Keep that metadata contract on4.19 without a synthetic proc node
            # or changing any ACDB database, executable code or import.
            old, new = b'/proc/asound/acdbdir\0', b'/vendor/etc/acdbdir\0'
            assert data.count(old) == 1 and new not in data
            assert len(new) <= len(old)
            data = data.replace(old, new + b'\0' * (len(old) - len(new)))
            fixups.append('read-only vendor acdbdir selector; exact PLE board value')
    destination.write_bytes(data)
    if source.endswith('/audio.primary.msm8937.so'):
        subprocess.run([str(patchelf), '--set-soname', 'audio.primary.ple.so',
                        '--add-needed', 'libprocessgroup.so', str(destination)], check=True)
        fixups.append('PLE-local SONAME; DT_NEEDED libprocessgroup: real set_sched_policy provider')
    actual = destination.read_bytes()
    if data.startswith(b'\x7fELF'):
        assert sections(original) == sections(actual), 'executable code changed: '+source
    destination.chmod(0o644)
    records.append('\t'.join((source,relative,digest,hashlib.sha256(actual).hexdigest(),'; '.join(fixups) or 'none')))
(output/'provenance.tsv').write_text('stock_source\tdestination\tstock_sha256\toutput_sha256\tfixup\n'+'\n'.join(records)+'\n')
print('PASS exact619F audio extraction: '+str(len(records))+' files; .text/.plt unchanged')
