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

from dateutil.parser import parse

from encoder import Video

def main():
    """Where the magic happens."""

    options, configs = parse_args(sys.argv)
    ip_reader = csv.reader(open(options.ips, 'rb'), delimiter=',')
    ip_converter = IpConverter(configs)
    width = options.width
    height = options.height
    color = 'black'
    # Here we apply ratios, since the map will be croped later on.
    width = int(width * 2.5)
    height = int(height * 1.33333333) 
    world_map = Map(width, height, color)

    roll = options.gen
    current_roll = None

    for row in ip_reader:
        try:
            ip = proxy_filter(row[0])
            timestamp = parse(row[1])
            if current_roll is None:
                current_roll = getattr(timestamp, roll)
            elif current_roll != getattr(timestamp, roll) and\
                    getattr(timestamp, roll) % options.gen_accuracy == 0:
                current_roll = getattr(timestamp, roll)
                # print current map to file, and generate new one.
                world_map.render('%s/%s.jpg' % (configs['maps']['folder'],
                    timestamp))

            data = ip_converter.get_gps_from_ip(ip)
            if data is not None:
                world_map.add_gps_to_map(data) 
        except pygeoip.GeoIPError, error:
            logging.error(error)
        except ValueError, error:
            logging.error(error)

    world_map.render('%s/%s.jpg' % (configs['maps']['folder'],
        timestamp))
    
    # generates video oO
    video = Video(width, height) 
    video.build(configs['maps']['folder'])

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
    parser.add_option('--height', dest='height', type='int', default=1080)
    parser.add_option('--width', dest='width', type='int', default=720)
    parser.add_option('--gen', dest='gen', default='hour',
            help='Generates pictures for every: minute, hour, day')
    parser.add_option('--gen-accuracy', dest='gen_accuracy', type='int', 
            default=1, help='Every x minute/hour/day')

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
