#encoding:UTF-8

import os
import numpy as np
from PyQt5.QtCore import *
import unittest

from shape import Shape
import sort_points

class PolygonSortedTest(unittest.TestCase):
    
    def setUp(self):
        p0 = [[0, 0], [10, 0], [10, 11], [0, 11]]
        p1 = [[1, 1], [9, 1], [9, 9], [1, 9]]
        p2 = [[2, 2], [8, 2], [8, 7], [2, 7]]
        poly0 = Shape()
        for p in p0:
            poly0.loadPoint(QPointF(*p))
        poly1 = Shape()
        for p in p1:
            poly1.loadPoint(QPointF(*p))
        poly2 = Shape()
        for p in p2:
            poly2.loadPoint(QPointF(*p))
        self.shapes = [poly0, poly1, poly2]
    
    def tearDown(self):
        del self.shapes
    
    def test_polyarea_0(self):
        x = [0, 1, 1, 0]
        y = [0, 0, 1, 1]
        result = sort_points.PolyArea(x, y)
        self.assertEqual(result, 1)
    
    def test_polyarea_1(self):
        x = [0, 2, 1, 0]
        y = [0, 0, 1, 1]
        result = sort_points.PolyArea(x, y)
        self.assertEqual(result, 1.5)
    
    def test_polyarea_2(self):
        x = [0, 1, 0]
        y = [0, 0, 1]
        result = sort_points.PolyArea(x, y)
        self.assertEqual(result, 0.5)
    
    def test_get_area_0(self):
        result = []
        for i in self.shapes:
            result.append(sort_points.get_area(i))
        self.assertListEqual(result, [110, 64, 30])
    
    def test_polygonsorted_0(self):
        result = sort_points.PolygonSorted(self.shapes)
        result = [sort_points.get_area(i) for i in result]
        self.assertListEqual(result, [30, 64, 110])
    
    def test_polygonsorted_1(self):
        polys = np.random.rand(10000, 4, 2)
        xys = np.transpose(polys, (0, 2, 1))
        areas = [sort_points.PolyArea(*i) for i in xys]
        areas = sorted(areas)
        shapes = []
        for i in polys:
            poly = Shape()
            for j in i:
                j = j.tolist()
                poly.loadPoint(QPointF(*j))
            shapes.append(poly)
        result = sort_points.PolygonSorted(shapes)
        result = [sort_points.get_area(i) for i in result]
        self.assertListEqual(result, areas)
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(PolygonSortedTest('test_polyarea_0'))
    suite.addTest(PolygonSortedTest('test_polyarea_1'))
    suite.addTest(PolygonSortedTest('test_polyarea_2'))
    suite.addTest(PolygonSortedTest('test_get_area_0'))
    suite.addTest(PolygonSortedTest('test_polygonsorted_0'))
    suite.addTest(PolygonSortedTest('test_polygonsorted_1'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')