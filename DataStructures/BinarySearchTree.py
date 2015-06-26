import sys

'''
Key Value pair class in case implementation requires key-value object
instead of primitive data type
'''


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


'''
BinaryTreeNode Class to store left, right, parent pointers as well
data field to hold data of primitive type in current implementation.
The data field can be another pointer field however most methods in
BinaryTreeNode and BinarySearchTree will also change
'''


class BinaryTreeNode(object):

    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        return str(self.data)

    '''
    Helping recursive function for postorder traversal. Recursion bottoms out
    for a brach/sub-tree when the node does not have either of children
    '''

    def nodeheight(self, node):
        if node is None:
            return 0
        return max(node.nodeheight(node.left), node.nodeheight(node.right)) + 1

    '''
    Helping recursive function for postorder traversal. Recursion bottoms out
    when root node has no unprocessed node
    '''

    def _rpostorder(self, node):
        if node.left:
            self._rpostorder(node.left)
        if node.right:
            self._rpostorder(node.right)
        print node.data

    '''
    Helping recursive function for preoder traversal. Recursion bottoms out
    when maxnode node is encountered.
    '''

    def _rpreorder(self, node):
        print node.data
        if node.left:
            self._rpreorder(node.left)
        if node.right:
            self._rpreorder(node.right)

    '''
    Helping recursive function for inoder traversal. Recursion bottoms out
    when maxnode node is encountered.
    '''

    def _rinorder(self, node):
        if node.left:
            self._rinorder(node.left)
        print node.data
        if node.right:
            self._rinorder(node.right)

    '''
    A helper function to print sub-tree. The None children are represnet with
    <.> and we proceed inorde traversal. We also encapsulate a node with with
    braces like starting { and closing } to represent a node is processed.

    The braces help in representing BST in way which is similar to human eye
    '''

    def printsubtree(self, node):
        sys.stdout.write("{")
        if node.left:
            self.printsubtree(node.left)
        else:
            sys.stdout.write(".")
            sys.stdout.write(node)
            if node.right:
                self.printsubtree(node.right)
            else:
                sys.stdout.write(".")
        sys.stdout.write("}")
        return

    '''
    If a node has right child then we are assured that right branch contains
    successor, now the minimum of right branch will be element bigger than
    node however smaller than all other nodes of branch so we have found node.

    If a node has no right child then the successor lies up the tree. So we
    move up the tree by swapping current node with parent till we encouter root
    i.e. node.parent is None. At any time the current node is left of parent
    means that the parent is the successor

    It is to be noted that the successor takes a pointer to the node as
    input. If pointer is not available then first we need to have the pointer
    which can be achieved by calling __getitem__ on BST instance.
    '''

    def successor(self):
        if self.right:
            minnode = self.right
            while minnode.left is not None:
                minnode = minnode.left
            return minnode
        else:
            node = self
            while node.parent is not None:
                if node.parent.left == node:
                    return node.parent
                node = node.parent
        return

    '''
    If a node has left child then we are assured that left branch contains
    predecessor, now the maximum of left branch will be element smaller than
    node however bigger than all other nodes of branch so we have found node.

    If a node has no left child then the predecessor lies up the tree. So we
    move up the tree by swapping current node with parent till encouter root
    i.e. node.parent is None. At any time the current node is right of parent
    means that the parent is the predecessor

    It is to be noted that the predecessor takes a pointer to the node as
    input. If pointer is not available then first we need to have the pointer
    which can be achieved by calling __getitem__ on BST instance.
    '''

    def predecessor(self):
        if self.left:
            maxnode = self.left
            while maxnode.right is not None:
                maxnode = maxnode.right
            return maxnode
        else:
            node = self
            while node.parent is not None:
                if node.parent.right == node:
                    return node.parent
                node = node.parent
        return


'''
BinarySearchTree to store pointer to root node and size field to store
number of nodes in BinarySearchTree
'''


