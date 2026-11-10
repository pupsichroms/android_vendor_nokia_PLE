#!/usr/bin/env python3
"""Extract only the hash-pinned PLE619F SDM dependencies; never replace core/HWC."""
from pathlib import Path
import argparse,hashlib,json,shutil

FILES={
 'libsdmextension.so':'fbefa88f5e3e2fa5847aac571ea0e6e72d9ffe21955774ae6796774c28139035',
 'libscalar.so':'0b8e85c5afe432899fbe830f2475672c4a4f107f2b55271ce196f55172f8e16b',
}
def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--stock-root',type=Path,required=True)
    cli.add_argument('--output',type=Path,default=Path(__file__).resolve().parent.parent/'proprietary/vendor')
    args=cli.parse_args();stock=args.stock_root.resolve();checked=[]
    for name,digest in FILES.items():
        source=stock/'system/vendor/lib64'/name;dest=args.output/'lib64'/name
        if source.is_symlink() or not source.resolve().is_relative_to(stock):
            raise SystemExit('Refusing an escaped stock source: '+name)
        data=source.read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest or data[:5]!=b'\x7fELF\x02':
            raise SystemExit('Not the exact PLE619F ELF64 dependency: '+name)
        if dest.is_symlink() or (dest.exists() and dest.read_bytes()!=data):
            raise SystemExit('Refusing to overwrite another payload: '+str(dest))
        checked.append((source,dest,digest,len(data)))
    # Every input and existing destination is checked before creating output.
    for source,dest,digest,size in checked:
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():shutil.copyfile(source,dest)
        dest.chmod(0o644)
    manifest={'authority':'Nokia PLE official Android9 619F local stock',
      'license_status':'proprietary-stock-local-extraction; redistribution-not-qualified',
      'profile':'PLE_ENABLE_STOCK_SDM_EXTENSION=true; default enabled after PLE runtime qualification',
      'source_built_core_hwc_gpu_userspace_unchanged':True,
      'files':[{'source':'system/vendor/lib64/'+s.name,'target':'/vendor/lib64/'+d.name,
                'sha256':digest,'bytes':size} for s,d,digest,size in checked]}
    (args.output/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('PASS exact619F SDM extension+scalar extracted; no core/HWC/GPU replacement')

if __name__=='__main__':main()
