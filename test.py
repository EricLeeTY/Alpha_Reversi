import numpy as np
list1 = [1,2,3,4,5,6]
list2 = list1[1:]
list3 = list2.extend(list1)
print(list2)
print(list3)