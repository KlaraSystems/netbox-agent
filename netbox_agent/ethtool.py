import logging
import re
import subprocess
from shutil import which
import platform

#  Originally from https://github.com/opencoff/useful-scripts/blob/master/linktest.py

# mapping fields from ethtool output to simple names
field_map = {
    'Supported ports': 'ports',
    'Supported link modes': 'sup_link_modes',
    'Supports auto-negotiation': 'sup_autoneg',
    'Advertised link modes': 'adv_link_modes',
    'Advertised auto-negotiation': 'adv_autoneg',
    'Speed': 'speed',
    'Duplex': 'duplex',
    'Port': 'port',
    'Auto-negotiation': 'autoneg',
    'Link detected': 'link',
    'media': 'speed',
    'status': 'link',
}


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


class Ethtool():
    """
    This class aims to parse ethtool output
    There is several bindings to have something proper, but it requires
    compilation and other requirements.
    """

    def __init__(self, interface, *args, **kwargs):
        self.interface = interface

    def _parse_ethtool_output(self):
        """
        parse ethtool output
        """

        fields = {}
        field = ''
        fields['speed'] = '-'
        fields['link'] = '-'
        fields['duplex'] = '-'

        output = subprocess.getoutput('ethtool {}'.format(self.interface))

        for line in output.split('\n')[1:]:
            line = line.rstrip()
            r = line.find(':')
            if r > 0:
               field = line[:r].strip()
               if field not in field_map:
                  continue
               field = field_map[field]
               output = line[r + 1:].strip()
               fields[field] = output
            else:
               if len(field) > 0 and \
                 field in field_map:
                  fields[field] += ' ' + line.strip()

        return fields

    def _parse_ethtool_module_output(self):
        status, output = subprocess.getstatusoutput('ethtool -m {}'.format(self.interface))
        if status == 0:
            r = re.search(r'Identifier.*\((\w+)\)', output)
            if r and len(r.groups()) > 0:
                return {'form_factor': r.groups()[0]}
        return {}

    def _parse_ifconfig_output(self):
        """
        parse FreeBSD ifconfig output
        """

        fields = {}
        field = ''
        fields['speed'] = '-'
        fields['link'] = '-'
        fields['duplex'] = '-'

        output = subprocess.getoutput('ifconfig {}'.format(self.interface))

        for line in output.split('\n')[1:]:
            line = line.rstrip()
            r = line.find(':')
            if r > 0:
               field = line[:r].strip()
               if field not in field_map:
                  continue
               field = field_map[field]
               output = line[r + 1:].strip()
               fields[field] = output
            else:
               if len(field) > 0 and \
                 field in field_map:
                  fields[field] += ' ' + line.strip()

        if fields['link'] == 'active':
            fields['link'] = 'yes'

        logging.debug('Interface {interface} S {speed}, L {link}'.format(interface=self.interface, speed=fields['speed'],link=fields['link']))

        return fields

    def parse(self):
        logging.debug('Ethtool called')
        if platform.system() == 'Linux':
            if which('ethtool') is None:
                return None
            output = self._parse_ethtool_output()
            output.update(self._parse_ethtool_module_output())

        if platform.system() == 'FreeBSD':
            if which('ifconfig') is None:
                return None
            logging.debug(' -> FreeBSD')
            output = self._parse_ifconfig_output()
            #output.update(self._parse_ethtool_module_output())

        return output
