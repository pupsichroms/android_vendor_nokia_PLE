#!/usr/bin/env python3
"""Reproduce pinned exact619F camera payload without replacing factory data.

Only metadata dependency fixups and selecting four unchanged PLE XML module
records are permitted. Native .text/.plt must remain byte-identical. Never
overwrite an existing output/checkpoint; validate all inputs before creating it.
"""
from pathlib import Path
import argparse
import hashlib
import re
import struct
import subprocess as sp
import xml.etree.ElementTree as E


def code_sections(data):
    assert data[:5]==b'\x7fELF\x01'
    offset=struct.unpack_from('<I',data,32)[0]
    size,count,index=struct.unpack_from('<HHH',data,46)
    names_offset,names_size=struct.unpack_from('<II',data,offset+size*index+16)
    names=data[names_offset:names_offset+names_size]
    result={}
    for i in range(count):
        header=offset+size*i
        index=struct.unpack_from('<I',data,header)[0]
        name=names[index:].split(b'\0',1)[0].decode()
        start,length=struct.unpack_from('<II',data,header+16)
        if name in ('.text','.plt'):result[name]=data[start:start+length]
    assert '.text' in result
    return result


def extract(stock,output,manifest,patchelf):
    assert not output.exists(), 'refusing to overwrite existing output/checkpoint'
    stock=stock.resolve()
    inputs=[]
    seen=set()
    for line in manifest.read_text().splitlines():
        if not line.strip() or line.startswith('#'):continue
        sha,relative=line.split()
        path=Path(relative)
        assert path.parts[0]=='vendor' and '..' not in path.parts and not path.is_absolute(),relative
        assert relative not in seen, 'duplicate input path'
        seen.add(relative)
        source=(stock/path).resolve()
        assert source.is_relative_to(stock), 'input escapes pinned stock root'
        data=source.read_bytes()
        assert hashlib.sha256(data).hexdigest()==sha, 'stock hash mismatch: '+relative
        inputs.append((relative,sha,data))
    assert inputs, 'empty camera input manifest'
    # All immutable inputs validated before publishing the fresh output tree.
    output.mkdir(parents=True)
    records=[]
    android_unused={'libmpbase.so','libarcsoft_night_shot.so','libarcsoft_smart_denoise.so'}
    names={'s5k3p3_ple_truly','s5k3p3_ofilm','s5k4h8_kingcome','s5k4h8_ple_ofilm'}
    for relative,sha,data in inputs:
        target=output/relative.removeprefix('vendor/')
        target.parent.mkdir(parents=True,exist_ok=True)
        fixups=[]
        original=data
        if relative=='vendor/etc/camera/camera_config.xml':
            root=E.fromstring(data)
            modules=[node for node in root if node.findtext('SensorName') in names]
            assert len(modules)==4 and {node.findtext('SensorName') for node in modules}==names
            selected=E.Element(root.tag,root.attrib)
            for node in modules:selected.append(node)
            notice=re.match(rb'\s*(<!--.*?-->)',data,re.S)
            assert notice, 'stock copyright notice missing'
            data=notice[1]+b'\n'+E.tostring(selected,encoding='utf-8')+b'\n'
            fixups.append('select only four byte-equivalent PLE module records')
        target.write_bytes(data)
        if original[:5]==b'\x7fELF\x01' and int.from_bytes(original[18:20],'little')==40:
            dynamic=sp.check_output(['readelf','-d',str(target)],text=True)
            if '[libstdc++.so]' in dynamic:
                sp.run([str(patchelf),'--replace-needed','libstdc++.so','libstdc++_vendor.so',str(target)],check=True)
                fixups.append('source-built libstdc++_vendor dependency name')
            if target.name in android_unused and '[libandroid.so]' in dynamic:
                # These exact pinned image algorithms import only C/math/log
                # primitives, not Android application APIs. Do not expose the
                # private platform libandroid namespace or add an empty shim.
                symbols=sp.check_output(['readelf','--wide','--dyn-syms',str(target)],text=True)
                assert not re.search(r'\bUND\s+(?:ANative|AAsset|ALooper|AInput|AConfiguration|AChoreographer)\w*',symbols)
                sp.run([str(patchelf),'--remove-needed','libandroid.so',str(target)],check=True)
                fixups.append('remove unused private libandroid DT_NEEDED')
            assert code_sections(original)==code_sections(target.read_bytes()), 'native code changed: '+relative
        target.chmod(0o755 if relative.startswith('vendor/bin/') else 0o644)
        records.append('\t'.join((relative,str(target.relative_to(output)),sha,
                                  hashlib.sha256(target.read_bytes()).hexdigest(),'; '.join(fixups) or 'none')))
    (output/'provenance.tsv').write_text('stock_source\tdestination\tstock_sha256\toutput_sha256\tfixup\n'+'\n'.join(records)+'\n')
    print(f'PASS {len(records)} pinned619F camera files; native code unchanged; no factory calibration input/output')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--stock-system',type=Path,required=True)
    p.add_argument('--output',type=Path)
    p.add_argument('--manifest',type=Path)
    args=p.parse_args()
    base=Path(__file__).resolve().parent.parent
    tree=base.parents[2]
    extract(args.stock_system,args.output or base/'proprietary/vendor',
            args.manifest or base/'config/manifests/camera/stock.sha256',
            tree/'prebuilts/extract-tools/linux-x86/bin/patchelf-0_17_2')
