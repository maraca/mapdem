"""Projects Lat, Lon points on a Map after applying a Mercator Projection"""


__author__ = 'cozzi.martin@gmail.com'


import math
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from PIL import Image


class Map:
    """Builds a jpg map from lat and long."""

    def __init__(self, width, height, background):
        """Represents a Map of the world."""

        self.height = height
        self.width = width
        self.map = Image.new('RGB', (width, height), background)
        self.pixel_map = self.map.load()

    def add_gps_to_map(self, coords):
        """Adds a pixel to the map representing a GPS dict."""
        x, y  = (self.lon_to_x(coords['lon']), self.lat_to_y(coords['lat']))
        # init mins and maxs

        deep_sky_blue = (0, 191, 255)
        self.pixel_map[x, y] = deep_sky_blue

    def _crop(self, path_to_file):
        """Crops the picture."""
        top_lat = 75
        min_lat = -60

        left = 0
        top = int(self.lat_to_y(top_lat))
        width = self.width
        height = int(self.lat_to_y(min_lat)) - top

        box = (left, top, left + width, top + height)
        area = self.map.crop(box)
        area.save(path_to_file, 'JPEG', quality=95)

        return (width, height)

    def _add_x_y_min_max(self):
        """Adds red points for x and y"""
        red = (255, 0, 0) 
        yellow = (255, 255, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        derp = (255, 0, 255)
        thitle = (216, 191, 216)

        y_min, x_min = (0, 0)
        x_max, y_max = self.map.size
        y_center = y_max / 2
        x_center = x_max / 2
        y_max = y_max - 1
        x_max = x_max - 1

        lon_min = -180
        lon_max = 180
        lat_min = -85
        lat_max = 85

        for i, lat in enumerate(range(lat_min, lat_max)):
            for j, lon in enumerate(range(lon_min, lon_max)):
                if i % 10:
                    self.pixel_map[self.lon_to_x(lon), self.lat_to_y(lat)] = derp

                if j % 10 == 0:
                    self.pixel_map[self.lon_to_x(lon), self.lat_to_y(lat)] = green

        self.pixel_map[self.lon_to_x(0) + 1, self.lat_to_y(0) +1] = red
        self.pixel_map[self.lon_to_x(0) + 2, self.lat_to_y(0) +2] = red
        self.pixel_map[self.lon_to_x(0) + 3, self.lat_to_y(0) +3] = red
        self.pixel_map[self.lon_to_x(0) + 4, self.lat_to_y(0) +4 ] = red

        self.pixel_map[self.lon_to_x(-122) + 1, self.lat_to_y(-37) +1] = red
        self.pixel_map[self.lon_to_x(-122) + 2, self.lat_to_y(-37) +2] = red
        self.pixel_map[self.lon_to_x(-122) + 3, self.lat_to_y(-37) +3] = red
        self.pixel_map[self.lon_to_x(-122) + 4, self.lat_to_y(-37) +4 ] = red

        """
        for x in range(x_max):
            for y in range(y_max):
                if y % 10 == 0:
                    self.pixel_map[x_min, y] = red
                    self.pixel_map[x_center, y] = red
                    self.pixel_map[x_max, y] = red

                if y % 25 == 0:
                    self.pixel_map[x, y] = thitle

                if x % 10 == 0:
                    self.pixel_map[x, y_min] = yellow
                    self.pixel_map[x, y_center] = yellow
                    self.pixel_map[x, 1023] = yellow

                if x % 25 == 0:
                    self.pixel_map[x, y] = thitle
        """

    def render(self, path_to_file):
        """Renders the map, and return file size."""
        
        return self._crop(path_to_file)

    def lon_to_x(self, lon):
        """Returns x on the map."""
        max_lon = 180
        max_merc_x = self.merc_x(max_lon)
        x = ((self.merc_x(lon) * (self.width / 2) ) / max_merc_x) + self.width / 2
        # x = (lon * (self.width / 360.0)) + self.width / 2
        
        return x


    def lat_to_y(self, lat):
        """Returns y on the map."""
        #y = (lat * (self.height / 180.0)) + self.height / 2
        lat = lat * -1
        max_lat = 90
        max_merc_y = self.merc_y(max_lat)
        
        
        y = ((self.merc_y(lat) * (self.height / 2) ) / max_merc_y) + self.height / 2
        return y

    def merc_x(self, lon):
      r_major=6378137.000
      return r_major*math.radians(lon)
     
    def merc_y(self, lat):
      if lat>89.5:lat=89.5
      if lat<-89.5:lat=-89.5
      r_major=6378137.000
      r_minor=6356752.3142
      temp=r_minor/r_major
      eccent=math.sqrt(1-temp**2)
      phi=math.radians(lat)
      sinphi=math.sin(phi)
      con=eccent*sinphi
      com=eccent/2
      con=((1.0-con)/(1.0+con))**com
      ts=math.tan((math.pi/2-phi)/2)/con
      y=0-r_major*math.log(ts)
      return y
