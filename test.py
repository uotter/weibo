__author__ = 'M'


def sort_by_value_dec(d):
    resultdic = {}
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0, len(backitems))]


dic = {1: 8, 2: 1, 4: 4}

dic_sort = sort_by_value_dec(dic)
print dic_sort
