def sum_only_integers(nums):
    total_sum = 0

    for num in nums:
        if type(num) == int:
            total_sum += num
        else:
            raise ValueError("All numbers are supposed to be integers")

    return total_sum