class BinarySearchTree(object):

    # __init__ method to initialze the BinarySearchTree object
    def __init__(self, *args):
        super(BinarySearchTree, self).__init__()
        if len(args) == 0:
            self.root = None
            self.size = 0
        else:
            self.root = args[0]
            self.size = 1

    '''
    A helper function to print sub-tree. The None children are represnet with
    <.> and we proceed inorde traversal. We also encapsulate a node with with
    braces like starting { and closing } to represent a node is processed.

    The braces help in representing BST in way which is similar to human eye
    '''
    def __repr__(self):
        rootnode = self.root
        if rootnode is not None:
            rootnode.printsubtree(rootnode)

    # Caculates height of tree from root. Calls nodeheight on rootnode
    def height(self):
        curnod = self.root
        if curnod is None:
            return 0
        else:
            return curnod.nodeheight(curnod) + 1

    '''
    Gives back the node with minimum key value in BinarySearchTree. Traverse
    left of tree till finds None value. Returns the last Non-None value
    '''

    def min_tree(self):
        curnod = self.root
        while curnod.left:
            curnod = curnod.left
        return curnod

    '''
    Gives back the node with maximum key value in BinarySearchTree. Traverse
    right of tree till finds None value. Returns the last Non-None value
    '''

    def max_tree(self):
        curnod = self.root
        while curnod.right:
            curnod = curnod.right
        return curnod

    '''
    Prints the node.data in preorder. Calls helper function _rpreorder on
    rootnode. Does not give a generator object back
    '''

    def recursive_preorder(self):
        curnod = self.root
        if curnod is None:
            return
        else:
            return curnod._rpreorder(curnod)

    '''
    Prints the node.data in inorder. Calls helper function _rinorder on
    rootnode. Does not give a generator object back
    '''

    def recursive_inorder(self):
        curnod = self.root
        if curnod is None:
            return
        else:
            return curnod._rinorder(curnod)

    '''
    Prints the node.data in postorder. Calls helper function _rpostorder on
    rootnode. Does not give a generator object back
    '''

    def recursive_postorder(self):
        curnod = self.root
        if curnod is None:
            return
        else:
            return curnod._rpostorder(curnod)

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

    '''
    Iterative preorder walk we require a stack to store righr and left child
    nodes till they get poped

    1. We start by adding rootnode to stack. First popping rootnode, yielding
    data and then pushing right and left child on stack as they exist.

    2. The topmost element of stack either left or right node depending
    rootnode's child goes throught above procedure

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

    '''
    This method inserts the data in appropriate position. First a object of
    BinarySearchTree with data is created and we start comparing data with
    curent node starting from rootnode and moving down.

    It is to be noted that insertion happens at leaf only so we traverse down
    till we have spotted a position i.e. we swap the current node with node in
    the direction we move. When we encounter a None while loop breaks.

    We also keep track of previous node by a parent pointer. If this node is
    None this means BST is empty otherwise we compare the data with parent data
    and insert accordingly.
    '''

    def __setitem__(self, data):
        parent = None
        curnod = self.root
        intrm = BinaryTreeNode(data, None, None, None)
        while curnod is not None:
            parent = curnod
            if intrm.data < curnod.data:
                curnod = curnod.left
            else:
                curnod = curnod.right
        intrm.parent = parent
        if parent is None:
            self.root = intrm
        elif intrm.data < parent.data:
            parent.left = intrm
        else:
            parent.right = intrm
        self.size += 1

    '''
    This method returns true if data/key is present in BinarySearchTree
    otherwise False.

    What we do is traverse down by comparing the data/key with current node's
    data/key and updating the curent node with node in which direction we move
    If we find a match i.e. curnod data/key equal to input data/key we return
    True otherwise at end of lopp False is returned.
    '''

    def __contains__(self, key):
        currentnode = self.root
        while currentnode is not None:
            if currentnode.data == key:
                return True
            elif currentnode.data <= key:
                currentnode = currentnode.right
            elif currentnode.data > key:
                currentnode = currentnode.left
        return False

    '''
    A helper function to get all items in sorted order from Binary Search Tree
    as a generator object. For efficiency reason it is better to form a
    generator object by calling inorder_keys() on BinarySearchTree object.
    '''

    def items(self):
        keyset = self.inorder_keys()
        for key in keyset:
            yield key.data

    '''
    This method returns the pointer to BinaryTreeNode i.e. if a node with data
    is present in BinarySearchTree otherwise it give KeyError exception

    To get the item from BST we start from root node as current node. We move
    down by replacing the current node i.e.right if key is greater in value
    than current node value or left othewise. if key is equal to current node
    then we return the current node otherwise KeyError is raised.
    '''

    def __getitem__(self, key):
        currentnode = self.root
        while currentnode is not None:
            if currentnode.data == key:
                return currentnode
            elif currentnode.data <= key:
                currentnode = currentnode.right
            else:
                currentnode = currentnode.left
        raise KeyError("no such key: {0!r}".format(key))

    '''
    First we check wether the node is present in BinarySearchTree or not. For
    same we call __getitem__(key) or simply [key] on BST instance. This method
    takes

    Once we have pointer available to the node. We divide the delete operation
    in three steps

    1. When the node has no child then we simply update the parent node's left
    or right child depending on node's position as None.

    2. When we have one child we replace the node with its child. To do that
    we first update child's parent pointer to point node's parent. We also
    update parent' left or right depending on node's position to child of to
    be deleted node.

    3. when we have two child we find a node to be swaped with node to be
    deleted. We find the node finding minimum of right sub-tree of node to be
    deleted. We then swap the min element with the node to be delted by
    updating left and right child of swapped node as well updating parent
    pointer of left and right childrent to swap node.
    '''

    def __delitem__(self, key):
        '''
        Validate input is BinaryTreeNode or othewise assuming the input is key
        call __getitem__(key) to get pointer for the node to be deleted.
        '''
        if isinstance(key, BinaryTreeNode):
            node = key
        else:
            node = self[key]
        parent = node.parent
        '''
        Check wether the node is left or right child, othewise it is rootnode
        We set L in case left child, R in case right child otherwise None
        '''
        position = None
        if parent:
            if parent.left == node:
                position = "L"
            else:
                position = "R"
        if node.right and node.left:
            self._delbothchild(position, parent, node)
        elif node.right:
            self._delonechild(position, parent, node.right)
        elif node.left:
            self._delonechild(position, parent, node.left)
        else:
            self._delnochild(position, parent)
        # Decrement the size of BST
        self.size -= 1

    '''
    In this case our node to be delted has both the children. So to find min
    of right sub-tree we create a BST tree rooted at node.right. Then we call
    first min_tree() to swapnode and leter we call delete for swapnode on new
    BST though we still have pointer to swapnode available for later

    Now we check whether the node to be deleted is left child or right child,
    accordingly we update parent pointer to swapnode.

    If parent is None means rootnode is to be deleted so we replace root of
    self. Note that since we maintain the invariant that node with equal value
    is on right of node so when we find the min of subtree i.e. swapnode we
    are sure that replacing it as rootnode would not violate the invariant.

    In last step we update the swapnode.right and swapnode.left to be same as
    node to be deleted. We then update parent pointer of both left and right
    child to point to swapnode. Lastly we set subtree.root as None.
    '''

    def _delbothchild(self, position, parent, node):
        subtree = BinarySearchTree(node.right, 0)
        swapnode = subtree.min_tree()
        del subtree[swapnode]
        if position:
            if position == "L":
                parent.left = swapnode
            else:
                parent.right = swapnode
        else:
            self.root = swapnode
        swapnode.left = node.left
        swapnode.right = node.right
        # Swapnode could be immediate left child of node which got removed.
        if node.left:
            node.left.parent = swapnode
        if node.right:
            node.right.parent = swapnode
        subtree.root = None

    '''
    In this case our node to be deleted has no children. We simply check
    whether the node to be deleted is left child or right child, accordingly
    we update parent's lefr or right to None. If parent is None then set
    self.root as None

    '''
    def _delnochild(self, position, parent):
        if position:
            if position == "L":
                parent.left = None
            else:
                parent.right = None
        else:
            self.root = None

    '''
    In this case our node to be deleted has one children. In this case children
    replaces the node to be deleted so we have a pointer for the child.

    Wec heck whether the node to be deleted is left child or right child,
    accordingly we update parent's left or right as None.

    If parent is None then set self.root as child and update child's parent to
    None
    '''

    def _delonechild(self, position, parent, child):
        if position:
            if position == "L":
                parent.left = child
            else:
                parent.right = child
            child.parent = parent
        else:
            self.root = child
            child.parent = None

    def __len__(self):
        return self.size

    def display(self):
        print "Inorder tree traversal"
        print ' '.join(str(item) for item in self.itrerative_inorder())


def main():
    test()


def test():
    keyset1 = [42, 40, 43, 37, 46, 36, 49]
    keyset2 = [42, 37, 46, 40, 43, 36, 49]
    bst = BinarySearchTree()
    for key in keyset2:
        bst.__setitem__(key)
    # bst.recursive_postorder()
    # bst.recursive_preorder()
    # bst.recursive_inorder()
    '''node = bst[37]
    print node.successor()
    print node.predecessor()
    print bst.__contains__(34)
    print bst.__contains__(40)
    print len(bst)'''
    del bst[37]
    bst.recursive_inorder()
    print ""
    print bst.root
    # del bst[40]
    # bst.recursive_inorder()'''


if __name__ == '__main__':
    main()
