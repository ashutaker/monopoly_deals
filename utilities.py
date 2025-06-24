
def find_subset_by_sum(nums, target):
    """
    Finds a subset of nums that sums to target.

    Args:
        nums: A list of integers ( available values of the money card).
        target: The target sum. (amount to pay)

    Returns:
        A list representing the subset, or None if no such subset exists. ( list of money cards to pay out of money pile)
    """
    n = len(nums)

    def backtrack(index, current_sum, current_subset):
        
        if current_sum == target:
            return current_subset[:]  # Return a copy to avoid modification
        if index == n or current_sum > target:
            return None

        # Include the current number
        result = backtrack(index + 1, current_sum + nums[index], current_subset + [nums[index]])
        if result:
            return result

        # Exclude the current number
        result = backtrack(index + 1, current_sum, current_subset)
        return result

    return backtrack(0, 0, [])

def get_cards_by_value(sort_money,target_money):
   result_money = find_subset_by_sum(sort_money, target_money)
   while not result_money:
       print(f"Rent to collect {target_money}")
       if sum(sort_money) < target_money:
           result_money = sort_money
       else:
           target_money  = target_money + 1
           result_money = find_subset_by_sum(sort_money, target_money )
   return result_money