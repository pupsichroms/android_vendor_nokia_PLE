#!/usr/bin/env python3
"""Pin exact619F DSI; adapt ONLY feero's real RMNET rtnetlink selector to4.19."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
os.umask(0o077)
base=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stock-system',required=True,type=Path)
parser.add_argument('--output',type=Path)
args=parser.parse_args();output=args.output or base/'proprietary/vendor'
assert not output.exists(),'refuse existing config selection'
records={}
for name,expected in {'netmgr_config.xml':'b23d73feeddb91d60cb00d545c1b4edbdcff058511f08796e29e28a3f507e6ad',
 'dsi_config.xml':'14d91e49d00fe2b20fcfe32861b2bf6c02067877e3f7de6371a668208bc459fe'}.items():
    data=(args.stock_system/'vendor/etc/data'/name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected,'wrong exact619F '+name
    records[name]={'data':data,'input_sha256':expected}
original=records['netmgr_config.xml']['data']
prefix,body=original.split(b'<listitem name = "feero">',1)
feero,suffix=body.split(b'</listitem>',1)
anchor=b'      <data name="rmnet_data_enabled" type="int"> 1 </data>\n'
insert=b'      <data name="rtm_rmnet_data_enabled" type="int"> 1 </data>\n'
assert feero.count(anchor)==1 and b'rtm_rmnet_data_enabled' not in feero
derived=prefix+b'<listitem name = "feero">'+feero.replace(anchor,anchor+insert,1)+b'</listitem>'+suffix
assert derived.count(insert)==original.count(insert)+1
check_prefix,check_body=derived.split(b'<listitem name = "feero">',1)
assert check_prefix+b'<listitem name = "feero">'+check_body.replace(insert,b'',1)==original
for name,data in [('netmgr_config.xml',derived),('dsi_config.xml',records['dsi_config.xml']['data'])]:
    root=ET.fromstring(re.sub(rb'<\?xml[^?]*\?>',b'',data,count=1))
    assert root.find("listitem[@name='feero']") is not None
records['netmgr_config.xml']['data']=derived
# All input and transformation checks precede creation, never partial output.
(output/'etc/data').mkdir(parents=True,exist_ok=False)
for name,row in records.items():
    target=output/'etc/data'/name;target.write_bytes(row['data']);target.chmod(0o644)
(output/'provenance.json').write_text(json.dumps({'source':'exact619F signed OTA extraction',
 'files':{name:{'input_sha256':row['input_sha256'],'output_sha256':hashlib.sha256(row['data']).hexdigest()} for name,row in records.items()},
 'only_adaptation':'feero rtm_rmnet_data_enabled=1 for real CONFIG_RMNET4.19; existing stock rtrmnet API, no fake success',
 'reference':'Mi-Thorium proprietary_vendor_xiaomi_mithorium-common-4.19 ef0e4b987e555e0c5ff4850cff497695c8638a75 uses this selector on newer-platform entries, NOT identical feero settings',
 'no_kernel_firmware_NV_carrier_APN_security_change':True},indent=2)+'\n')
print('PASS2exact619Fconfigs;DSIbyteexact;ONLYfeeroRTMselectoradded')
