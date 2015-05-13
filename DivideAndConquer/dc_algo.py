# -*- coding: utf-8 -*-
import sys      # analysis:ignore
from numpy import *  # analysis:ignore


# TODO: Replace all TODO comments (yes, this one too!)
# TODO: Add doctests, post them on the forum


#STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
STOCK_PRICE_CHANGES = [
    13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]


# Implement pseudocode from the book
def find_maximum_subarray_brute(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)
    """
    GlobalMax = None
    LeftIndice = low
    RightIndice = high
    # Range over values of array for the left indice
    for slowitr in xrange(len(A)):
        LocalSum = 0
        # Range over values of array for the right indice
        for fastitr in xrange(slowitr, len(A)):
            LocalSum += A[fastitr]
            if LocalSum > GlobalMax:
                GlobalMax = LocalSum
                LeftIndice = slowitr
                RightIndice = fastitr
    # Return final left, right index and Sum of Maximum Subarray
    return (LeftIndice, RightIndice, GlobalMax)


# Implement pseudocode from the book
def find_maximum_crossing_subarray(A, low, mid, high):
    """
    Find the maximum subarray that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    """
    # Computing Max Sum for for the left Array~
    LeftSum = -sys.maxint
    MaxLeft = mid
    Sum = 0
    for leftitr in xrange(mid, low - 1, -1):
        Sum += A[leftitr]
        if Sum > LeftSum:
            LeftSum = Sum
            MaxLeft = leftitr
    # Now computing for the right Array
    RightSum = -sys.maxint
    MaxRight = mid + 1
    Sum = 0
    for rightitr in xrange(mid + 1, high + 1, 1):
        Sum += A[rightitr]
        if Sum > RightSum:
            RightSum = Sum
            MaxRight = rightitr
    return (MaxLeft, MaxRight, LeftSum + RightSum)


def find_maximum_subarray_recursive(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4
    """
    # Check if array has single element then return the element as tupple
    if high == low:
        return (low, high, A[low])
    # Call function recursively for left and right half and call Crossing
    # Subarray for actual computation
    else:
        mid = (low + high) // 2
        (leftlow, lefthigh, leftsum) = find_maximum_subarray_recursive(
            A, low, mid)
        (rightlow, righthigh, rightsum) = find_maximum_subarray_recursive(
            A, mid + 1, high)
        (midlow, midhigh, midsum) = find_maximum_crossing_subarray(
            A, low, mid, high)
        if leftsum >= rightsum and leftsum >= midsum:
            return (leftlow, lefthigh, leftsum)
        elif rightsum >= leftsum and rightsum >= midsum:
            return (rightlow, righthigh, rightsum)
        elif midsum >= rightsum and midsum >= leftsum:
            return (midlow, midhigh, midsum)


