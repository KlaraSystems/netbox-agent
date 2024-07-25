import subprocess
import json

def get_dmidecode():
    result = subprocess.run(['dmidecode'], capture_output=True, text=True)
    return result.stdout

def parse_dmidecode(output):
    lines = output.splitlines()
    data = {}
    current_section = None
    current_subsection = None

    for line in lines:
        if line.startswith('Handle'):
            continue
        if "Physical Memory Array" in line:
            current_section = 'Physical Memory Array'
            data[current_section] = {}
        elif "Memory Device" in line:
            current_section = 'Memory Device'
            if current_section not in data:
                data[current_section] = []
            current_subsection = {}
            data[current_section].append(current_subsection)
        elif line.startswith('\t') and current_section:
            key, value = map(str.strip, line.split(':', 1))
            if current_section == 'Physical Memory Array':
                if key not in ["Starting Address", "Ending Address"]:
                    data[current_section][key] = value
            elif current_section == 'Memory Device' and current_subsection is not None:
                if key not in [
                    "Starting Address", "Ending Address", "Range Size", "Physical Device Handle", 
                    "Memory Array Mapped Address Handle", "Partition Row Position"]:
                    current_subsection[key] = value
        elif line.strip() == "" and current_section == 'Memory Device':
            if current_subsection is not None and not current_subsection:
                data[current_section].remove(current_subsection)
            current_subsection = None

    return data

dmidecode_output = get_dmidecode()
parsed_data = parse_dmidecode(dmidecode_output)
json_output = json.dumps({"dimminfo": parsed_data}, indent=4)
print(json_output)
