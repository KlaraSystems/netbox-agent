import subprocess
import json

def get_mpsutil_adapters():
    result = subprocess.run(['mpsutil', 'show', 'adapters'], capture_output=True, text=True)
    return result.stdout

def parse_mpsutil_adapters(output):
    lines = output.splitlines()
    data = []

    for line in lines[1:]:  # Skip the header line
        if line.strip():  # Ignore empty lines
            parts = line.split()
            device_info = {
                "Device Name": parts[0],
                "Chip Name": parts[1],
                "Board Name": parts[2],
                "Firmware": parts[3]
            }
            data.append(device_info)

    return data

def main():
    mpsutil_output = get_mpsutil_adapters()
    parsed_data = parse_mpsutil_adapters(mpsutil_output)

    json_output = json.dumps(parsed_data, indent=4)
    print(json_output)

if __name__ == "__main__":
    main()
