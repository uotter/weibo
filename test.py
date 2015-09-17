__author__ = 'M'


def sort_by_value_dec(d):
    resultdic = {}
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0, len(backitems))]


a = [1, 3, 5, 7]
b = [1, 3, 4, 6, 8]
c = list(set(b)-set(a))
print c
