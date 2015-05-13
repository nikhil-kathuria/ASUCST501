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

	print  "Left :" + str(LeftIndice) + "\nRight :" + str(RightIndice) + "\nThe Sum :" +str(GlobalMax)
	print  "Lenght of Array :" + str(len(A))		
	return LeftIndice,RightIndice,GlobalMax

from time import time
time0 = time()
MaxSubarray([2,-3,4,-8,9,1,-3,12,-11,-9,25,-3,4,-12,7,4,6,7,-9,-2,-5,20,-11,-23,4,5,6,2,-11,3,5,
	-12,9,25,-3,4,-12,12,-11,-9,25,-3,2,-3,4,-8,9,1,-3,12,-11,-9,25,-3,4,-12,7,4,6,7,-9,-2,-5,20,-11,-23,-12,9,
	])
time1 = time()
print (time1-time0)



