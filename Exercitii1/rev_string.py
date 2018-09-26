# # sss = 'mon nom est mihai'
# #
# # a = sss.split(' ')
# #
# # b = []
# # for i in a:
# #     b.append(i)
# #
# # b.reverse()
# # print(b)
#
#
# def get_revese():
#     sss =  input('get your reverse: ')
#     a = sss.split(' ')
#     b = []
#
#     for i in a:
#         b.append(i)
#     b.reverse()
#     for j in b:
#         print(j)
#
# get_revese()


def reverse():
    a =  input('reverse your words: ')
    b=a.split()
    c=b[::-1]
    d=" ".join(c)
    return d


reverse()