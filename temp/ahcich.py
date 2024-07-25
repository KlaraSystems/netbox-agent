import subprocess
import json

def get_sysctl_ahcich():
    result = subprocess.run(['sysctl', 'dev.ahcich'], capture_output=True, text=True)
    return result.stdout

def parse_sysctl_ahcich(output):
    lines = output.splitlines()
    data = {}
    
    for line in lines:
        if line.startswith('dev.ahcich'):
            key, value = map(str.strip, line.split(':', 1))
            key_parts = key.split('.')
            channel = key_parts[2]
            short_key = key_parts[-1]

            if channel not in data:
                data[channel] = {}

            if short_key == "%pnpinfo":
                data[channel]['pnpinfo'] = value
            elif short_key == "%location":
                location_dict = {}
                for item in value.split():
                    k, v = item.split('=')
                    location_dict[k] = v
                data[channel]['location'] = location_dict
            else:
                data[channel][short_key.strip('%')] = value

    return data

sysctl_output = get_sysctl_ahcich()
parsed_data = parse_sysctl_ahcich(sysctl_output)
json_output = json.dumps(parsed_data, indent=4)
print(json_output)
