import datetime
import logging
import uuid
from typing import Sequence, List

from cassandra import ProtocolVersion
from cassandra.cluster import Cluster, Session, ResultSet
from ronds_sdk.options.pipeline_options import CassandraOptions


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]


@Singleton
class CassandraManager(object):
    """
    Cassandra 数据库的操作类, 单例
    连接到固定的一个 Cassandra 集群, 可以操作多个 keyspace
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 ):
        self.cluster = Cluster(options.cassandra_host, protocol_version=ProtocolVersion.DSE_V1)
        self.session_cache = dict()  # type: dict[str, Session]

    def get_session(self, keyspace):
        # type: (str) -> Session
        if not self.session_cache.__contains__(keyspace):
            self.session_cache[keyspace] = self.cluster.connect(keyspace)
        return self.session_cache.get(keyspace)

    def query(self, keyspace: str, sql: str, params: List[str]) -> ResultSet:
        result = self.get_session(keyspace).execute(sql, params)
        return result

    def execute(self, keyspace: str, sql: str, params: List[str]) -> None:
        self.get_session(keyspace).execute(sql, params)

    def __del__(self):
        try:
            self.cluster.shutdown()
            logging.info("cassandra cluster shutdown~")
        except Exception as ex:
            logging.error("CassandraManager cluster shutdown failed: %s" % ex)
            raise ex


class ProcessDataManager(object):
    """
    内置的操作工艺数据表的操作类
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 keyspace=None,  # type: str
                 ):
        self._options = options
        self._table_name = options.cassandra_table_process  # type: str
        self.cassandra_manager = CassandraManager(options)  # type: CassandraManager
        if keyspace:
            self.keyspace = keyspace
        elif options.cassandra_keyspace:
            self.keyspace = options.cassandra_keyspace

    @property
    def _get_session(self):
        return self.cassandra_manager.get_session(self.keyspace)

    @property
    def _get_window_select_prepare(self):
        return self._get_session.prepare("""SELECT id, time, value
                                            FROM %s 
                                            where id in ?
                                            AND time > ? 
                                            AND time <= ?""" % self._table_name)

    def window_select(self,
                      uid_list,  # type: Sequence[str],
                      start_time,  # type: datetime.datetime
                      end_time,  # type: datetime.datetime
                      ):
        # type:  (...) -> ResultSet
        uuid_list = [uuid.UUID(uid) for uid in uid_list]
        return self._get_session.execute(self._get_window_select_prepare, [uuid_list, start_time, end_time])
