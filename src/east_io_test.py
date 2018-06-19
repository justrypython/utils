#encoding:UTF-8
#author:justry

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import unittest
from east_io import EastReader, EastWriter, PolyArea, get_area, PolygonSorted,\
     boxIsInBox, getParaBox


class FuncTest(unittest.TestCase):
    
    def setUp(self):
        p0 = [[0, 0], [10, 0], [10, 11], [0, 11]]
        p1 = [[1, 1], [9, 1], [9, 9], [1, 9]]
        p2 = [[2, 2], [8, 2], [8, 7], [2, 7]]
        self.shapes = [p0, p1, p2]
    
    def tearDown(self):
        del self.shapes
    
    def test_polyarea_0(self):
        x = [0, 1, 1, 0]
        y = [0, 0, 1, 1]
        result = PolyArea(x, y)
        self.assertEqual(result, 1)
    
    def test_polyarea_1(self):
        x = [0, 2, 1, 0]
        y = [0, 0, 1, 1]
        result = PolyArea(x, y)
        self.assertEqual(result, 1.5)
    
    def test_polyarea_2(self):
        x = [0, 1, 0]
        y = [0, 0, 1]
        result = PolyArea(x, y)
        self.assertEqual(result, 0.5)
    
    def test_get_area_0(self):
        result = []
        for i in self.shapes:
            result.append(get_area(i))
        self.assertListEqual(result, [110, 64, 30])
    
    def test_polygonsorted_0(self):
        shapes = []
        for i in self.shapes:
            shapes.append({'upperleft':i[1],
                           'upperright':i[0],
                           'lowerright':i[3], 
                           'lowerleft':i[2]})
        result = PolygonSorted(shapes)
        result = [get_area([i['upperleft'],
                            i['upperright'],
                            i['lowerright'],
                            i['lowerleft']]) for i in result]
        self.assertListEqual(result, [30, 64, 110])
    
    def test_polygonsorted_1(self):
        polys = np.random.rand(10000, 4, 2)
        xys = np.transpose(polys, (0, 2, 1))
        areas = [PolyArea(*i) for i in xys]
        areas = sorted(areas)
        shapes = []
        for i in polys:
            shapes.append({'upperleft':i[1],
                           'upperright':i[0],
                           'lowerright':i[3], 
                           'lowerleft':i[2]})
        result = PolygonSorted(shapes)
        result = [get_area([i['upperleft'],
                            i['upperright'],
                            i['lowerright'],
                            i['lowerleft']]) for i in result]
        results = np.array(result) - np.array(areas)
        theta = 1e-9
        self.assertTrue(np.all(results<theta))
    
    def test_boxisinbox(self):
        a = [[0, 0], [10, 0], [10, 10], [0, 10]]
        b = [[0, 0], [20, 0], [20, 20], [0, 20]]
        c = [[30, 30], [40, 30], [40, 40], [30, 40]]
        self.assertTrue(boxIsInBox(a, a))
        self.assertTrue(boxIsInBox(b, b))
        self.assertTrue(boxIsInBox(c, c))
        self.assertTrue(boxIsInBox(a, b))
        self.assertFalse(boxIsInBox(a, c))
        self.assertFalse(boxIsInBox(b, a))
        self.assertFalse(boxIsInBox(b, c))
        self.assertFalse(boxIsInBox(c, a))
        self.assertFalse(boxIsInBox(c, b))
        
    def test_getparabox(self):
        a = [[0, 0], [10, 0], [10, 10], [0, 10]]
        b = [[0, 0], [20, 0], [20, 20], [0, 20]]
        c = [[30, 30], [40, 30], [40, 40], [30, 40]]
        labels = ['upperleft', 'upperright', 'lowerright', 'lowerleft']
        a = {i[0]:i[1] for i in zip(labels, a)}
        b = {i[0]:i[1] for i in zip(labels, b)}
        c = {i[0]:i[1] for i in zip(labels, c)}
        box = getParaBox(a, [b, c])
        self.assertDictEqual(box, b)

class EastWriterTest(unittest.TestCase):
    
    def setUp(self):
        self.eastwriter = EastWriter('', 'east_write', (0, 0))
    
    def tearDown(self):
        pass
    
    def test_0(self):
        self.eastwriter.addRegion([0, 0], [10, 0], [10, 10], [0, 10], 'box1', '0')
        self.eastwriter.addRegion([0, 0], [20, 0], [20, 20], [0, 20], 'box2', '0')
        self.eastwriter.addRegion([30, 30], [40, 30], [40, 40], [30, 40], 'box3', '0')
        self.eastwriter.save()
        self.eastreader = EastReader('east_write.txt')
        points = [i[1] for i in self.eastreader.shapes]
        self.assertListEqual([[[0, 0], [10, 0], [10, 10], [0, 10]],
                              [[0, 0], [20, 0], [20, 20], [0, 20]],
                              [[30, 30], [40, 30], [40, 40], [30, 40]]], points)
        
    def test_1(self):
        boxes = []
        for i in range(1000):
            for j in range(4):
                p1 = np.random.randint(1, 100, [2], dtype=np.int)
                p2 = p1 + [np.random.randint(1, 100), 0]
                p3 = p2 + [0, np.random.randint(1, 100)]
                p4 = p3 - [np.random.randint(1, 100), 0]
                p4 = np.clip(p4, (0, 0), (400, 400))
            boxes.append([p1.tolist(), p2.tolist(), p3.tolist(), p4.tolist()])
            self.eastwriter.addRegion(p1.tolist(), p2.tolist(), p3.tolist(), p4.tolist(), 
                                      str(i), '0')
        self.eastwriter.save()
        self.eastreader = EastReader('east_write.txt')
        points = [i[1] for i in self.eastreader.shapes]
        boxes = sorted(boxes, key=lambda i:i[0])
        boxes = sorted(boxes, key=lambda i:i[1])
        boxes = sorted(boxes, key=lambda i:i[2])
        boxes = sorted(boxes, key=lambda i:i[3])
        points = sorted(points, key=lambda i:i[0])
        points = sorted(points, key=lambda i:i[1])
        points = sorted(points, key=lambda i:i[2])
        points = sorted(points, key=lambda i:i[3])
        self.assertListEqual(boxes, points)
        

class EastReaderTest(unittest.TestCase):
    
    def setUp(self):
        self.eastio = EastReader('east_reader.txt')
    
    def tearDown(self):
        pass
    
    def test_0(self):
        pass
    

def suite():
    suite = unittest.TestSuite()
    # FuncTest
    suite.addTest(FuncTest('test_polyarea_0'))
    suite.addTest(FuncTest('test_polyarea_1'))
    suite.addTest(FuncTest('test_polyarea_2'))
    suite.addTest(FuncTest('test_get_area_0'))
    suite.addTest(FuncTest('test_polygonsorted_0'))
    suite.addTest(FuncTest('test_polygonsorted_1'))
    suite.addTest(FuncTest('test_boxisinbox'))
    suite.addTest(FuncTest('test_getparabox'))
    # EastWriter
    suite.addTest(EastWriterTest('test_0'))
    suite.addTest(EastWriterTest('test_1'))
    # EastReader
    suite.addTest(EastReaderTest('test_0'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')