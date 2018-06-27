#encoding:UTF-8
#author:justry

import os
import string

class Trie:

    def __init__(self):
        self.path = {}
        self.value = None
        self.value_valid = False

    def __setitem__(self, key, value):
        head = key[0]
        if head in self.path:
            node = self.path[head]
        else:
            node = Trie()
            self.path[head] = node

        if len(key) > 1:
            remains = key[1:]
            node.__setitem__(remains, value)
        else:
            node.value = value
            node.value_valid = True

    def __delitem__(self, key):
        head = key[0]
        if head in self.path:
            node = self.path[head]
            if len(key) > 1:
                remains = key[1:]
                node.__delitem__(remains)
            else:
                node.value_valid = False
                node.value = None
            if len(node) == 0:
                del self.path[head]

    def __getitem__(self, key):
        head = key[0]
        if head in self.path:
            node = self.path[head]
        else:
            raise KeyError(key)
        if len(key) > 1:
            remains = key[1:]
            try:
                return node.__getitem__(remains)
            except KeyError:
                raise KeyError(key)
        elif node.value_valid:
            return node.value
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        return True

    def __len__(self):
        n = 1 if self.value_valid else 0
        for k in self.path.keys():
            n = n + len(self.path[k])
        return n

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def nodeCount(self):
        n = 0
        for k in self.path.keys():
            n = n + 1 + self.path[k].nodeCount()
        return n

    def keys(self, prefix=[]):
        return self.__keys__(prefix)

    def __keys__(self, prefix=[], seen=[]):
        result = []
        if self.value_valid:
            isStr = True
            val = ""
            for k in seen:
                if type(k) != str or len(k) > 2:
                    isStr = False
                    break
                else:
                    val += k
            if isStr:
                result.append(val)
            else:
                result.append(seen)
        if len(prefix) > 0:
            head = prefix[0]
            prefix = prefix[1:]
            if head in self.path:
                nextpaths = [head]
            else:
                nextpaths = []
        else:
            nextpaths = self.path.keys()                
        for k in nextpaths:
            nextseen = []
            nextseen.extend(seen)
            nextseen.append(k)
            result.extend(self.path[k].__keys__(prefix, nextseen))
        return result

    def __iter__(self):
        for k in self.keys():
            yield k
        #raise StopIteration

    def __add__(self, other):
        result = Trie()
        result += self
        result += other
        return result

    def __sub__(self, other):
        result = Trie()
        result += self
        result -= other
        return result

    def __iadd__(self, other):
        for k in other:
            self[k] = other[k]
        return self

    def __isub__(self, other):
        for k in other:
            del self[k]
        return self
    
    def get_similar(self, s):
        similar_s, similar_s2 = similar(s)
        ret = self._get_similar(similar_s, s)
        if ret != s:
            return ret
        ret = self._get_similar(similar_s2, s)
        return ret

    def _get_similar(self, similar_s, s):
        ret = s
        cnt = 0
        for i in similar_s:
            if not i:
                continue
            if i in self:
                newcnt = self[i]
                if newcnt > cnt:
                    cnt = newcnt
                    ret = i
        return ret

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def similar_insert(s, ax):
    ret = []
    for i in string.ascii_lowercase:
        ret.append(s[:ax]+i+s[ax:])
    return ret

def similar_change(s, ax):
    ret = []
    for i in string.ascii_lowercase:
        ret.append(s[:ax]+i+s[ax+1:])
    return ret

def similar_change_2(s, ax):
    ret = []
    for i in string.ascii_lowercase:
        ret.append(s[:ax]+i+s[ax+2:])
    return ret

def similar_delete(s, ax):
    return [s[:ax]+s[ax+1:]]

def similar(s):
    ret = []
    ret2 = []
    ret.extend(similar_insert(s, len(s)+1))
    for i in range(len(s), -1, -1):
        ret.extend(similar_insert(s, i))
        ret.extend(similar_change(s, i))
        ret.extend(similar_delete(s, i))
    for i in range(len(s)):
        ret2.extend(similar_change_2(s, i))
    return [i for i in ret if i != s], ret2

class EngCorrect(object):
    
    def __init__(self, filepath):
        self.trie = Trie()
        self._load(filepath)

    def _load(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines = [i.replace('\n', '') for i in lines]
        for i in lines:
            a, b = i.split()
            b = int(b)
            self.trie[a] = b
        
    def __contains__(self, s):
        return s in self.trie
        
    def get_similar(self, s):
        s = ''.join([i for i in s if i not in string.punctuation])
        return self.trie.get_similar(s)

if __name__ == '__main__':
    import datetime
    from autocorrect import spell
    from ocr_correct import o_0, uppercase_lowercase

    file_path = "engwordlist.txt"
    start_time = datetime.datetime.now()
    trie = EngCorrect(file_path)
    end_time = datetime.datetime.now()
    print('\n')
    print('load time is ', end_time - start_time)

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
        for j in i.split():
            ret1.append(spell(j))
            if j in trie:
                ret.append(j)
            else:
                ret.append(trie.get_similar(j))
        print(' '.join(ret))
        print(' '.join(ret1))
        print('#'*70)