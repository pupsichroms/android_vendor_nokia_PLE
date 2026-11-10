#!/usr/bin/env python3
"""Exact619F104->120-byte Parcel stack ABI, with matching unwind metadata.

No branch, call, opcode, authentication result or protocol byte is replaced.
Unknown input is rejected. The local pinned table contains only same-width
stack-immediate and CFI operand edits, derived and independently disassembled.
"""
import hashlib
import json
from pathlib import Path

def transform(data, reverse=False):
    table = json.loads(Path(__file__).with_name('goodix-parcel120.json').read_text())
    before = 'output_sha256' if reverse else 'input_sha256'
    after = 'input_sha256' if reverse else 'output_sha256'
    assert hashlib.sha256(data).hexdigest()==table[before], 'unknown Goodix Parcel ABI input'
    result = bytearray(data)
    for row in table['patches']:
        old = bytes.fromhex(row['new' if reverse else 'old'])
        new = bytes.fromhex(row['old' if reverse else 'new'])
        start = row['offset']
        assert len(old)==len(new) and bytes(result[start:start+len(old)])==old
        result[start:start+len(old)] = new
    assert hashlib.sha256(result).hexdigest()==table[after], 'Goodix Parcel ABI output mismatch'
    return bytes(result)
