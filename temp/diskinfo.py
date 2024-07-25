import subprocess
import json
import glob

def get_diskinfo(device):
    result = subprocess.run(['diskinfo', '-v', device], capture_output=True, text=True)
    return result.stdout

def parse_diskinfo(output):
    lines = output.strip().split("\n")
    disk_id = lines[0].split("/")[-1]
    keys = [
        "sectorsize", 
        "mediasize in bytes", 
        "mediasize in sectors", 
        "stripesize", 
        "stripeoffset", 
        "Cylinders according to firmware.", 
        "Heads according to firmware.", 
        "Sectors according to firmware.", 
        "Disk descr.", 
        "Disk ident.", 
        "Attachment", 
        "Physical path", 
        "TRIM/UNMAP support", 
        "Rotation rate in RPM", 
        "Zone Mode"
    ]
    
    values = [line.split("#")[0].strip() for line in lines[1:]]
    
    diskinfo = {"id": disk_id}
    for key, value in zip(keys, values):
        diskinfo[key] = value
    
    return {"diskinfo": diskinfo}

def get_all_diskinfo():
    devices = glob.glob('/dev/da*')
    all_diskinfo = []
    for device in devices:
        diskinfo_output = get_diskinfo(device)
        parsed_data = parse_diskinfo(diskinfo_output)
        all_diskinfo.append(parsed_data)
    return all_diskinfo

all_diskinfo = get_all_diskinfo()
json_output = json.dumps(all_diskinfo, indent=4)
print(json_output)
