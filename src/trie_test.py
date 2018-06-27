#!/usr/bin/python -B

import datetime
import string
import unittest
from autocorrect import spell
from ocr_correct import o_0, uppercase_lowercase
from trie import Trie, levenshteinDistance, similar_insert
from trie import similar_change, similar_delete, similar
from trie import similar_change_2


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

    def _square_brackets(self, key):
        return self.trie[key]

    def test_basicAssignment(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEqual(1, len(self.trie))
        self.assertEqual(3, self.trie.nodeCount())
        self.assertTrue("Foo" in self.trie)
        self.trie["Bar"] = None
        self.assertTrue("Bar" in self.trie)

    def test_basicRemoval(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        del self.trie["Foo"]
        self.assertRaises(KeyError, self._square_brackets, "Foo")
        self.assertEqual(0, len(self.trie))
        self.assertEqual(0, self.trie.nodeCount())
        self.assertFalse("Foo" in self.trie)

    def test_MixedTypes(self):
        self.trie["Foo"] = True
        self.trie[[1, 2, 3]] = True
        self.assertTrue(self.trie["Foo"])
        self.assertTrue(self.trie[[1, 2, 3]])
        self.assertTrue([1, 2, 3] in self.trie)
        self.assertTrue("Foo" in self.trie)
        del self.trie[[1, 2, 3]]
        self.assertFalse([1, 2, 3] in self.trie)

    def test_Iteration(self):
        self.trie["Foo"] = True
        self.trie["Bar"] = True
        self.trie["Grok"] = True
        for k in self.trie:
            self.assertTrue(k in self.trie)
            self.assertTrue(self.trie[k])

    def test_Addition(self):
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        t3 = t2 + self.trie
        self.assertTrue("Foo" in self.trie)
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertFalse("Foo" in t2)
        self.assertTrue("Foo" in t3)
        self.assertTrue("Food" in t3)

    def test_Subtraction(self):
        self.trie["Food"] = True
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        t3 = self.trie - t2
        t4 = t2 - self.trie
        self.assertTrue("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertTrue("Foo" in t3)
        self.assertFalse("Food" in t3)
        self.assertFalse("Foo" in t4)
        self.assertFalse("Food" in t4)

    def test_SelfAdd(self):
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        self.assertTrue("Foo" in self.trie)
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertFalse("Foo" in t2)
        self.trie += t2
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in self.trie)

    def test_SelfSub(self):
        self.trie["Foo"] = True
        self.trie["Food"] = True
        t2 = Trie()
        t2["Food"] = True
        self.assertTrue("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)
        self.trie -= t2
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)

    def test_SelfGet(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEqual("Bar", self.trie.get("Food", "Bar"))
        self.assertEqual("Bar", self.trie.get("Food", default="Bar"))
        self.assertTrue(self.trie.get("Foo"))
        self.assertTrue(self.trie.get("Food") is None)

    def test_KeysByPrefix(self):
        self.trie["Foo"] = True
        self.trie["Food"] = True
        self.trie["Eggs"] = True
        kset = self.trie.keys()
        self.assertTrue("Foo" in kset)
        self.assertTrue("Food" in kset)
        self.assertTrue("Eggs" in kset)        
        kset = self.trie.keys("Foo")        
        self.assertTrue("Foo" in kset)
        self.assertTrue("Food" in kset)
        kset = self.trie.keys("Ox")
        self.assertEqual(0, len(kset))
        
    def test_getitem_0(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEqual("Bar", self.trie.get("Food", "Bar"))
        self.assertEqual("Bar", self.trie.get("Food", default="Bar"))
        self.assertTrue(self.trie.get("Foo"))
        self.assertTrue(self.trie.get("Food") is None)
        
    def test_keys_0(self):
        self.trie["Foo"] = True
        self.trie['Foodd'] = True
        a = self.trie.keys("Food")
        self.assertListEqual(a, ['Foo', 'Foodd'])
        a = self.trie.keys("Foot")
        self.assertListEqual(a, ['Foo'])
        a = self.trie.keys("Fot")
        
    def test_get_similar(self):
        self.trie["Foo"] = True
        self.trie['Foodd'] = True
        a = self.trie.get_similar('Food')
        self.assertEqual(a, 'Foodd')
        a = self.trie.get_similar('Foot')
        self.assertEqual(a, 'Foo')
        

class SimilarTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_insert_0(self):
        s = 'foot'
        for i in range(len(s)+1):
            ss = similar_insert(s, i)
            for j in ss:
                d = levenshteinDistance(j, s)
                self.assertEqual(d, 1)
    
    def test_change_0(self):
        s = 'foot'
        for i in range(len(s)):
            ss = similar_change(s, i)
            for j in ss:
                if j != s:
                    d = levenshteinDistance(j, s)
                    self.assertEqual(d, 1)
    
    def test_change_1(self):
        s = 'foot'
        ss = []
        for i in range(len(s)-1):
            ss.extend(similar_change_2(s, i))
        ss_d = [levenshteinDistance(s, i) for i in ss]
        print(ss_d)
    
    def test_delete_0(self):
        s = 'foot'
        ss = []
        for i in range(len(s)):
            ss.extend(similar_delete(s, i))
        self.assertListEqual(['oot', 'fot', 'fot', 'foo'], ss)
    
    def test_similar_0(self):
        s = 'foot'
        a = similar(s)
        self.assertTrue(1)
        

class LevenshteinDistanceTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_0(self):
        s1 = 'string1'
        s2 = 'string2'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 1)
    
    def test_1(self):
        s1 = 'string1'
        s2 = 'string1'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 0)
    
    def test_2(self):
        s1 = 'string1'
        s2 = 'string'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 1)
    
    def test_3(self):
        s1 = 'strnig1'
        s2 = 'string1'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 2)
    
    def test_4(self):
        s1 = 'ring1'
        s2 = 'string1'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 2)
    
    def test_5(self):
        s1 = 'sting1'
        s2 = 'string1'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 1)
    
    def test_6(self):
        s1 = 'tnultiple'
        s2 = 'multiple'
        d = levenshteinDistance(s1, s2)
        self.assertEqual(d, 2)
        
