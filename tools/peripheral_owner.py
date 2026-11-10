#!/usr/bin/env python3
"""Pinned PLE619F PM owner lifetime fix; never disable RefBase checks."""
from pathlib import Path
import hashlib
import json

def transform(data, reverse=False):
    table=json.loads(Path(__file__).with_name('peripheral-owner.json').read_text())
    assert hashlib.sha256(Path(__file__).with_name('peripheral-owner.S').read_bytes()).hexdigest()==table['assembly_sha256']
    before='output_sha256' if reverse else 'input_sha256'
    after='input_sha256' if reverse else 'output_sha256'
    assert hashlib.sha256(data).hexdigest()==table[before], 'unknown peripheral owner input'
    output=bytearray(data)
    for row in table['patches']:
        start=row['offset']
        old=bytes.fromhex(row['new' if reverse else 'old'])
        new=bytes.fromhex(row['old' if reverse else 'new'])
        assert len(old)==len(new)==4 and start%4==0
        assert output[start:start+4]==old
        output[start:start+4]=new
    assert hashlib.sha256(output).hexdigest()==table[after]
    return bytes(output)
