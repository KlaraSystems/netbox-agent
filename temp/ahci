import subprocess
import json

def get_sysctl_ahci():
    result = subprocess.run(['sysctl', 'dev.ahci'], capture_output=True, text=True)
    return result.stdout

def parse_sysctl_ahci(output):
    lines = output.splitlines()
    data = {}
    
    for line in lines:
        if line.startswith('dev.ahci'):
            key, value = map(str.strip, line.split(':', 1))
            key_parts = key.split('.')
            short_key = key_parts[-1]
            
            if short_key == "%pnpinfo":
                pnpinfo_dict = {}
                for item in value.split():
                    k, v = item.split('=')
                    pnpinfo_dict[k] = v
                data['pnpinfo'] = pnpinfo_dict
            elif short_key == "%location":
                location_dict = {}
                for item in value.split():
                    k, v = item.split('=')
                    location_dict[k] = v
                data['location'] = location_dict
            else:
                data[short_key.strip('%')] = value

    return data

sysctl_output = get_sysctl_ahci()
parsed_data = parse_sysctl_ahci(sysctl_output)
json_output = json.dumps(parsed_data, indent=4)
print(json_output)
