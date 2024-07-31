from netbox_agent.raid.base import Raid, RaidController
from netbox_agent.misc import get_vendor
from netbox_agent.config import config
import subprocess
import logging
import re


def mpsutil():
    mpsutil_output = get_mpsutil_adapters()
    parsed_data = parse_mpsutil_adapters(mpsutil_output)

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
            controllers.append(device_info)

    return controllers

