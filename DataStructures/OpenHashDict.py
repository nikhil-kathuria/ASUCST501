# Import unit test import unittest

# Set Global parameters for hash
'''
The idea is to have some values to act as dummy values
These values can be assigned so that the value referenced by key can
be given special treatment. Like deleted keys can be marked dummy and in lookup
these values can be ignored so that we are able to probe to all slot index
pointed by hash function
'''
DUMMY = "[DuMmY_Val]"


'''
Set the shift value to 5. This helps in creating a balance of bits invloved
in mask operation both when the table size is small or large and a recurrence
over all index of Table
'''
PERTURB_SHIFT = 5


class _KeyValuePair(object):

    '''
A class to hold the key and corresponding value. The object is stored
at the slot pointed by hash function
'''

    def __init__(self, key, value):
        super(_KeyValuePair, self).__init__()
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, next):
        self._next = next

    def __repr__(self):
        return "(" + str(self._key) + ", " + str(self._value) + ")"


class OpenAddressHashDict(object):

    ''' The main class implementing the the OpenAddressing HashDict
The initial size for hash table chosen is 8 this is because we want our mask
(which helps to wrap around the index value generated within the length of
hash table) to be len -1 = 8 -1 = 7 i.e. in binary 111.

The Max load factor is .7 i.e. 70 %. If the table occupancy reaches or crosses
70% threshold then we double the length of hash table. This is done to ensure
for two reasons
1. The insert funtion should either find a empty slot at all times
2. The average of number of probes drastically increases as we reach the state
of table being full i.e. the lookup slows down and speed of hash/dict depends
on finding the key location on near constant time i.e. O(1)
'''

    def __init__(self, bin_count=8, max_load=0.7):
        super(OpenAddressHashDict, self).__init__()
        self._used = 0
        self._dummy = 0
        self._table = [None] * bin_count
        self._maxload = max_load
        pass

    @property
    def _load_factor(self):
        return (self._used + self._dummy) / float(len(self._table))
        pass

    @property
    def _bin_count(self):
        return len(self._table)
        pass

    def __len__(self):
        return self._used
        pass

    def _kvplist(self):
        kvlist = list()
        for itr in range(0, len(self._table)):
            if self._table[itr] is not None:
                if self._table[itr]._value != DUMMY:
                    kvlist.add(self._table[itr]._key, self._table[itr]._value)
        return kvlist

    def _index_gen(self, key, length):
        '''
        A generator function for getting the next index produced by hash
        function. Since if current yielded index does not satisfy the
        calling funtion requirement ; the calling function can fetch next
        value from by calling next() on generator object
        '''
        mask = length - 1
        perturb = hash(key)
        i = perturb & mask
        yield i
        while True:
            i = ((i << 2) + i + perturb + 1)
            perturb >>= PERTURB_SHIFT
            yield i & mask

    def _lookup(self, key):
        '''
        Since we have HashDict always 30 % free and our hashfunction
        will generate all the possible idex of Table we are guaranteed that
        either we will return None or non dummy value.
        Note that dummy value counts toward occupancy of Table.
        '''
        gen_obj = self._index_gen(key, len(self._table))
        while True:
            idx = gen_obj.next()
            if self._table[idx] is None:
                return None
            elif self._table[idx]._key == key:
                    if self._table[idx]._value != DUMMY:
                        return self._table[idx]

    def _insert(self, kvp):
        '''
        Inserts a KeyValuePair object in Table
        '''
        key = kvp._key
        gen_obj = self._index_gen(key, len(self._table))
        while True:
            idx = gen_obj.next()
            if self._table[idx] is None:
                self._table[idx] = kvp
                self._used += 1
                return None
            elif self._table[idx]._key == key:
                self._table[idx] = kvp
                self._used += 1
                return None

    def _rebuild(self, bincount):
        '''
        Rebuild this HashDict with new bincount. The dummy count is restored
        to zero once we have iterated over all index of old table. The table
        index with None or kvp node having value as DUMMY are ignored. The
        lookup function is expected to return an index even if there is
        colloision in newtable as the key of oldnode will be different than
        colloision node due to unique keys property of Hash maintained
        throughout implementation.
        '''
        newtable = [None] * bincount
        oldtable = self._table
        self._table = newtable
        self._used = 0
        self._dummy = 0
        for itr in xrange(0, len(oldtable)):
            oldnode = oldtable[itr]
            if oldnode is not None and oldnode._value != DUMMY:
                self._insert(oldnode)
        pass

    def __getitem__(self, key):
        if __debug__:
            if key is None:
                raise AssertionError("None cannot be key")
        idx = self._lookup(key)
        if idx is None:
            raise KeyError("no such key: {0!r}".format(key))
        else:
            return idx._value
        pass

    def __setitem__(self, key, value):
        if __debug__:
            if key is None or value is None:
                raise AssertionError("None cannot be key or value")
            if value == DUMMY:
                raise AssertionError("<" + DUMMY + "> Cannot be value")
        '''self.assertFalse(, "None cannot be key")
        self.assertFalse(value is None, "None cannot be value")
        self.assertFalse(value == DUMMY, "<" + DUMMY + "> Cannot be value")'''
        kvp = _KeyValuePair(key, value)
        self._insert(kvp)
        if self._load_factor >= self._maxload:
            if self._used > 5000:
                self._rebuild(2 * len(self._table))
            else:
                self._rebuild(4 * len(self._table))
        pass

    def __delitem__(self, key):
        if __debug__:
            if key is None:
                raise AssertionError("None cannot be key")
        idx = self._lookup(key)
        if idx is None:
            raise KeyError("no such key: {0!r}".format(key))
        elif idx._key == key:
            idx._value = DUMMY
            self._dummy += 1
            self._used -= 1
        pass

    def __contains__(self, key):
        if __debug__:
            if key is None:
                raise AssertionError("None cannot be key")
        idx = self._lookup(key)
        if idx is None:
            return False
        elif idx._key == key:
            return True
        pass

    def __repr__(self):
        r = ["{0!r} : {1!r}".format(k, v) for k, v in self._kvplist()]
        return "Dict({" + ", ".join(r) + "})"

    def _display(self):
        print "In display ChainedHashDict"
        print "Occupied Length of Hashtable : " + str(len(self))
        print "Load Factor : " + str(self._load_factor)
        string = ""
        print "In display OpenAddressHashDict"
        for itr in range(0, len(self._table)):
            string += str(itr) + ": "
            string += str(self._table[itr]) + "\n"
        print string
        pass


def test():
    hashex = OpenAddressHashDict()
    hashex.__setitem__(30, "Jade")
    hashex.__setitem__(20, "SubZero")
    hashex.__setitem__(32, "killjoy")
    hashex.__setitem__(45, "Igot")
    hashex.__setitem__(46, "heat")
    hashex.__setitem__(47, "streak")
    hashex.__setitem__("timon", "1")
    hashex.__setitem__("Pumba", "2")
    print hashex.__contains__(30)
    hashex._display()
    hashex.__delitem__(20)
    print hashex.__getitem__(30)
    print hashex.__len__()
    pass

if __name__ == '__main__':
    test()
