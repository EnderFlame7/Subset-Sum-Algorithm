import math
import os

'''
    This file contains the template for Assignment1.  For testing it, I will place it
    in a different directory, call the function <number_of_allowable_intervals>, and check
    its output. So, you can add/remove  whatever you want to/from this file.  But, don't
    change the name of the file or the name/signature of the following function.

    Also, I will use <python3> to run this code.
'''

def number_of_allowable_intervals(input_file_path, output_file_path):
    '''
        This function will contain your code.  It wil read from the file <input_file_path>,
        and will write its output to the file <output_file_path>.
    '''
    
    #Accessing the input text file
    file = open(input_file_path, "r")

    # Store the size, maximum, and minimum
    lines = file.readlines()
    size = int(lines[0].split(", ")[0])
    min = int(lines[0].split(", ")[1])
    max = int(lines[0].split(", ")[2])

    # Store the list of numbers in a list
    list = lines[1].split(", ")
    for i in range(size):
        list[i] = int(list[i])
     
    #It is good practice to close the file at the end to free up resources 
    file.close()

    # Open the output file and write the result of algorithm_B to that file
    fout = open(output_file_path, "w+")
    fout.write(str(count_valid_contiguous_subarrays(list, size, min, max)))
    fout.close()

def count_valid_contiguous_subarrays(list, size, min, max):
     
    # Store the number of valif contigous subarrays in this variable
	valid_contiguous_subarrays = 0

    # If the subarray NOT of length 1
	if size > 1:

        # Get the left and right half sublists
		left_sublist = list[0:math.ceil(size / 2)]
		right_sublist = list[math.ceil(size / 2):size]

        # Get the sizes of each
		left_size = math.ceil(size / 2)
		right_size = size - math.ceil(size / 2)

        # Declare lists for both
		left_sum_list = []
		right_sum_list = []

        # Initialize the elements of the left_sum_list
		sum = 0
		for n in range(left_size-1, -1, -1):
			sum += left_sublist[n]
			left_sum_list.append(sum)

        # Initialize the elements of the right_sum_list
		sum = 0
		for m in right_sublist:
			sum += m
			right_sum_list.append(sum)

        # Get the number of valid contigous subarrays within the left, right, and "middle" sublists
		valid_contiguous_subarrays += count_valid_contiguous_subarrays(left_sublist, left_size, min, max)
		valid_contiguous_subarrays += count_valid_contiguous_subarrays(right_sublist, right_size, min, max)
		valid_contiguous_subarrays += number_of_pairs(left_sum_list, right_sum_list, [min, max])
	
    # If the subarray is of length 1 and is within valid range...
	elif list[0] >= min and list[0] <= max:

        # Increment the number of valid contigous subarrays by 1
		valid_contiguous_subarrays += 1

	return valid_contiguous_subarrays

# ALGORITHM A BELOW

# Algorithm with goal of O((n+m)log(n+m)) time
def number_of_pairs(arr_a, arr_b, min_max_range):
    mergeSort(arr_a)
    mergeSort(arr_b)
    count = 0

    for a in arr_a:
        if a + arr_b[0] > min_max_range[1] or a + arr_b[len(arr_b) - 1] < min_max_range[0]:
            continue
        else:
            l = left_sum_index(arr_b, 0, len(arr_b) - 1, a, min_max_range)
            r = right_sum_index(arr_b, 0, len(arr_b) - 1, a, min_max_range)
            count = count + r - l + 1  # Sums range of correct pairs for a+b with specific a
    return count


# Finds the starting index where a+b is within the range
# Should be O(log(m))
def left_sum_index(arr, lidx, ridx, a, min_max_range):
    m = lidx + ((ridx - lidx) // 2)
    med = arr[m]
    s = a + med
    if s < min_max_range[0] and ridx == lidx:
        return m + 1
    elif ridx == lidx:
        return m
    elif s < min_max_range[0]:  # a+b too small, search right subarray
        return left_sum_index(arr, m + 1, ridx, a, min_max_range)
    else:  # a+b still within range, search left subarray
        return left_sum_index(arr, lidx, m, a, min_max_range)


# Finds the last index where a+b is still within the range
# Should be O(log(m))
def right_sum_index(arr, lidx, ridx, a, min_max_range):
    m = lidx + ((ridx - lidx) // 2)
    med = arr[m]
    s = a + med
    if s > min_max_range[1] and ridx == lidx:
        return m - 1
    elif ridx == lidx:
        return m
    elif s > min_max_range[1]:  # a+b too big, search left subarray
        return right_sum_index(arr, lidx, m, a, min_max_range)
    else:  # a+b still within range, search right subarray
        return right_sum_index(arr, m + 1, ridx, a, min_max_range)

def merge(arr, L, R):
    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = 0  # Initial index of iterator

    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr):
    arr_len = len(arr)

    if arr_len > 1:
        m = arr_len // 2

        # subarray lengths
        n1 = m
        n2 = arr_len - m

        # create temp arrays
        L = [0] * n1
        R = [0] * n2

        # Copy data to temp arrays L[] and R[]
        for i in range(0, n1):
            L[i] = arr[i]

        for j in range(0, n2):
            R[j] = arr[n1 + j]

        # Sort first and second halves
        mergeSort(L)
        mergeSort(R)
        merge(arr, L, R)


# testing number of pairs
a = [-2,0,-1]
b = [-3,10]
r = [-3,20]
#print("number of pairs", (number_of_pairs(a, b, r)))

# testing merge
one = [-10, 4, 10, 6, 2, 8]
two = [1, 5, 9, 7, 3, 11]
array_a = one + two
#print("combined array", array_a)
mergeSort(array_a)
#m = len(array_a)//2
#merge(array_a, m)
#print("mergeSorted array", array_a)

# test 2 number of pairs
print("number of pairs", (number_of_pairs(one, two, r)))

# test 3 number of pairs
A = [8,12,-5,-3,3,7,-1,0]
B = [-6,9,13,-3,0,1,-4,5]
print("number of pairs", (number_of_pairs(A, B, r)))

# test 4 repeat test 3 with different size arrays: smaller a
A = [8,12,-5,-3,3,7,-1]
B = [-6,9,13,-3,0,1,-4,5]
print("number of pairs", (number_of_pairs(A, B, r)))

# test 5 repeat test 3 with different size arrays: smaller b
B = [8,12,-5,-3,3,7,-1]
A = [-6,9,13,-3,0,1,-4,5]
print("number of pairs", (number_of_pairs(A, B, r)))