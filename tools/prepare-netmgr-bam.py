#!/usr/bin/env python3
"""Link physical-BAM initialization without LD_PRELOAD/AT_SECURE bypass."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, struct, subprocess, tempfile
os.umask(0o077)
base=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stock-system',required=True,type=Path)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
dest=args.output or base/'proprietary/vendor'
assert not dest.exists(),'refuse existing BAM selection'
source=args.stock_system/'vendor/bin/netmgrd'
def sha(data): return hashlib.sha256(data).hexdigest()
original=source.read_bytes()
assert sha(original)=='fc97d495473fbf03df9a3aea1eda1560fcb4e2be6fcb4efa9dcc21fe6e07279d','wrong exact619F netmgr input'
tool=base.parents[2]/'prebuilts/extract-tools/linux-x86/bin/patchelf-0_18'
def sections(data):
    assert data[:6]==b'\x7fELF\x02\x01'
    offset=struct.unpack_from('<Q',data,40)[0]
    stride,count,index=struct.unpack_from('<HHH',data,58)
    rows=[struct.unpack_from('<IIQQQQIIQQ',data,offset+i*stride) for i in range(count)]
    names=rows[index]; strings=data[names[4]:names[4]+names[5]]
    return {strings[row[0]:].split(b'\0',1)[0].decode():data[row[4]:row[4]+row[5]] for row in rows if row[1]!=8}
with tempfile.TemporaryDirectory(prefix='ple-netmgr-bam-') as temp:
    binary=Path(temp)/'netmgrd'; shutil.copyfile(source,binary)
    subprocess.run([str(tool),'--add-needed','libple_netmgr_bam.so',str(binary)],check=True)
    subprocess.run([str(tool),'--add-needed','libhidlbase_shim.so',str(binary)],check=True)
    actual=binary.read_bytes()
    before,after=sections(original),sections(actual)
    for name in ('.text','.plt','.rodata','.eh_frame','.eh_frame_hdr','.gcc_except_table','.init_array','.fini_array','.data','.data.rel.ro'):
        if name in before: assert before[name]==after[name],name+' native bytes changed'
    assert original[24:32]==actual[24:32],'entrypoint changed'
    for data in (original,actual):
        offset=struct.unpack_from('<Q',data,32)[0]
        stride,count=struct.unpack_from('<HH',data,54)
        for i in range(count):
            kind,flags=struct.unpack_from('<II',data,offset+i*stride)
            assert kind!=1 or flags&3!=3,'writable executable LOAD segment'
    old=subprocess.check_output([str(tool),'--print-needed',str(source)],text=True).splitlines()
    new=subprocess.check_output([str(tool),'--print-needed',str(binary)],text=True).splitlines()
    assert 'libhidlbase_shim.so' not in old and new==['libhidlbase_shim.so','libple_netmgr_bam.so']+old
    (dest/'bin').mkdir(parents=True,exist_ok=False)
    shutil.copyfile(binary,dest/'bin/netmgrd'); (dest/'bin/netmgrd').chmod(0o755)
(dest/'provenance.json').write_text(json.dumps({'source':'registered exact619F native netmgr, existing GLOBAL HIDL bridge',
    'input_sha256':sha(original),'output_sha256':sha(actual),'only_delta':'DT_NEEDED libple_netmgr_bam.so, GLOBAL HIDL retained first',
    'native_code_rodata_unwind_entrypoint_unchanged':True,'no_preload_environment_or_security_bypass':True},indent=2)+'\n')
print('PASS linked BAM dependency/GLOBAL HIDL first/native code+unwind unchanged')
