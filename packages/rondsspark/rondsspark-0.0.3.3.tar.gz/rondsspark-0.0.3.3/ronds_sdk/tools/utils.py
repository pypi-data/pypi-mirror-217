import json
from typing import Callable, List

from ronds_sdk import error


class WrapperFunc(object):
    def call(self, *args, **kwargs):
        raise NotImplementedError


class ForeachBatchFunc(WrapperFunc):
    def __init__(self,
                 func,  # type: Callable
                 **kwargs
                 ):
        self._func = func
        self._kwargs = kwargs

    def call(self, *args, **kwargs):
        new_kwargs = {**self._kwargs, **kwargs}
        self._func(*args, **new_kwargs)


class RuleParser(object):

    def __init__(self,
                 rule_path,  # type: str
                 ):
        self._rule_path = rule_path

    def load(self) -> list:
        with open(self._rule_path, 'r') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            return json.loads(config.strip('\t\r\n'))

    @staticmethod
    def point_ids(rule: dict) -> List[str]:
        """
        读取 rule 配置文件中的测点 id list
        :param rule: 规则配置
        :return: 测点 id list
        """
        points = rule['points']
        p_list = list()
        if points:
            for point in points:
                p_list.append(point.point_id)
        return p_list

    @staticmethod
    def datetime_format():
        return '%Y-%m-%d %H:%M:%S'
