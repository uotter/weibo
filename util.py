# -*-coding:UTF-8-*-
__author__ = 'M'


# ��һ���ֵ����d������value��ֵ���н������У������к������Ԫ�ص�key�ϳ�Ϊһ��list�������к��˳�򷵻�
def sort_by_value_dec(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[index][1] for index in range(0, len(backitems))]