def find_maximum_subarray_iterative(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.
    """
    # Set default values of left and right Index, local and global maximum
    # subarray sum, Last index when local sum is zero
    GlobalMax = -sys.maxint
    LocalMax = 0
    LeftIndice = 0
    RightIndice = -1
    LastlocalIndice = 0
    for itr in range(0, len(A)):
        LocalMax = LocalMax + A[itr]
        # Update Global Sum and Right Index of Subarray when Local Sum exceeds
        # Global Sum
        if GlobalMax < LocalMax:
            GlobalMax = LocalMax
            RightIndice = itr
        # Update left Indice when Global and Local sum are same and last index
        # not zero
        if LocalMax == GlobalMax and LastlocalIndice != 0:
            LeftIndice = LastlocalIndice + 1
        # Set LocalSum to zero and store Array Index if LocalSum is less than
        # zero
        if LocalMax < 0:
                LastlocalIndice = itr
                LocalMax = 0
    return (LeftIndice, RightIndice, GlobalMax)


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    Mlength = len(A)
    C = zeros([Mlength, Mlength], dtype=int)
    for itra in range(0, Mlength):
        for itrb in range(0, Mlength):
            for itrc in range(0, Mlength):
                C[itra][itrb] = C[itra][itrb] + A[itra][itrc] * B[itrc][itrb]
    return C


def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"
    Fulllength = len(A)

    # Defining Subtract function for Matrices
    def MatrixSubtract(A, B):
        C = zeros([len(A), len(B)], dtype=int)
        for itra in range(0, len(A)):
            for itrb in range(0, len(B)):
                C[itra][itrb] = A[itra][itrb] - B[itra][itrb]
        return C

    # Defining Add function for Matrices
    def MatrixAdd(A, B):
        C = zeros([len(A), len(B)], dtype=int)
        for itra in range(0, len(A)):
            for itrb in range(0, len(B)):
                C[itra][itrb] = A[itra][itrb] + B[itra][itrb]
        return C

    if (Fulllength % 2) != 0:
        print "The matrix has length not in power of 2"

    elif Fulllength == 2:
        return square_matrix_multiply(A, B)

    else:
        Halflength = Fulllength // 2

        # Initializing Subarrays
        a11 = zeros([Halflength, Halflength], dtype=int)
        a12 = zeros([Halflength, Halflength], dtype=int)
        a21 = zeros([Halflength, Halflength], dtype=int)
        a22 = zeros([Halflength, Halflength], dtype=int)
        b11 = zeros([Halflength, Halflength], dtype=int)
        b12 = zeros([Halflength, Halflength], dtype=int)
        b21 = zeros([Halflength, Halflength], dtype=int)
        b22 = zeros([Halflength, Halflength], dtype=int)

        # Populating Subarray Values
        for itra in range(0, Halflength):
            for itrb in range(0, Halflength):
                # Top left of both A and B Matrix
                a11[itra][itrb] = A[itra][itrb]
                b11[itra][itrb] = B[itra][itrb]
                # Top right of both A and B Matrix
                a12[itra][itrb] = A[itra][itrb + Halflength]
                b12[itra][itrb] = B[itra][itrb + Halflength]
                # Bottom left of both A and B Matrix
                a21[itra][itrb] = A[itra + Halflength][itrb]
                b21[itra][itrb] = B[itra + Halflength][itrb]
                # Bottom right of both A and B Matrix
                a22[itra][itrb] = A[itra + Halflength][itrb + Halflength]
                b22[itra][itrb] = B[itra + Halflength][itrb + Halflength]

        # Defining 10 Subbarays
        s1 = MatrixSubtract(b12, b22)
        s2 = MatrixAdd(a11, a12)
        s3 = MatrixAdd(a21, a22)
        s4 = MatrixSubtract(b21, b11)
        s5 = MatrixAdd(a11, a22)
        s6 = MatrixAdd(b11, b22)
        s7 = MatrixSubtract(a12, a22)
        s8 = MatrixAdd(b21, b22)
        s9 = MatrixSubtract(a11, a21)
        s10 = MatrixSubtract(b11, b12)

        # Defining 7 Matrices which recursively call
        # square_matrix_multiply_strassens
        p1 = square_matrix_multiply_strassens(a11, s1)
        p2 = square_matrix_multiply_strassens(s2, b22)
        p3 = square_matrix_multiply_strassens(s3, b11)
        p4 = square_matrix_multiply_strassens(a22, s4)
        p5 = square_matrix_multiply_strassens(s5, s6)
        p6 = square_matrix_multiply_strassens(s7, s8)
        p7 = square_matrix_multiply_strassens(s9, s10)

        # Finally computing the Top left, Top Right, Bottom Left, Bottom Right
        # of Product Matrix
        C11 = MatrixSubtract(MatrixAdd(MatrixAdd(p5, p4), p6), p2)
        C12 = MatrixAdd(p1, p2)
        C21 = MatrixAdd(p3, p4)
        C22 = MatrixAdd(MatrixSubtract(p5, p3), MatrixSubtract(p1, p7))

        # Forming the Product Matrix by combing Top left, Top Right, Bottom
        # Left, Bottom Right
        C = zeros([len(A), len(B)], dtype=int)
        for itra in range(0, Halflength):
            for itrb in range(0, Halflength):
                # Top left of Matrix C
                C[itra][itrb] = C11[itra][itrb]
                # Top right of Matrix C
                C[itra][itrb + Halflength] = C12[itra][itrb]
                # Bottom left of Matrix C
                C[itra + Halflength][itrb] = C21[itra][itrb]
                # Bottom right of Matrix C
                C[itra + Halflength][itrb + Halflength] = C22[itra][itrb]

        # Return the multiplied Matrice formed by above
        return C


def test():
    import doctest
    doctest.testmod()
    print (find_maximum_subarray_brute(
        STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1))
    print (find_maximum_subarray_recursive(
        STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1))
    print (find_maximum_subarray_iterative(
        STOCK_PRICE_CHANGES, 0, len(STOCK_PRICE_CHANGES) - 1))
    print (square_matrix_multiply([[1, 3], [2, 4]], [[1, 3], [2, 4]]))
    print (square_matrix_multiply([
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4]], [[1, 2, 3, 4],
                        [1, 2, 3, 4],
                        [1, 2, 3, 4],
                        [1, 2, 3, 4]
                        ]))
    print "\n"
    print(square_matrix_multiply_strassens([
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4]], [[1, 2, 3, 4],
                        [1, 2, 3, 4],
                        [1, 2, 3, 4],
                        [1, 2, 3, 4]
                        ]))


if __name__ == '__main__':
    test()
