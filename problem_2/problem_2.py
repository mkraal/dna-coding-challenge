"""
Implementation of Problem 2 using Binary search
"""


def closest_binary_search(data, target) -> int:
    """Perform binary search on a sorted array with non-unique integers

    Returns index j such that A[0], ..., A[j - 1] are strictly less than target, and all elements in the range A[j], ..., A[n - 1] are greater than or equal to"""

    # Handle edge cases
    if target <= data[0] or target > data[-1]:
        return -1
    low, high = 0, len(data) - 1

    # Start search
    while low <= high:
        mid = (low + high) // 2
        check = data[mid]
        if check < target:
            low = mid + 1
        else:
            high = mid - 1

    # Return the index
    if low < len(data) and data[low] >= target:
        return low
    return -1


def main():
    test_1 = [-3, -1, 0, 1, 2, 4, 5, 6, 6, 8, 9]
    # test_2 = [1,2,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]

    res = closest_binary_search(test_1, 4)
    print(res)


if __name__ == "__main__":
    main()
