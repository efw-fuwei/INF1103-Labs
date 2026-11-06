import copy

list1 = [[1, 2], [3, 4]]
list2 = copy.deepcopy(list1)  # Creates brand-new copies of EVERYTHING inside

list2[1][1] = 99
print(list1)  # Output: [[1, 2], [3, 4]] -> Unchanged!
print(list2)  # Output: [[99, 2], [3, 4]] -> Changed!