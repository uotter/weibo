# -*-coding:UTF-8-*-
__author__ = 'M'


# 对一个字典变量d按照其value的值进行降序排列，把排列后的所有元素的key合称为一个list按照排列后的顺序返回
def sort_by_value_dec(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[index][1] for index in range(0, len(backitems))]
