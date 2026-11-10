#!/usr/bin/env python3
"""Extract pinned619F packet-data inputs; add only the existing HIDL ABI link.

No protocol/code/calibration/firmware changes. Refuse wrong inputs/existing
output; keep private results private. The linked shim is source-built separately.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import struct
import subprocess as sp
import tempfile

os.umask(0o077)
base=Path(__file__).resolve().parent.parent
tree=base.parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stock-system',required=True,type=Path)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
output=args.output or base/'proprietary/vendor'
assert not output.exists(),'refuse existing data selection'
patchelf=tree/'prebuilts/extract-tools/linux-x86/bin/patchelf-0_18'
assert sp.check_output([str(patchelf),'--version'],text=True).strip()=='patchelf 0.18.0'

def sections(data):
    assert data[:6]==b'\x7fELF\x02\x01'
    off=struct.unpack_from('<Q',data,40)[0]
    size,count,index=struct.unpack_from('<HHH',data,58)
    rows=[struct.unpack_from('<IIQQQQIIQQ',data,off+i*size) for i in range(count)]
    strings=rows[index];names=data[strings[4]:strings[4]+strings[5]]
    return {names[r[0]:].split(b'\0',1)[0].decode():data[r[4]:r[4]+r[5]] for r in rows if r[1]!=8}

records=[]
for line in (base/'config/manifests/radio-data-stock.sha256').read_text().splitlines():
    expected,relative=line.split()
    assert relative.startswith('vendor/') and '..' not in Path(relative).parts
    assert relative in ('vendor/bin/netmgrd','vendor/etc/data/netmgr_config.xml') or relative.startswith('vendor/lib64/')
    data=(args.stock_system/relative).read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected,'wrong exact619F input '+relative
    records.append([relative,data,expected])
assert len(records)==19
for row in records:
    if row[0]!='vendor/bin/netmgrd':continue
    original=row[1]
    assert hashlib.sha256(original).hexdigest()=='fc97d495473fbf03df9a3aea1eda1560fcb4e2be6fcb4efa9dcc21fe6e07279d'
    with tempfile.TemporaryDirectory(prefix='ple-netmgr-link-') as temp:
        candidate=Path(temp)/'netmgrd';candidate.write_bytes(original)
        before=sp.check_output([str(patchelf),'--print-needed',str(candidate)],text=True).splitlines()
        assert 'libhidlbase_shim.so' not in before
        sp.run([str(patchelf),'--add-needed','libhidlbase_shim.so',str(candidate)],check=True)
        after=sp.check_output([str(patchelf),'--print-needed',str(candidate)],text=True).splitlines()
        assert after==['libhidlbase_shim.so']+before
        data=candidate.read_bytes()
    old,new=sections(original),sections(data)
    for name in ('.text','.plt','.rodata','.eh_frame','.eh_frame_hdr','.gcc_except_table','.init_array','.fini_array','.data','.data.rel.ro'):
        if name in old:assert old[name]==new[name],'code/unwind/runtime data changed: '+name
    assert original[24:32]==data[24:32],'entry point changed'
    for raw in (original,data):
        off=struct.unpack_from('<Q',raw,32)[0]
        entsize,count=struct.unpack_from('<HH',raw,54)
        for i in range(count):
            kind,flags=struct.unpack_from('<II',raw,off+i*entsize)
            assert kind!=1 or flags&3!=3,'writable executable LOAD segment'
    row[1]=data
# Validate all inputs/transformation BEFORE the first destination is created.
output.mkdir(parents=True,exist_ok=False)
for relative,data,expected in records:
    target=output/relative.removeprefix('vendor/')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data);target.chmod(0o755 if relative.startswith('vendor/bin/') else 0o644)
(output/'provenance.json').write_text(json.dumps({
    'source':'exact619F signed OTA extraction','patchelf_version':'0.18.0',
    'transform':'netmgrd DT_NEEDED libhidlbase_shim.so ONLY; code/unwind/data unchanged',
    'files':{r:{'input_sha256':h,'output_sha256':hashlib.sha256(d).hexdigest()} for r,d,h in records},
    'no_firmware_NV_calibration_protocol_change':True},indent=2)+'\n')
print('PASS19exact619F inputs; netmgr HIDL dependency only, all code/unwind/data bytes retained')
