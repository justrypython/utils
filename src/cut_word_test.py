#encoding:UTF-8

import os
import unittest
import cut_word

class CutWordTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_0(self):
        s0 = 'thumbgreenappleactiveassignmentweeklymetaphor'
        s1 = cut_word.infer_spaces(s0)
        self.assertEqual(s1, 'thumb green apple active assignment weekly metaphor')
    
    def test_1(self):
        s0 = 'femaleapplicants'
        s1 = cut_word.infer_spaces(s0)
        self.assertEqual(s1, 'female applicants')
    
    def test_2(self):
        s0 = 'IhadanadvantageOver'.lower()
        s1 = cut_word.infer_spaces(s0)
        self.assertEqual(s1, 'i had an advantage over')
    
    def test_3(self):
        s0 = 'maleIhadanadvantageOver'.lower()
        s1 = cut_word.infer_spaces(s0)
        self.assertEqual(s1, 'male i had an advantage over')
        
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(CutWordTest('test_0'))
    suite.addTest(CutWordTest('test_1'))
    suite.addTest(CutWordTest('test_2'))
    suite.addTest(CutWordTest('test_3'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')