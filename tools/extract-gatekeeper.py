#!/usr/bin/env python3
"""Extract only the unchanged, SHA-pinned Nokia619F hardware Gatekeeper."""
import argparse
import hashlib
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent.parent


def extract(stock_system, output, manifest=BASE / 'config/manifests/gatekeeper/stock.sha256'):
    stock_system, output = Path(stock_system).resolve(), Path(output)
    rows = Path(manifest).read_text().splitlines()
    if len(rows) != 1:
        raise ValueError('expected exactly one hardware Gatekeeper input')
    expected, relative = rows[0].split()
    if relative != 'vendor/lib64/hw/gatekeeper.msm8937.so':
        raise ValueError('unexpected stock Gatekeeper path')
    source = (stock_system / relative).resolve()
    if not source.is_relative_to(stock_system):
        raise ValueError('stock symlink escapes source root')
    with source.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != expected:
        raise ValueError('wrong or modified stock Gatekeeper input')
    if output.exists() or output.is_symlink():
        raise FileExistsError('refuse to overwrite an existing payload directory')
    target = output / 'lib64/hw/gatekeeper.msm8937.so'
    target.parent.mkdir(parents=True)
    shutil.copyfile(source, target)
    target.chmod(0o644)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stock-system', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=BASE / 'proprietary/vendor')
    args = parser.parse_args()
    extract(args.stock_system, args.output)
    print('PASS exact619F hardware Gatekeeper; no binary or credential fixup')
