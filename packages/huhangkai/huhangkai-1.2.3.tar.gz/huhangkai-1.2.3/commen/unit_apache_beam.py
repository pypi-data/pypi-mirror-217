import datetime
import re
import time

import apache_beam as beam
import uuid

from apache_beam import PCollection
from apache_beam.pvalue import DoOutputsTuple
from apache_beam.transforms import window


class ApacheFun:
    window = window

    def __init__(self, data=None, name="", out=None):
        self.pipeline = beam.Pipeline()
        self.data = data
        self.out = out
        self.value = None
        self.name = name or str(uuid.uuid4())[-12:]
        self._i = 0
        self._tmp_value = None
        if data:
            self.create()

    def __str__(self):
        return self.value

    def _name(self):
        self._i += 1
        return str(self.name) + str(self._i)

    def run(self):
        """执行"""
        self.pipeline.run()

    def print(self, fmt=None):
        """打印"""
        def _print(x):
            if fmt:
                _str = "self._tmp_value=" + fmt
                exec(_str)
                print(self._tmp_value)
            else:
                print(x)
        if isinstance(self.out, PCollection):
            self.out | self._name() >> beam.Map(lambda x: _print(x))
        elif isinstance(self.out, (list, tuple, DoOutputsTuple)):
            for i in self.out:
                if isinstance(i, PCollection):
                    i | self._name() >> beam.Map(lambda x: _print(x))
        self.run()

    def create(self, data=None):
        """创建"""
        self.value = self.pipeline | self._name() >> beam.Create(data or self.data)
        if not(data and self.data):
            self.out = self.value
        return self

    def par_do(self, fn, *args, **kwargs):
        """ParDo 与 DoFn 方法"""
        self.value = self.out = self.get_out() | self._name() >> beam.ParDo(fn, *args, **kwargs)
        return self

    def window_info(self, fn, *args, **kwargs):
        self.value = self.out = self.get_out() | self._name() >> beam.WindowInto(fn, *args, **kwargs)
        return self

    def get_out(self):
        """判断是否已经是管道"""
        return self.out if isinstance(self.out, PCollection) else self.create().value

    def map(self, fn, *args, **kwargs):
        """对集合中的每个元素应用简单的 1 对 1 映射函数。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Map(fn, *args, **kwargs)
        return self

    def map_tuple(self, fn, *args, **kwargs):
        """如果PCollection由（键、值）对组成，则可以使用MapTuple将它们解压到不同的函数参数中"""
        self.value = self.out = self.get_out() | self._name() >> beam.MapTuple(fn, *args, **kwargs)
        return self

    def filter(self, fn, *args, **kwargs):
        """给定一个谓词，过滤掉所有不满足该谓词的元素。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Filter(fn, *args, **kwargs)
        return self

    def flat_map(self, fn, *args, **kwargs):
        """应用一个函数，该函数将集合返回到输入中的每个元素，并输出所有结果元素。"""
        self.value = self.out = self.get_out() | self._name() >> beam.FlatMap(fn, *args, **kwargs)
        return self

    def flat_map_tuple(self, fn, *args, **kwargs):
        """应用一个函数，该函数将集合返回到输入中的每个元素，并输出所有结果元素。"""
        self.value = self.out = self.get_out() | self._name() >> beam.FlatMapTuple(fn, *args, **kwargs)
        return self

    def regex_matches(self, regex, group=0):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.matches(regex, group)
        return self

    def regex_all_match(self, regex):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.all_matches(regex)
        return self

    def regex_matches_kv(self, regex, keyGroup=0):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.matches_kv(regex, keyGroup)
        return self

    def regex_find(self, regex, group=0):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.find(regex, group)
        return self

    def regex_find_all(self, regex):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.find_all(regex)
        return self

    def regex_find_kv(self, regex, keyGroup=0):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.find_kv(regex, keyGroup)
        return self

    def regex_replace_all(self, regex, replacement):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.replace_all(regex, replacement)
        return self

    def regex_replace_first(self, regex, replacement):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.replace_first(regex, replacement)
        return self

    def regex_split(self, regex, outputEmpty=False):
        """根据正则表达式过滤输入字符串元素，也可以根据匹配的组对它们进行转换。"""
        self.value = self.out = self.get_out() | self._name() >> beam.Regex.split(regex, outputEmpty)
        return self

    def partition(self, fn, num, *args, **kwargs):
        """基于某些分区函数将每个输入元素路由到特定的输出集合。"""
        self.out = self.get_out() | self._name() >> beam.Partition(fn, num, *args, **kwargs)
        self.value = [ApacheFun(out=x) for x in self.out]
        return self

    def pvalue_as_dict(self, data):
        """字典"""
        return beam.pvalue.AsDict(self.create(data).value)

    def pvalue_as_iter(self, data):
        """列表"""
        return beam.pvalue.AsIter(self.create(data).value)

    def pvalue_as_singleton(self, data):
        """单实例"""
        return beam.pvalue.AsSingleton(self.create(data).value)

    def keys(self, data=None):
        self.value = self.create(data).value | self._name() >> beam.Keys()
        if not(data and self.data):
            self.out = self.value
        return self

    def values(self, data=None):
        self.value = self.create(data).value | self._name() >> beam.Values()
        if not (data and self.data):
            self.out = self.value
        return self

    def to_string_kvs(self):
        """将输入集合中的每个元素转换为字符串。"""
        self.value = self.out = self.get_out() | self._name() >> beam.ToString.Kvs()
        return self

    def to_string_element(self):
        """将输入集合中的每个元素转换为字符串。"""
        self.value = self.out = self.get_out() | self._name() >> beam.ToString.Element()
        return self

    def to_string_iterables(self):
        """将输入集合中的每个元素转换为字符串。"""
        self.value = self.out = self.get_out() | self._name() >> beam.ToString.Iterables()
        return self

    def timestamped_value(self, key=None, type="bj"):
        """应用一个函数来确定输出集合中每个元素的时间戳，并更新与每个输入关联的隐式时间戳。请注意，只有向前调整时间戳才是安全的"""
        class GetTimestamp(beam.DoFn):
            def __init__(self, key=None):
                self.key = key

            def process(self, plant, timestamp=beam.DoFn.TimestampParam):
                key = self.key if self.key else "current"
                if type == "utc":
                    plant[key] = timestamp.to_utc_datetime()
                elif type == "bj":
                    plant[key] = datetime.datetime.fromtimestamp(timestamp.micros / 1e6).strftime("%Y-%m-%d %H:%M:%S")
                elif type == "rfc":
                    plant[key] = timestamp.to_rfc3339()
                elif type == "proto":
                    plant[key] = timestamp.to_proto()
                yield plant

        self.value = self.out = self.get_out() | self._name() >> beam.Map(
            lambda plant: self.window.TimestampedValue(plant, plant[key] if key and plant.get(key) else time.time())
        ) | self._name() >> beam.ParDo(GetTimestamp(key=key))
        return self

    def kvswap(self, data=None):
        """获取一个键值对集合并返回一个键值对集合，其中每个键值对都进行了交换。"""
        self.value = self.create(data).value | self._name() >> beam.KvSwap()
        if not (data and self.data):
            self.out = self.value
        return self

    def co_group_by_key(self, *args, **kwargs):
        """获取多个键控元素集合并生成一个集合，其中每个元素都包含一个键和与该键关联的所有值。"""
        plants = {}
        for i, v in enumerate(args):
            plants["key%s" % i] = v if isinstance(v, PCollection) else (
                v.value if isinstance(v, ApacheFun) else self.create(v).value)
        for k, v in kwargs.items():
            plants[k] = v if isinstance(v, PCollection) else (
                v.value if isinstance(v, ApacheFun) else self.create(v).value)
        self.value = self.out = plants | self._name() >> beam.CoGroupByKey()
        return self

    def combine_globally(self, fn, *args, **kwargs):
        """组合集合中的所有元素"""
        self.value = self.out = self.get_out() | self._name() >> beam.CombineGlobally(fn, *args, **kwargs)
        return self

    def combine_percentages_fn(self, key=None, type=1):
        """统计集合中的所有元素"""
        class PercentagesFn(beam.CombineFn):
            def __init__(self, key=None, type=1):
                self.key = key
                self.type = type

            def create_accumulator(self):
                return {}

            def add_input(self, accumulator, input):
                input = input[self.key] if self.key and self.key in input else input
                if input not in accumulator:
                    accumulator[input] = 0
                accumulator[input] += 1
                return accumulator

            def merge_accumulators(self, accumulators):
                merged = {}
                for accum in accumulators:
                    for item, count in accum.items():
                        if item not in merged:
                            merged[item] = 0
                        merged[item] += count
                return merged

            def extract_output(self, accumulator):
                if self.type == 1:
                    return accumulator
                elif self.type == 2:
                    total = sum(accumulator.values())  # 10
                    percentages = {item: count / total for item, count in accumulator.items()}
                    return percentages
                elif self.type == 3:
                    total = sum(accumulator.values())  # 10
                    percentages = {item: ("%.1f%%" % (count / total * 100)) for item, count in accumulator.items()}
                    return percentages
        self.value = self.out = self.combine_globally(PercentagesFn(key, type)).value
        return self


if __name__ == '__main__':
    from study.data.data import *
    ApacheFun(data_list_tuple).create().print()
