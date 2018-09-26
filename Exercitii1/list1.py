a = [1, 1, 2, 3, 5, 8, 13, 8, 21, 34, 55, 89]
b = [1, 2, 3, 4, 3, 5, 6, 8, 7, 7, 8, 9, 10, 11, 12, 13]
# c=[]
#
# for i in a:
#     for j in b:
#         if i == j:
#             c.append(i) # sau j
#
#
# print (c)
#

#
# sau !!!
#

import random
# a=random.sample(range(1,30),15)
# b=random.sample(range(1,40),25)
# print(a)
# print(b)
# newlist=[]
# for i in a:
#     if i in b:
#         if i in newlist:
#           print("duplicates are",i)
#
#         else:
#             newlist.append(i)
#
# print(newlist)

# sau !!!

mylist = []

for element in a :
    if element in b :
        if element not in mylist:
            mylist.append(element)
        else:
            continue
            print(element,'elemente comune')
print(mylist)


# sau !!!

# c =[]
# print([e for e in b if e in a and e not in c])


# sau !!!

# import random
#
# lst = [x for x in range(1, random.randint(1,30)) if x in range(1, random.randint(1,30)) ]
#
# print list(set(lst))

# a = [1,1,1,6,7,8,9,4,9]
# b = [1,6,87,98,67,45,10,11,12,13,14,15,16]
# print(set(a) & set(b))