class CorrectTest(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        file_path = "engwordlist.txt"
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        start_time = datetime.datetime.now()
        lines = [i.replace('\n', '') for i in lines]
        for i in lines:
            a, b = i.split()
            b = int(b)
            self.trie[a] = b
        end_time = datetime.datetime.now()
        print('\n')
        print('load time is ', end_time - start_time)
            
    def tearDown(self):
        pass
    
    def test_0(self):
        start_time = datetime.datetime.now()
        for i in range(1000):
            a = self.trie.get_similar('similat')
        end_time = datetime.datetime.now()
        print('during time is ', end_time - start_time)
        print(a)
    
    def test_1(self):
        file_path = '9781601988157-summary14.result'
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i in lines:
            i = o_0(i)
            i = uppercase_lowercase(i)
            ret = []
            ret1 = []
            i = i.lower()
            print(i)
            i = ''.join([k for k in i if k not in string.punctuation])
            for j in i.split():
                ret1.append(spell(j))
                if j in self.trie:
                    ret.append(j)
                else:
                    ret.append(self.trie.get_similar(j))
            print(' '.join(ret))
            print(' '.join(ret1))
            print('#'*70)
    
    def test_2(self):
        s = 'hnation'
        ss = self.trie.get_similar(s)
        print(ss)
        s = 'wwith'
        ss = self.trie.get_similar(s)
        print(ss)
        s = 'thle'
        ss = self.trie.get_similar(s)
        print(ss)
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTrie('test_basicAssignment'))
    suite.addTest(TestTrie('test_basicRemoval'))
    suite.addTest(TestTrie('test_MixedTypes'))
    suite.addTest(TestTrie('test_Iteration'))
    suite.addTest(TestTrie('test_Addition'))
    suite.addTest(TestTrie('test_Subtraction'))
    suite.addTest(TestTrie('test_SelfAdd'))
    suite.addTest(TestTrie('test_SelfSub'))
    suite.addTest(TestTrie('test_SelfGet'))
    suite.addTest(TestTrie('test_KeysByPrefix'))
    suite.addTest(TestTrie('test_getitem_0'))
    suite.addTest(TestTrie('test_keys_0'))
    suite.addTest(TestTrie('test_get_similar'))
    suite.addTest(LevenshteinDistanceTest('test_0'))
    suite.addTest(LevenshteinDistanceTest('test_1'))
    suite.addTest(LevenshteinDistanceTest('test_2'))
    suite.addTest(LevenshteinDistanceTest('test_3'))
    suite.addTest(LevenshteinDistanceTest('test_4'))
    suite.addTest(LevenshteinDistanceTest('test_5'))
    suite.addTest(LevenshteinDistanceTest('test_6'))
    suite.addTest(SimilarTest('test_insert_0'))
    suite.addTest(SimilarTest('test_change_0'))
    suite.addTest(SimilarTest('test_change_1'))
    suite.addTest(SimilarTest('test_delete_0'))
    suite.addTest(SimilarTest('test_similar_0'))
    suite.addTest(CorrectTest('test_2'))
    suite.addTest(CorrectTest('test_0'))
    suite.addTest(CorrectTest('test_1'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')