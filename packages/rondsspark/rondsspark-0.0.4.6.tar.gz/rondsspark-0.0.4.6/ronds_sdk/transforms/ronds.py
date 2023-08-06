import logging
import time

from ronds_sdk.dataframe import pvalue
from ronds_sdk.tools.utils import RuleParser
from ronds_sdk.transforms.ptransform import PTransform
from typing import TYPE_CHECKING, Union

__all__ = [
    'RulesCassandraScan',
    'Create',
    'Socket',
    'Filter',
    'Console',
    'Algorithm',
    'Sleep'
]


class Sleep(PTransform):

    def __init__(self,
                 seconds=60,  # type: int
                 ):
        super(Sleep, self).__init__()
        self.seconds = seconds

    def expand(self, input_inputs, action_func=None):
        return input_inputs


class RulesCassandraScan(PTransform):
    """
    根据规则配置, 按照制定时间窗口周期, 进行 Cassandra 定期读表加载数据
    """

    def __init__(self,
                 rule_path,  # type: str
                 ):
        super(RulesCassandraScan, self).__init__()
        self._rules = RuleParser(rule_path).load()

    @property
    def rules(self):
        return self._rules

    def expand(self, p_begin, action_func=None):
        assert isinstance(p_begin, pvalue.PBegin)
        return pvalue.PCollection(p_begin.pipeline,
                                  element_type=pvalue.PBegin,
                                  is_bounded=True)


class Create(PTransform):
    def __init__(self, values):
        """
        create dataframe from memory list, generally for test
        :param values: eg. [(1, 2, 'str'), ...]
        """
        super(Create, self).__init__()
        if isinstance(values, (str, bytes)):
            raise TypeError(
                'PTransform Create: Refusing to treat string as '
                'an iterable. (string=%r)' % values)
        elif isinstance(values, dict):
            values = values.items()
        self.values = values

    def expand(self, p_begin, action_func=None):
        return pvalue.PCollection(p_begin.pipeline,
                                  element_type=pvalue.PBegin,
                                  is_bounded=True)


class Socket(PTransform):
    def __init__(self,
                 host,  # type: str
                 port,  # type: int
                 ):
        """
        Read Socket Data, for streaming
        :param host: socket host
        :param port: socket port
        """
        super(Socket, self).__init__()
        if not host or not port:
            raise ValueError(
                'PTransform Socket: host or port unexpected null, '
                'host: %s , port: %s' % (host, port))
        self.host = host
        self.port = port

    def expand(self, p_begin, action_func=None):
        return pvalue.PCollection(p_begin.pipeline,
                                  element_type=pvalue.PBegin,
                                  is_bounded=False)


class Filter(PTransform):
    def __init__(self,
                 select_cols,  # type: Union[str, list[str]]
                 where  # type: str
                 ):
        """
        过滤数据, 同时进行字段的筛选
        eg. pipeline | ... | 'filter data' >> ronds.Filter("col_1", "col_2 > 'xxx'")
        :param select_cols:
        :param where:
        """
        super(Filter, self).__init__()
        self.where = where
        self.select_cols = select_cols

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_type=pvalue.PCollection,
                                  is_bounded=input_inputs.is_bounded)


class Console(PTransform):

    def __init__(self,
                 mode='complete',  # type: str
                 ):
        """
        控制台输出数据集, for test
        :param mode: 输出模式, 默认 complete
        """
        super(Console, self).__init__()
        self.mode = mode if mode else 'complete'

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_type=pvalue.PCollection,
                                  is_bounded=input_inputs.is_bounded)


class Algorithm(PTransform):
    def __init__(self,  # type: Algorithm
                 alg_path=None,  # type: str
                 func_name=None,  # type: str
                 ):
        """
        调用外部算法, 指定算法文件的地址和需要调用的函数名称;
        算法需要接受记录作为参数, 同时返回记录作为算法的处理结果
        :param alg_path: 算法文件地址
        :param func_name: 算法函数名称
        """
        super(Algorithm, self).__init__()
        self.path = alg_path
        self.func_name = func_name

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_type=pvalue.PCollection,
                                  is_bounded=input_inputs.is_bounded)
