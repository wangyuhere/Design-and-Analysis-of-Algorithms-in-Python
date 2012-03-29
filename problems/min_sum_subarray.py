'''
Problem description:

Give a array of integers, find a subarray of this array which has the minimum sum.
For example, [12, 3, -5, 3, -9, 10, 0], the subarray [-5, 3, -9] has the minimum sum -11.

Input: an array as a list
Output: sub-array which has the minimum sum and the sum

'''
from math import floor

def brute(a):
	'''Brute force O(n^2)'''
	min_sum = float('inf')
	begin = 0
	end = 0
	
	for i in range(2, len(a)+1):
		sum = 0
		for j in range(0, i):
			sum += a[j]
			
		if sum < min_sum:
			min_sum, begin, end = sum, 0, i
			
		for k in range(1, len(a)-i+1):
			sum = sum - a[k-1] + a[k+i-1]
			if sum < min_sum:
				min_sum, begin, end = sum, k, k+i
	
	return a[begin:end], min_sum


def divide(a):
	'''Divide and conquer O(n*log(n))'''
	if len(a) == 0:
		return None, None
	
	def conquer(s, b, e):
		'''Find the minmum subarray recursivly.
		Input:
			s: array
			b: begin index
			e: end index
		Return:
			((left_sum, left_begin_index, left_end_index),
			 (all_sum, all_begin_index, all_end_index),
			 (right_sum, right_begin_index, right_end_index))
		'''
		if e == b + 1:
			return (s[b], b, e), (s[b], b, e), (s[b], b, e)
		
		l1, l2, l3 = conquer(s, b, int(b+floor((e-b)/2)))
		r1, r2, r3 = conquer(s, int(b+floor((e-b)/2)), e)
		
		all = [l1, l2, l3, (l3[0]+r1[0], l3[1], r1[2]), r1, r2, r3]
		left = filter(lambda x:x[1]==l1[1], all)
		right = filter(lambda x:x[2]==r3[2], all)
		
		compare = lambda x, y: cmp(x[0], y[0])
		l = sorted(left, compare)[0]
		a = sorted(all, compare)[0]
		r = sorted(right, compare)[0]
		return l, a, r
	
	left, all, right = conquer(a, 0, len(a))
	return a[all[1]:all[2]], all[0]


def dynamic(a):
	'''Dynamic programming O(n)'''
	min_sum = (a[0], 0, 1)
	r_min_sum = (a[0], 0, 1)
	for i in range(1, len(a)):
		if r_min_sum[0]+a[i] > a[i]:
			r_min_sum = (a[i], i, i+1)
		else:
			r_min_sum = (r_min_sum[0]+a[i], r_min_sum[1], i+1)
			
		if r_min_sum[0] < min_sum[0]:
			min_sum = r_min_sum

	return a[min_sum[1]:min_sum[2]], min_sum[0]


def main():
	a = [12, 3, -5, 3, -9, 10, 0]
	print 'Input: ', a, '\n'
	
	ms = [brute, divide, dynamic]
	for m in ms:
		s = m(a)
		print m.__doc__
		print s, '\n'


if __name__ == '__main__':
	main()
	