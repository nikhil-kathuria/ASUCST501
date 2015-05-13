import sys, math

def MaxSubarrayRecursive(MainArray):


	### Defining the combine fucntion which finds subarray in Crossing Array
	def MaxCrossingArray(CrossArray,low,mid,high):
		LeftSum=-sys.maxint
		MaxLeft=mid
		Sum=0
		for leftitr in xrange(mid,low-1,-1):
			Sum += CrossArray[leftitr]
			if Sum > LeftSum:
				LeftSum = Sum
				MaxLeft = leftitr
	## Now computing for the right Array			
		RightSum=-sys.maxint
		MaxRight=mid+1
		Sum=0
		for rightitr in xrange(mid+1,high+1,1):
			Sum += CrossArray[rightitr]
			if Sum > RightSum:
				RightSum = Sum
				MaxRight = rightitr
	## return the MaxRight and MaxLeft Index along with Sum of Both Subarrays
		return (MaxLeft, MaxRight, LeftSum+RightSum)
	
	
	### Defining Main calling function for MaxSubarray
	def MaxSubArray(MainArray,low,high):
		if high == low:
			return (low, high, MainArray[low])
		else:
			mid = (low + high) // 2
			##print low, high, mid
			(leftlow, lefthigh, leftsum)= MaxSubArray(MainArray,low, mid)
			(rightlow, righthigh, rightsum) = MaxSubArray(MainArray,mid+1,high)
			(midlow, midhigh, midsum) = MaxCrossingArray(MainArray, low, mid, high)
			if leftsum >= rightsum and leftsum >= midsum:
				return (leftlow, lefthigh, leftsum)
			elif rightsum >= leftsum and rightsum >= midsum:
				return (rightlow, righthigh, rightsum)
			elif midsum >=rightsum and midsum >= leftsum:
				return (midlow, midhigh, midsum)
	
	### The Brute Force Max Sub Array Function
	def MaxSubarray(A):
		GlobalMax=None
		LeftIndice=0
		RightIndice=0

		for slowitr in xrange(len(A)):
			LocalSum=0
			for fastitr in xrange(slowitr,len(A)):
				LocalSum += A[fastitr]
				if LocalSum > GlobalMax:
					GlobalMax = LocalSum
					LeftIndice=slowitr
					RightIndice=fastitr

	#print  "Left :" + str(LeftIndice) + "\nRight :" + str(RightIndice) + "\nThe Sum :" +str(GlobalMax)
	#print  "Lenght of Array :" + str(len(A))		
		return LeftIndice,RightIndice,GlobalMax						
	
	### The Wrapper Function exploiting both 
	def MaxSubArrayMixed(MainArray,low,high):
		if len(MainArray) < 68:
			return (MaxSubArray(MainArray))
		else:
			mid = (low + high) // 2
			##print low, high, mid
			(leftlow, lefthigh, leftsum)= MaxSubArray(MainArray,low, mid)
			(rightlow, righthigh, rightsum) = MaxSubArray(MainArray,mid+1,high)
			(midlow, midhigh, midsum) = MaxCrossingArray(MainArray, low, mid, high)
			if leftsum >= rightsum and leftsum >= midsum:
				return (leftlow, lefthigh, leftsum)
			elif rightsum >= leftsum and rightsum >= midsum:
				return (rightlow, righthigh, rightsum)
			elif midsum >=rightsum and midsum >= leftsum:
				return (midlow, midhigh, midsum)


	## The initiation Call to MaxSubarray which calls MaxCrossingArray
	LenghtOfArray= len(MainArray) -1
	return MaxSubArray(MainArray,0,LenghtOfArray)


from time import time
time0 = time()
print MaxSubarrayRecursive([2,-3,4,-8,9,1,-3,12,-11,-9,25,-3,4,-12,7,4,6,7,-9,-2,-5,20,-11,-23,4,5,6,2,-11,3,5,
	-12,9,25,-3,4,-12,12,-11,-9,25,-3,2,-3,4,-8,9,1,-3,12,-11,-9,25,-3,4,-12,7,4,6,7,-9,-2,-5,20,-11,-23,-12,9,
	])
time1 = time()
print (time1-time0)