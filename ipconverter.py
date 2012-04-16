"""Ops on IPs based on pygeoip"""

__author__ = 'cozzi.martin@gmail.com'


import pygeoip


class IpConverter:

    def __init__(self, configs):
        self.gi = pygeoip.GeoIP(configs['geoip'])

    def get_gps_from_ip(self, ip):
        """Returns Latitute and Longitude from an IP."""
        gir = self.gi.record_by_addr(ip)
        if gir is not None:
            lat = gir.get('latitude')
            lon = gir.get('longitude')
            if lat is not None and lon is not None:
                return {'lat': lat, 'lon': lon}

        return None
