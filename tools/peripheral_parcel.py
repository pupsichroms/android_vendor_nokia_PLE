#!/usr/bin/env python3
"""Exact619F PM client: seven104->120 Parcel stack frames, no logic edits."""
from pathlib import Path
import hashlib
import json

def transform(data, reverse=False):
    table=json.loads(Path(__file__).with_name('peripheral-parcel120.json').read_text())
    before='output_sha256' if reverse else 'input_sha256'
    after='input_sha256' if reverse else 'output_sha256'
    assert hashlib.sha256(data).hexdigest()==table[before], 'unknown peripheral Parcel ABI input'
    assert table['functions']==7 and table['parcel_bytes']==120
    output=bytearray(data)
    for row in table['patches']:
        old=bytes.fromhex(row['new' if reverse else 'old'])
        new=bytes.fromhex(row['old' if reverse else 'new'])
        start=row['offset']
        assert len(old)==len(new)==4 and start%4==0
        assert output[start:start+4]==old
        output[start:start+4]=new
    assert hashlib.sha256(output).hexdigest()==table[after], 'peripheral Parcel output mismatch'
    return bytes(output)
