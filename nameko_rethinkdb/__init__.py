from collections import namedtuple
from weakref import WeakKeyDictionary

import rethinkdb as r
from nameko.extensions import DependencyProvider


class RethinkDBWrapper(namedtuple('RethinkDB', 'connection table')):
    def create_index(self, name, *args, **kwargs):
        _conn = self.connection
        _table = self.table
        if name not in _table.index_list().run(_conn):
            _table.index_create(name, *args, **kwargs).run(_conn)
            _table.index_wait(name).run(_conn)
        return True


class RethinkDB(DependencyProvider):
    def __init__(self, db_name, table_name, alias=None, primary_key='uuid', wrapper_callbacks=None):
        self.rdb_connections = WeakKeyDictionary()
        self.db = db_name
        self.table = table_name
        self.alias = alias
        self.primary_key = primary_key or 'uuid'
        self.wrapper_callbacks = list(wrapper_callbacks or [])

    # def setup(self):
    #     service_name = self.container.service_name
    #     rdb_config = self.container.config[RDB_KEY][service_name]
    #
    #     self.RDB_HOST = rdb_config['RDB_HOST']
    #     self.RDB_PORT = rdb_config['RDB_PORT']
    #     self.RDB_DB = self.db

    def get_dependency(self, worker_ctx):
        _alias = self._get_alias(worker_ctx)

        connection = self.rdb_connections.get(_alias, None)
        if connection is None:
            connection = r.connect(host='rethinkdb', port=28015)
            self.rdb_connections[_alias] = connection

        _db = self._check_db(connection)
        _table = self._check_table(_db, connection)
        _wrapper = RethinkDBWrapper(*(connection, _table))
        map(lambda x: x(_wrapper), filter(callable, self.wrapper_callbacks))
        return _wrapper

    def _check_db(self, connection):
        if self.db not in r.db_list().run(connection):
            r.db_create(self.db).run(connection)
        return r.db(self.db)

    def _check_table(self, db, connection):
        if self.table not in db.table_list().run(connection):
            db.table_create(self.table, primary_key=self.primary_key).run(connection)
        return db.table(self.table)

    def _get_alias(self, worker_ctx):
        return self.alias or worker_ctx

    def worker_teardown(self, worker_ctx):
        _alias = self._get_alias(worker_ctx)

        connection = self.rdb_connections.pop(_alias, None)
        try:
            connection.close()
        except AttributeError:  # pragma: no cover
            pass