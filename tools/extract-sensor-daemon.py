#!/usr/bin/env python3
"""Exact619F sensor daemon, private writable registry, never factory writes."""
from pathlib import Path
import argparse
import hashlib
import struct

STOCK_SHA = 'af585c5ce02d522828f9be051125063fcd0a70f9f5f0dae26598641e159e037d'

def sections(data):
    assert data[:6] == b'\x7fELF\x02\x01' and struct.unpack_from('<H',data,18)[0] == 183
    offset = struct.unpack_from('<Q',data,40)[0]
    size,count,index = struct.unpack_from('<HHH',data,58)
    strings_offset,strings_size = struct.unpack_from('<QQ',data,offset+size*index+24)
    strings = data[strings_offset:strings_offset+strings_size]
    result = {}
    for number in range(count):
        header = offset+size*number
        name_offset = struct.unpack_from('<I',data,header)[0]
        name = strings[name_offset:].split(b'\0',1)[0].decode()
        start,length = struct.unpack_from('<QQ',data,header+24)
        result[name] = (start,length)
    return result

def rehome(data):
    assert hashlib.sha256(data).hexdigest()==STOCK_SHA, 'wrong stock daemon input'
    original=data
    start,length=sections(data)['.rodata']
    for directory in (b'/mnt/vendor/persist/sensors/', b'/persist/sensors/'):
        for filename,destination in ((b'sns.reg',b'/data/vendor/sensors/r'),
                                     (b'sensors_dbg_config.txt',b'/data/vendor/sensors/d')):
            old=directory+filename+b'\0'
            new=destination+b'\0'
            assert len(new)<=len(old) and data.count(old)==1, 'unexpected registry path layout'
            offset=data.index(old)
            assert start<=offset and offset+len(old)<=start+length, 'path outside .rodata'
            data=data[:offset]+new+b'\0'*(len(old)-len(new))+data[offset+len(old):]
    assert len(original)==len(data) and b'/persist/sensors/' not in data
    assert original[:start]==data[:start] and original[start+length:]==data[start+length:]
    return data

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stock-system',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    assert not a.output.exists(), 'refuse output/checkpoint overwrite'
    result=rehome((a.stock_system/'vendor/bin/sensors.qti').read_bytes())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(result)
    a.output.chmod(0o755)
    print('INPUT',STOCK_SHA,'OUTPUT',hashlib.sha256(result).hexdigest())
