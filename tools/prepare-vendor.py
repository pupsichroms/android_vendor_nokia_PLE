#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prepare the complete private PLE payload from exact, already-extracted inputs.

No downloads, device access, metadata regeneration or overwrite of existing
payloads. Publish only after every expected file, digest and mode is verified.
"""
import argparse
import csv
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent.parent
PFP_AUTHORITY = 'TheMuppets_Mi8937_aae77327cb51edcfdbaa7df1e2e08fae19784f36'
PFP_SOURCE = 'proprietary/vendor/firmware/a530_pfp.fw'
PFP_HASH = '072cbbb67eeb67689fd3ba2c11708e0778ae873b42d79cac030821e12fbcd126'
FIXED_INPUTS = {
    'vendor/bin/sensors.qti': 'af585c5ce02d522828f9be051125063fcd0a70f9f5f0dae26598641e159e037d',
    'vendor/etc/data/netmgr_config.xml': 'b23d73feeddb91d60cb00d545c1b4edbdcff058511f08796e29e28a3f507e6ad',
    'vendor/etc/data/dsi_config.xml': '14d91e49d00fe2b20fcfe32861b2bf6c02067877e3f7de6371a668208bc459fe',
    'vendor/lib64/libsdmextension.so': 'fbefa88f5e3e2fa5847aac571ea0e6e72d9ffe21955774ae6796774c28139035',
    'vendor/lib64/libscalar.so': '0b8e85c5afe432899fbe830f2475672c4a4f107f2b55271ce196f55172f8e16b',
}

def relative(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or any(p in {'', '.', '..'} for p in name.split('/')):
        raise ValueError('unsafe relative input path: ' + name)
    return Path(*path.parts)

def checked(root, name, digest):
    path = (root / relative(name)).resolve()
    if not path.is_relative_to(root):
        raise ValueError('input symlink escape: ' + name)
    if not path.is_file():
        raise ValueError('missing input: ' + name)
    if not re.fullmatch('[0-9a-f]{64}', digest):
        raise ValueError('invalid input digest: ' + name)
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    if actual != digest:
        raise ValueError('input hash mismatch: ' + name)
    return path

def records(path):
    return [line.split('\t') for line in path.read_text().splitlines()
            if line.strip() and not line.startswith('#')]

def publish(source, destination):
    """Linux atomic rename without replacement, including a concurrent empty dir."""
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renameat2
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(-100, os.fsencode(source), -100, os.fsencode(destination), 1) != 0:
        error = ctypes.get_errno()
        raise OSError(error, 'refuse existing output or failed atomic publication', str(destination))

def prepare(args):
    destination = Path(os.path.abspath(args.output or BASE / 'proprietary'))
    if destination.exists() or destination.is_symlink():
        raise ValueError('refuse existing output: ' + str(destination))
    if not destination.parent.is_dir():
        raise ValueError('output parent must already exist: ' + str(destination.parent))
    if any(p.is_symlink() for p in destination.parents):
        raise ValueError('output parent symlink escape')
    stock = args.stock_root.resolve()
    if not (stock / 'system').is_dir():
        raise ValueError('missing extracted stock system input')
    # Do not resolve system/ on its own: an escaped system symlink must remain
    # detectable against the caller's complete stock root.
    system = stock / 'system'
    pfp = args.gpu_pfp_reference_root.resolve()
    android = (args.android_root or BASE.parents[2]).resolve()
    tools = android / 'prebuilts/extract-tools/linux-x86/bin'
    for name in ('patchelf-0_17_2', 'patchelf-0_18'):
        if not (tools / name).is_file():
            raise ValueError('missing Android extraction tool input: ' + name)
    llvm_strip = android / 'prebuilts/clang/host/linux-x86/clang-r563880c/bin/llvm-strip'
    if not llvm_strip.is_file():
        raise ValueError('missing Android extraction tool input: llvm-strip r563880c')
    expected = {}
    for digest, mode, name in records(BASE / 'config/payload-digests.tsv'):
        relative(name)
        if name in expected or not re.fullmatch('0[0-7]{3}', mode):
            raise ValueError('duplicate output or invalid mode: ' + name)
        expected[name] = (digest, int(mode, 8))
    if not expected:
        raise ValueError('empty expected output manifest')
    with (BASE / 'config/blob-spec.tsv').open() as stream:
        core = list(csv.DictReader(stream, delimiter='\t'))
    for row in core:
        authority = row['source_authority']
        if authority == 'Nokia6_V6.19F':
            path = checked(stock, row['source_path'], row['sha256'])
        elif (authority == PFP_AUTHORITY and row['source_path'] == PFP_SOURCE
              and row['destination_path'] == 'vendor/firmware/a530_pfp.fw'
              and row['sha256'] == PFP_HASH and row['abi'] == 'data'):
            path = checked(pfp, PFP_SOURCE, PFP_HASH)
        else:
            raise ValueError('unapproved core input authority')
        magic = path.read_bytes()[:5]
        abi = row['abi']
        if ((abi == 'elf32' and magic != b'\x7fELF\x01')
                or (abi == 'elf64' and magic != b'\x7fELF\x02')
                or (abi == 'data' and magic.startswith(b'\x7fELF'))
                or abi not in {'elf32', 'elf64', 'data'}):
            raise ValueError('core input ABI mismatch')
        row['input'] = path
        relative(row['destination_path'])
    # Validate all retained component input manifests before invoking any helper.
    for manifest in sorted((BASE / 'config/manifests').rglob('*.sha256')):
        for line in manifest.read_text().splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            digest, name = line.split()
            checked(stock, name if manifest.name == 'goodix-stock.sha256' else 'system/' + name, digest)
    for name, digest in FIXED_INPUTS.items():
        checked(stock, 'system/' + name, digest)
    wifi = records(BASE / 'config/manifests/wifi.tsv')
    for digest, name, target in wifi:
        checked(stock, 'system/' + name, digest)
        relative(target)
    groups = json.loads((BASE / 'config/payload-groups.json').read_text())
    # A new sibling stage is the only write before the complete output is valid.
    with tempfile.TemporaryDirectory(prefix='.ple-extract-', dir=destination.parent) as temporary:
        temporary = Path(temporary)
        toolkit = temporary / 'toolkit'
        package = toolkit / 'vendor/nokia/PLE'
        package.mkdir(parents=True)
        shutil.copytree(BASE / 'tools', package / 'tools', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copytree(BASE / 'config', package / 'config')
        (toolkit / 'prebuilts').symlink_to(android / 'prebuilts', target_is_directory=True)
        components = temporary / 'components'
        components.mkdir()
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        def run(script, *arguments):
            subprocess.run([sys.executable, str(package / 'tools' / script), *map(str, arguments)],
                           check=True, env=env)
        outputs = {}
        def component(key, script, *arguments):
            out = components / str(len(outputs))
            run(script, *arguments, '--output', out)
            outputs[key] = out
        core_dir = components / 'core'
        for row in core:
            target = core_dir / row['destination_path'].removeprefix('vendor/')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(row['input'], target)
        outputs['proprietary/vendor'] = core_dir
        component('audio/proprietary', 'extract-audio.py', '--stock-system', system)
        component('camera/proprietary', 'extract-camera.py', '--stock-system', system)
        component('display-composition', 'extract-display-composition.py', '--stock-root', stock)
        component('gatekeeper/proprietary', 'extract-gatekeeper.py', '--stock-system', system)
        for group, manifest in [('media/proprietary', 'stock.sha256'), ('media/c2d', 'c2d.sha256')]:
            component(group, 'extract-camera.py', '--stock-system', system,
                      '--manifest', package / 'config/manifests/media' / manifest)
        goodix = components / 'goodix'
        run('extract-goodix.py', '--stock-root', stock, '--output-root', goodix, '--verify-text')
        outputs['proprietary-goodix/vendor'] = goodix / 'vendor'
        component('radio/proprietary', 'extract-radio.py', '--stock-system', system)
        component('radio-data/proprietary', 'extract-radio-data.py', '--stock-system', system)
        component('radio-data-bam/proprietary', 'prepare-netmgr-bam.py', '--stock-system', system)
        # The retained NON-BAM variant includes Android's ELF metadata
        # normalization. The accepted BAM binary deliberately keeps the direct
        # prepare-netmgr-bam output. Final hashes enforce both exact recipes.
        subprocess.run([str(llvm_strip), '--strip-debug',
                        str(outputs['radio-data/proprietary'] / 'bin/netmgrd')], check=True, env=env)
        component('radio-data-config/proprietary', 'extract-radio-data-config.py', '--stock-system', system)
        component('sensors/proprietary', 'extract-sensors.py', '--stock-system', system)
        daemon = components / 'daemon'
        run('extract-sensor-daemon.py', '--stock-system', system, '--output', daemon / 'bin/sensors.qti')
        outputs['sensors/daemon'] = daemon
        output = temporary / 'proprietary'
        output.mkdir()
        def add(source, target):
            relative(target)
            if target not in expected:
                raise ValueError('unexpected output: ' + target)
            digest, mode = expected[target]
            data = source.read_bytes()
            if hashlib.sha256(data).hexdigest() != digest:
                raise ValueError('derived output digest mismatch: ' + target)
            dest = output / target
            if dest.exists() and dest.read_bytes() != data:
                raise ValueError('conflicting component outputs: ' + target)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            dest.chmod(mode)
        for group, directory in outputs.items():
            for source, target in groups[group].items():
                relative(source)
                if not target.startswith('proprietary/'):
                    raise ValueError('unsafe output mapping')
                add(directory / source, target.removeprefix('proprietary/'))
        for digest, source, target in wifi:
            add(checked(stock, 'system/' + source, digest), target)
        actual = {str(path.relative_to(output)) for path in output.rglob('*') if path.is_file()}
        if actual != set(expected):
            raise ValueError('incomplete prepared payload: ' + repr(sorted(set(expected) - actual)))
        # Re-read every output after merging, including shared destinations.
        for name, (digest, mode) in expected.items():
            checked(output, name, digest)
            if (output / name).stat().st_mode & 0o777 != mode:
                raise ValueError('output mode mismatch: ' + name)
        publish(output, destination)
    print('PASS complete private PLE payload: ' + str(len(expected)) + ' verified files at ' + str(destination))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stock-root', required=True, type=Path, help='extracted exact619F root containing system/')
    parser.add_argument('--gpu-pfp-reference-root', required=True, type=Path, help='root containing the pinned Mi8937 PFP file')
    parser.add_argument('--android-root', type=Path, help='LineageOS root providing prebuilts/extract-tools')
    parser.add_argument('--output', type=Path, help='new proprietary directory; default: this vendor tree/proprietary')
    args = parser.parse_args()
    prepare(args)

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError, AttributeError) as error:
        print('error: ' + str(error), file=sys.stderr)
        sys.exit(1)
