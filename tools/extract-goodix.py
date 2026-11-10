#!/usr/bin/env python3
"""Reproduce the narrow PLE619F Goodix selection without replacing core blobs.

All source hashes are checked before writing. Dependency/property/path fixups
and the guarded104->120-byte Parcel stack-layout compatibility transform only;
no permission grant, security-check removal or firmware-update suppression.
Redistribution of the proprietary outputs remains unverified: keep local.
"""
from pathlib import Path
import argparse
import hashlib
import struct
import subprocess
from goodix_parcel import transform as parcel_transform

parser = argparse.ArgumentParser()
parser.add_argument('--stock-root', required=True, type=Path)
parser.add_argument('--output-root', type=Path)
parser.add_argument('--verify-text', action='store_true')
args = parser.parse_args()
base = Path(__file__).resolve().parent.parent
tree = base.parents[2]
out = args.output_root or base/'proprietary'
tool = tree/'prebuilts/extract-tools/linux-x86/bin/patchelf-0_17_2'
records = []
for line in (base/'config/manifests/goodix-stock.sha256').read_text().splitlines():
    digest, source = line.split()
    data = (args.stock_root/source).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, 'stock hash mismatch: '+source
    relative = source.removeprefix('system/')
    if relative.startswith('etc/firmware/'):
        relative = 'vendor/firmware/'+Path(source).name
    elif relative == 'lib64/libstdc++.so':
        relative = 'vendor/'+relative
    records.append((source, relative, digest, data))

def text_segment(data):
    assert data[:5] == b'\x7fELF\x02'
    shoff = struct.unpack_from('<Q', data, 40)[0]
    entsize, count, stridx = struct.unpack_from('<HHH', data, 58)
    strings_header = shoff+stridx*entsize
    strings_offset, strings_size = struct.unpack_from('<QQ', data, strings_header+24)
    names = data[strings_offset:strings_offset+strings_size]
    for i in range(count):
        header = shoff+i*entsize
        index = struct.unpack_from('<I', data, header)[0]
        name = names[index:].split(b'\0',1)[0]
        if name == b'.text':
            offset,size = struct.unpack_from('<QQ',data,header+24)
            return data[offset:offset+size]
    raise AssertionError('no executable text section')

provenance = ['stock_source\tdestination\tstock_sha256\toutput_sha256\tfixup']
for source, relative, digest, data in records:
    destination = out/relative
    destination.parent.mkdir(parents=True,exist_ok=True)
    fixup = 'none'
    if relative.endswith('/gxfingerprint.default.so'):
        old,new = b'/system/etc/firmware\0',b'/vendor/firmware\0'
        assert data.count(old) == 1, 'ambiguous firmware-path literal'
        data = data.replace(old,new+b'\0'*(len(old)-len(new)))
        fixup = 'firmware search path only: /system/etc/firmware -> /vendor/firmware'
    if '/lib64/' in relative:
        names = {
            b'persist.fp.navigation': b'persist.vendor.fpnav',
            b'sys.gxfp.lv': b'vendor.fplv',
            b'sys.gxfp.version': b'vendor.fpver',
            b'sys.fih.fingerprint': b'vendor.fpready',
            b'sys.fp.vid': b'vendor.fp',
            b'persist.enable.esd': b'persist.vendor.esd',
            b'persist.close.keymaster': b'persist.vendor.closekm',
            b'ro.template.count': b'ro.vendor.fpcnt',
        }
        applied = []
        for old, new in names.items():
            old, new = old+b'\0', new+b'\0'
            if old in data:
                assert len(new) <= len(old) and data.count(old) == 1
                data = data.replace(old, new+b'\0'*(len(old)-len(new)))
                applied.append(new[:-1].decode())
        if applied:
            fixup += '; vendor property names: '+','.join(applied)
    if relative.endswith('/libfp_client.so'):
        data = parcel_transform(data)
        fixup += '; guarded42 Parcel stack frames104->120 plus matching CFI; calls/branches unchanged'
    destination.write_bytes(data)
    destination.chmod(0o755 if '/bin/' in relative else 0o644)
    if relative.endswith('/gx_fpd'):
        # The symbol audit found no imports from these two obsolete DSOs.
        subprocess.run([str(tool),'--remove-needed','libbacktrace.so',
                        '--remove-needed','libunwind.so',str(destination)],check=True)
        fixup = 'remove two unused obsolete DT_NEEDED entries only'
    elif relative.endswith('/libfpservice.so'):
        subprocess.run([str(tool),'--add-needed','libple_goodix_dumpdeny.so',str(destination)],check=True)
        fixup += '; add fail-closed diagnostic DUMP permission bridge only'
    output = destination.read_bytes()
    if '/firmware/' in relative:
        assert hashlib.sha256(output).hexdigest() == digest, 'firmware changed: '+source
    elif args.verify_text and output.startswith(b'\x7fELF'):
        original = (args.stock_root/source).read_bytes()
        verified = parcel_transform(output,reverse=True) if relative.endswith('/libfp_client.so') else output
        assert text_segment(verified) == text_segment(original), 'unexpected executable code changed: '+source
    provenance.append('\t'.join((source,relative,digest,hashlib.sha256(output).hexdigest(),fixup)))
(out/'provenance.tsv').write_text('\n'.join(provenance)+'\n')
print('PASS exact619F Goodix selection: '+str(len(records))+' files; guarded Parcel layout only, TA bytes unchanged')
