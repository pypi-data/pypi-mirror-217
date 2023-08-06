import importlib
import json
import sys
from os.path import dirname, abspath
from typing import TYPE_CHECKING
from pathlib import Path

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

from ronds_sdk import error
from ronds_sdk.dataframe import pvalue
from ronds_sdk.options.pipeline_options import SparkRunnerOptions, CassandraOptions, AlgorithmOptions
from ronds_sdk.transforms import ronds
from ronds_sdk.transforms.ptransform import PTransform, ForeachBatchTransform

if TYPE_CHECKING:
    from ronds_sdk.options.pipeline_options import PipelineOptions


class RulesCassandraScan(ForeachBatchTransform):

    def __init__(self,
                 rule_load,  # type: ronds.RulesCassandraScan
                 options,  # type: PipelineOptions
                 spark=None,  # type: SparkSession
                 ):
        super(RulesCassandraScan, self).__init__()
        self._rules = rule_load.rules
        self._spark = spark
        self.__options = options

    @property
    def options(self):
        return self.__options

    def expand(self, p_begin, action_func=None):
        from ronds_sdk.transforms.pandas.cassandra_rule import ForeachRule
        foreach_rule = ForeachRule(self.options.view_as(CassandraOptions), action_func)
        if self._spark:
            repartition_num = self.options.view_as(SparkRunnerOptions).spark_repartition_num
            df = self._spark.createDataFrame(self._rules)
            df = df.repartition(repartition_num, df.device_id)
            if action_func:
                df.foreachPartition(foreach_rule.foreach_rules)
            return pvalue.PDone(p_begin.pipeline,
                                element_type=DataFrame,
                                is_bounded=True)
        else:
            df = pd.DataFrame(self._rules)
            return pvalue.PCollection(p_begin.pipeline,
                                      element_value=df,
                                      element_type=pd.DataFrame,
                                      is_bounded=True)


class Console(PTransform):

    def __init__(self,
                 console,  # type: ronds.Console
                 ):
        super(Console, self).__init__()
        self._mode = console.mode

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        df = input_inputs.element_value
        assert isinstance(df, pd.DataFrame)
        print(df.head(10))
        return pvalue.PDone(input_inputs.pipeline,
                            element_type=pd.DataFrame,
                            is_bounded=True)


class Algorithm(PTransform):

    def __init__(self,
                 algorithm,  # type: ronds.Algorithm
                 options,  # type: PipelineOptions
                 ):
        super(Algorithm, self).__init__()
        self._options = options.view_as(AlgorithmOptions) if options is not None \
            else AlgorithmOptions()
        self.path = algorithm.path if algorithm.path \
            else self._options.algorithm_path
        self.func_name = algorithm.func_name if algorithm.func_name \
            else self._options.algorithm_funcname
        # directory of RondsSpark/ronds_sdk/transforms/pandas
        self._base_dir = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))

        # load algorithm as module by path
        self._algorithm_func = self.__load_alg()

    @staticmethod
    def is_absolute(path: str) -> bool:
        p_obj = Path(path)
        return p_obj.is_absolute()

    @property
    def algorithm_func(self):
        return self._algorithm_func

    def __load_alg(self):
        """load algorithm by file path"""

        # load new algorithm func
        alg_absolute_path = self.path if self.is_absolute(self.path) \
            else '%s/%s' % (self._base_dir, self.path)
        if alg_absolute_path not in sys.path:
            sys.path.append(alg_absolute_path)
        func_paths = self.func_name.split('.')
        if len(func_paths) <= 1:
            raise error.TransformError("""algorithm func path expect the format: file.function_name, 
                                          but found: %s""" % self.func_name)
        model_path = '.'.join(func_paths[0:-1])
        func_name = func_paths[-1]
        alg_model = importlib.import_module(model_path)
        alg_func = getattr(alg_model, func_name)
        if alg_func is None:
            raise error.TransformError("""failed load algorithm """)
        return alg_func

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        assert isinstance(input_inputs.element_value, pd.DataFrame)
        df_dict = input_inputs.element_value.to_dict('records')
        res_df_list = list()
        for row in df_dict:
            res_row = self.algorithm_func(row)
            if isinstance(res_row, dict):
                res_df_list.append(res_row)
            elif isinstance(res_row, str):
                res_df_list.append(json.loads(res_row))
            else:
                raise error.TransformError('unexpected algorithm func return type: %s, value: %s'
                                           % (type(res_row), res_row))
        df = pd.DataFrame(res_df_list)
        assert isinstance(df, pd.DataFrame)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_value=df,
                                  element_type=pd.DataFrame,
                                  is_bounded=True)
