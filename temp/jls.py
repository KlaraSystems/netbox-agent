import subprocess
import json

def get_jls_json():
    result = subprocess.run(['jls', '--libxo', 'json,pretty', '-n'], capture_output=True, text=True)
    return result.stdout

def capturejls():
    jls_output = get_jls_json()
    try:
        parsed_data = json.loads(jls_output)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return
    json_output = json.dumps(parsed_data, indent=4)
    print(json_output)

capturejls()
