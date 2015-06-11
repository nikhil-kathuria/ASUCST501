# Import SinglyLinkedList Class for storing list in buckets
from SinglyLinkedList import SinglyLinkedList
import sys


'''
To calcuate the index of bucket where KeyValuePair object will added
we will user mutplication method. Multiplication and bit extraction
are faster than division/mod method

Multiplication Method:
h(k) = [(a * k) mod 2w] >> (w -r), where
>> denotes the bit shift operator
2^r us the table size (=m)
w the bit-length of machine words
and A is chosen to be odd integer between 2^(w-1) and 2^w
'''


def machine_word_size():
    num_bytes = 0
    maxint = sys.maxint
    while maxint > 0:
        maxint = maxint >> 1
        num_bytes += 1
    return num_bytes


'''On 64 bit machines W comes as 63 due to one bit for sign bit the maximum
word we can expect 2^63. Similarly on 32 bit machines W comes as 31'''
W = machine_word_size()


'''Assign value to A based on bit length of word. We have chose A to be a odd
integer between 2^(w-1) and 2^w in both cases.'''
if W == 63:
    A = 922337209247
elif W == 31:
    A = 3294967303
else:
    raise ValueError("Bit length of machine word expected either {64, 32}")


class _KeyValuePair(object):

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


class ChainedHashDict(object):

    def __init__(self, bin_count=8, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self._table = [None] * bin_count
        self._maxload = max_load
        pass

    @property
    def load_factor(self):
        return len(self) / float(len(self._table))
        pass

    @property
    def bin_count(self):
        return len(self._table)
        pass

    def poweroftwo(self, num):
        num_bytes = 0
        while num != 1:
            num = num >> 1
            num_bytes += 1
        return num_bytes

    def hashcomp(self, key, length):
        mask = sys.maxint - 1
        r = self.poweroftwo(length)
        idx = (hash(key) * A) & mask >> W - r
        return idx

    def rebuild(self, bincount):
        # Rebuild this hash table with a new bin count
        newtable = [None] * bincount
        for itr in xrange(0, len(self._table)):
            if self._table[itr] is not None:
                currentlist = iter(self._table[itr])
                for currentnode in currentlist:
                    kvp = _KeyValuePair(currentnode._item.key, currentnode._item.value)
                    index = self.hashcomp(currentnode._item.key, len(newtable))
                    if newtable[index] is None:
                        newtable[index] = SinglyLinkedList().prepend(kvp)
                    else:
                        newtable[index].prepend(kvp)
        self._table = newtable
        pass

    def __getitem__(self, key):
        index = self.hashcomp(key, len(self._table))
        if self._table[index] is None:
            raise KeyError("no such key: {0!r}".format(key))
        else:
            currentlist = iter(self._table[index])
            for currentnode in currentlist:
                if currentnode._item.key == key:
                    return currentnode._item.value
        raise KeyError("no such key: {0!r}".format(key))
        pass

    def __setitem__(self, key, value):
        kvp = _KeyValuePair(key, value)
        index = self.hashcomp(key, len(self._table))
        if self._table[index] is None:
            self._table[index] = SinglyLinkedList().prepend(kvp)
        else:
            currentlist = iter(self._table[index])
            for currentnode in currentlist:
                if currentnode._item.key == key:
                    currentnode._item.value = value
                    return
            self._table[index].prepend(kvp)
        # Check load factor
        if self.load_factor >= self._maxload:
            self.rebuild(2 * len(self._table))
        pass

    def __delitem__(self, key):
        index = self.hashcomp(key, len(self._table))
        kvplist = self._table[index]
        itematkey = None
        if kvplist is None:
            raise KeyError("no such key: {0!r}".format(key))
        else:
            currentlist = iter(self._table[index])
            for currentnode in currentlist:
                if currentnode._item.key == key:
                    itematkey = currentnode.item
                    kvplist.remove(itematkey)
                    return
            raise KeyError("no such key: {0!r}".format(key))
        pass

    def __contains__(self, key):
        index = self.hashcomp(key, len(self._table))
        if self._table[index] is None:
            return False
        else:
            currentlist = iter(self._table[index])
            for currentnode in currentlist:
                if currentnode._item.key == key:
                        return True
        return False
        pass

    def __len__(self):
        length = 0
        for itr in range(0, len(self._table)):
            if self._table[itr] is not None:
                length += len(self._table[itr])
        return length
        pass

    def display(self):
        print "In display ChainedHashDict"
        print "Occupied Length of Hastable : " + str(len(self))
        print "Load Factor : " + str(self.load_factor)
        string = ""
        for itr in range(0, len(self._table)):
            string += str(itr) + ": "
            string += str(self._table[itr]) + "\n"
        print string
        pass


def test():
    hashex = ChainedHashDict()
    hashex.__setitem__(30, "Raze")
    hashex.__setitem__(20, "Maze")
    hashex.__setitem__(32, "killJoy")
    hashex.__setitem__("Game", "Igot")
    hashex.__setitem__(46, "loop")
    hashex.__setitem__("Hell", "Boy")
    # hashex.display()
    hashex.__setitem__(48, "Igot")
    hashex.__setitem__(50, "Igot")
    print(hashex.__contains__(30))
    hashex.__delitem__(48)
    hashex.__delitem__(46)
    print hashex.__getitem__(30)
    print len(hashex)
    hashex.display()
    # hash.rebuild(20)
    pass

if __name__ == '__main__':
    test()
