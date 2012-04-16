#!/usr/bin/env python
"""Gets ip addresses from a file. Generate their Lat and Lon. Print them on a map.
"""

__author__ = 'cozzi.martin@gmail.com'


import csv
import jsonlib
import logging
import optparse
import requests
import sys
import time
import yaml
import pygeoip

from ipconverter import IpConverter
from map import Map



def main():
    """Where the magic happens."""

    options, configs = parse_args(sys.argv)
    ip_reader = csv.reader(open(options.ips, 'rb'), delimiter=',')
    ip_converter = IpConverter(configs)
    world_map = Map(1440, 1800, 'black')

    for row in ip_reader:
        try:
            ip = proxy_filter(row[0])
            data = ip_converter.get_gps_from_ip(ip)
            if data is not None:
                world_map.add_gps_to_map(data) 
                # requests.post(hotspot, data)
        except pygeoip.GeoIPError, error:
            logging.error(error)

    world_map.render()

def proxy_filter(ips):
    """Remove Proxies from the list of IPs"""
    ips = ips.split(';')[0]
    return ips.split(',')[0]


def parse_args(argv):
    """Parses args from sys."""
    parser = optparse.OptionParser(usage='%prog [OPTIONS]', description=__doc__)
    parser.add_option('--ips', dest='ips', help='File with Ips')
    parser.add_option('--config', dest='config', help='YAML config file')
    parser.add_option('--verbose', dest='verbose', action='store_true',
            default=False)
    parser.add_option('--stdin', dest='stdin', action='store_true',
            default=False)
    parser.add_option('--count', dest='count', type='int', default=5)


    options, args = parser.parse_args(argv)
    if len(args) > 1:
        parser.error('Unexpected argument: %s' % ', '.join(args[1:]))

    for opt in parser.option_list:
        if opt.dest:
            if getattr(options, opt.dest) is None:
                parser.error('%s is required!' % opt.get_opt_string())

    logger = logging.getLogger()
    logger.setLevel(options.verbose and logging.DEBUG or logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
    logger.addHandler(stream_handler)

    config_file = open(options.config, 'r') 
    configs = yaml.load(config_file)
    config_file.close()

    return options, configs


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.error('Ctrl-C: Quitting early.')
