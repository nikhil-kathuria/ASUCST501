# TODO: Get rid of all flake8 warnings -- that means adding docstrings
#      to the file, classes, and methods.


class SinglyLinkedNode(object):

    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):

    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self._head = SinglyLinkedNode(None, None)
        self._length = 0
        pass

    def __len__(self):
        return self._length
        pass

    def __iter__(self):
        currentnode = self._head
        while currentnode._next is not None:
            yield currentnode._next
            currentnode = currentnode._next
        pass

    def __contains__(self, item):
        currentnode = self._head._next
        while currentnode is not None:
            if currentnode._item == item:
                return True
            currentnode = currentnode._next
        return False
        pass

    def remove(self, item):
        currentnode = self._head._next
        previous = self._head

        if currentnode is None:
            raise ValueError("list.remove(x): x not in list")

        elif currentnode._next is None and currentnode._item == item:
            self._head = SinglyLinkedNode()
            self._length -= 1
            return self

        while currentnode is not None:
            if currentnode._item == item:
                previous._next = currentnode._next
                self._length -= 1
                return self
            previous = currentnode
            currentnode = currentnode._next

        raise ValueError("list.remove(x): x not in list")
        pass

    def prepend(self, item):
        node = SinglyLinkedNode(item, None)
        currentnode = self._head
        nextnode = currentnode._next
        if currentnode._next is None:
            currentnode._next = node
        else:
            currentnode._next = node
            node._next = nextnode
        self._length += 1
        return self
        pass

    def __repr__(self):
        s = "List:" + "->".join([str(item) for item in self])
        return s


def test():
    list1 = SinglyLinkedList()
    list1.prepend(1).prepend(8).prepend(3).prepend(1)
    print list1.remove(1).remove(3).remove(1).remove(8)
    print list1.__contains__(8)
    print list1.__len__()
    '''gen = list1.__iter__()
    for itr in range(0, list1.__len__()):
        print gen.next()
    pass'''

if __name__ == '__main__':
    test()
