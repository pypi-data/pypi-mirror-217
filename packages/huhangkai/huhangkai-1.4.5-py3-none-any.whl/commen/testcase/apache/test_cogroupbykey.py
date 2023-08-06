from commen.testcase.apache.data import *
from commen.unit_apache_beam import ApacheFun


class TestPolymerization:
    # 通过键聚合所有输入元素，并允许下游处理使用与键关联的所有值
    def test_polymerization_001(self):
        ApacheFun(data_type=data_type).co_group_by_key(icons=data_list_tuple3, durations=data_list_tuple4).print()

    def test_polymerization_002(self):
        ApacheFun(data_type=data_type).co_group_by_key(data_list_tuple3, data_list_tuple4, data_list_tuple4).print()

    # 组合集合中的所有元素, 使用函数
    def test_polymerization_003(self):
        def get_common_items(sets):
            return set.intersection(*(sets or [set()]))
        ApacheFun(data_list_set, data_type=data_type).combine_globally(get_common_items).print()

    def test_polymerization_004(self):
        ApacheFun(data_list_set, data_type=data_type).combine_globally(lambda sets: set.intersection(*(sets or [set()]))).print()

    def test_polymerization_005(self):
        ApacheFun(data_list_set, data_type=data_type).combine_globally(
            lambda sets, exclude: set.intersection(*(sets or [set()])) - exclude, exclude={'🥕'}).print()

    def test_polymerization_006(self):
        ApacheFun(data_list2, data_type=data_type).combine_percentages_fn(type=3).print()
