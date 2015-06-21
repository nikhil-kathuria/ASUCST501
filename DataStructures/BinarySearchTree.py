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


class BinaryTreeNode(object):

    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

    def nodeheight(self, node):
        if node is None:
            return 0
        if node.left and node.right is None:
            return 0
        else:
            max(self.nodeheight(node.left), self.nodeheight(node.right)) + 1

    def __repr__(self):
        return str(self.data)


class BinarySearchTree(object):

    def __init__(self):
        super(BinarySearchTree, self).__init__()
        self.root = None
        # TODO initialize
        pass

    # @property
    def height(self):
        rootnode = self.root
        if rootnode is None:
            return 0
        else:
            return rootnode.nodeheight(rootnode) + 1
        pass

    '''
    Iterative inorder walk we require a stack to store elements which we have
    encountered but we cannot yield them as they are not the lowest element in
    tree.

    1. We start by reachig the leftmost(minimum) element and storing all
    elements encountered yet.

    2. We yield the node and check if the current node has any right children.
    If it does not have this means we need to pop the topmost element from
    stack element from stack and treat as current node

    3. If the current node has right children we allocate current node as right
    children and check for left again as we started for the root node.

    4. Lastly when we do not have any right node and stack lenght is zero then
    we know that we have processed all the elements of tree.
    '''
    def itrerative_inorder(self):
        rootnode = self.root
        stack = []
        while rootnode is not None:
            while rootnode.left is not None:
                stack.append(rootnode)
                rootnode = rootnode.left
            yield rootnode.data
            while rootnode.right is None:
                if len(stack) != 0:
                    rootnode = stack.pop()
                    yield rootnode.data
                else:
                    return
            rootnode = rootnode.right
        pass

    '''
    Iterative preorder walk we require a stack to store righr and left child
    nodes till they get poped

    1. We start by adding rootnode to stack. First popping rootnode, yielding
    data and then pushing right and left child on stack as they exist.

    2. The topmost element of stack either left or right node depending rootnode's
    child goes throught above procedure

    3. This process continues till the last element is poped with no child.
    '''
    def itrerative_preorder(self):
        rootnode = self.root
        if rootnode is None:
            return
        stack = []
        stack.append(rootnode)
        while len(stack) != 0:
            rootnode = stack.pop()
            yield rootnode.data
            if rootnode.right:
                stack.append(rootnode.right)
            if rootnode.left:
                stack.append(rootnode.left)
        pass

    '''
    In postorder we visit the left child of node first then right child of node
    and then visit the node. This property holds recursiverly till we have
    reached a node with no child and then we need to backtrack.

    For iteratuve walk we require a stack to store the nodes which are not
    processd completely. The top of our stack is the current node at all times

    Since we visit either child first we keep appending to stack and traversing
    down. Once we confirm a node with no child we traverse up i.e.backtrack and
    stack property helps in backtracking.

    Moreover we require a pointer for previously visted node. We update the
    previous node poiter at end of while loop which holds true till stack is
    not empty.
    1. To know we are travering up the tree from left
        -> When we traverse up left of the tree we need to check the current
           node has right child or not. If it has we append right chid otherwise
           we pop stack to eliminate fully seen nodes and print current node's 
           data to fully process the node
    2. To know we are traversing up the tree from right
        -> When we traverse up right of tree we need to only pop the stack as
           we always visit the left child first so we have fully seen the node
           so pop it print current node's data to fully process node.
    '''
    def itrerative_postorder(self):
        rootnode = self.root
        if rootnode is None:
            return
        # Use list as stack by calling append and pop methods only
        stack = []
        prvnod = None
        stack.append(rootnode)
        while len(stack) != 0:
            # Mimic peek() for stack i.e. assign curent element without poping
            curnod = stack[len(stack) - 1]
            # When we are traversing down the tree
            if (not prvnod or prvnod.left == curnod or prvnod.right == curnod):
                if curnod.left:
                    stack.append(curnod.left)
                elif curnod.right:
                    stack.append(curnod.right)
                # This node has no child
                else:
                    stack.pop()
                    yield curnod.data
            # When we are traversing up the tree from left
            elif curnod.left == prvnod:
                if curnod.right:
                    stack.append(curnod.right)
                '''
                In case of else the current node has no right child means the
                node is fully seen and now we can pop and yield current node's
                data. This is similar to case when node we are traversing up
                the tree from right. So we have combined both in single else.
                '''
            # When we are traversing up the tree from right
            else:
                stack.pop()
                yield curnod.data
            prvnod = curnod
        pass

    def items(self):
        keyset = self.inorder_keys()
        for nodecount in keyset:
            yield (nodecount.data._key, nodecount.data._value)
        pass

    def __getitem__(self, key):
        rootnode = self.root
        while rootnode is not None:
            if rootnode.data._key == key:
                return rootnode.data._value
            elif rootnode.data._key > key:
                rootnode = rootnode.right
            elif rootnode.data._key < key:
                rootnode = rootnode.left
        pass

    def __setitem__(self, data):
        itr = None
        rootnode = self.root
        # data = _KeyValuePair(key, value)
        intrm = BinaryTreeNode(data, None, None, None)
        while rootnode is not None:
            itr = rootnode
            if intrm.data < rootnode.data:
                rootnode = rootnode.left
            else:
                rootnode = rootnode.right
        intrm.parent = itr
        if itr is None:
            self.root = intrm
        elif intrm.data < itr.data:
            itr.left = intrm
        else:
            itr.right = intrm
        pass

    def __delitem__(self, key):
        # TODO
        pass

    def __contains__(self, key):
        rootnode = self.root
        while rootnode is not None:
            if rootnode.data._key == key:
                return True
            elif rootnode.data._key < key:
                rootnode = rootnode.right
            elif rootnode.data._key > key:
                rootnode = rootnode.left
        return False
        pass

    def __len__(self):
        nodecount = 0
        keyset = self.inorder_keys()
        for nodecount in keyset:
            nodecount += 1
        return nodecount
        pass

    def display(self):
        print "Inorder tree traversal"
        print 'Inorder:', ','.join(item for item in self.inorder_keys())
        print "\n" + "Postorder tree traversal"
        print 'Postorder:', ','.join(item for item in self.inorder_keys())
        pass


def main():
    test()


def test():
    keyset = [42, 40, 43, 37, 46, 36, 49]
    # smallkey = [42, 40, 43]
    bst = BinarySearchTree()
    for key in keyset:
        bst.__setitem__(key)
    # print bst.root.data
    # print bst.root.left.data
    # print bst.root.right.data
    for node in bst.itrerative_postorder():
        print node


if __name__ == '__main__':
    main()
