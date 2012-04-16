#!/usr/bin/env python

import unittest

from map import Map

class TestMap(unittest.TestCase):

    def setUp(self):
        self.map = Map(1200, 1024, 'black')


    def test_lon_to_x(self):
        self.assertEqual(self.map.lon_to_x(180), float(1200))
        self.assertEqual(round(self.map.lon_to_x(0)), float(600))
        self.assertEqual(self.map.lon_to_x(-180), float(0))

    def test_lat_to_y(self):
        self.assertEqual(self.map.lat_to_y(90), float(1024))
        self.assertEqual(round(self.map.lat_to_y(0)), float(512))
        self.assertEqual(round(self.map.lat_to_y(-90)), float(0))


if __name__ == '__main__':
    unittest.main()

