import re
import logging
import threading
from enum import Enum
from typing import Sequence
from jinja2 import Template
from functools import lru_cache

LIMIT_1 = 1
_REGEX = r':[\w|\d]*'
DYNAMIC_REGEX = '{%|{{|}}|%}'
DB_LOCK = threading.RLock()


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Sequence) else args


def try_commit(db_ctx):
    if db_ctx.transactions == 0:
        logging.debug('Commit transaction...')
        try:
            db_ctx.connection.commit()
            logging.debug('Commit ok.')
        except Exception:
            logging.warning('Commit failed, try rollback...')
            db_ctx.connection.rollback()
            logging.warning('Rollback ok.')
            raise


def simple_sql(sql: str, *args, **kwargs):
    return get_named_sql_args(sql, **kwargs) if kwargs else (sql, args)


def dynamic_sql(sql: str, *args, **kwargs):
    if kwargs:
        if _is_dynamic_sql(sql):
            sql = Template(sql).render(**kwargs)
        return get_named_sql_args(sql, **kwargs)

    return sql, args


def is_dynamic_sql(sql: str):
    return re.search(DYNAMIC_REGEX, sql)


@lru_cache(maxsize=128)
def _is_dynamic_sql(sql: str):
    return True if is_dynamic_sql(sql) else False


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


@lru_cache(maxsize=256)
def get_named_sql(sql: str):
    return re.sub(_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(_REGEX, sql)]


def log(function: str, sql: str, *args, **kwargs):
    logging.debug("Exec func 'mysqlx.%s' \n\t\tsql: %s \n\t\targs: %s \n\t\tkwargs: %s" % (function, sql.strip(), args, kwargs))


def page_log(function: str, sql: str, page_num, page_size, *args, **kwargs):
    logging.debug("Exec func 'mysqlx.%s', page_num: %d, page_size: %d \n\t\tsql: %s \n\t\targs: %s \n\t\tkwargs: %s" % (
        function, page_num, page_size, sql.strip(), args, kwargs))


class DBCtx(threading.local):
    """
    Thread local object that holds connection info.
    """

    def __init__(self, connect, use_mysql_connector):
        self.connect = connect
        self.connection = None
        self.transactions = 0
        self.prepared = True
        if use_mysql_connector:
            self.get_cursor = lambda: self.connection.cursor(prepared=self.prepared)
            self.log = lambda action: logging.debug('%s connection <%s>...' % (action, hex(id(self.connection._cnx))))
        else:
            self.get_cursor = lambda: self.connection.cursor()
            self.log = lambda action: logging.debug('%s connection <%s>...' % (action, hex(id(self.connection))))

    def is_not_init(self):
        return self.connection is None

    def init(self):
        self.transactions = 0
        self.connection = self.connect()
        self.log('Use')

    def release(self):
        if self.connection:
            self.log('Release')
            self.connection.close()
            self.connection = None

    def cursor(self):
        """
        Return cursor
        """
        # logging.debug('Cursor prepared: %s' % self.prepared)
        return self.get_cursor()

    def statement(self, sql: str):
        """
        Return statement
        """
        return self.connection.statement(sql)


class ConnectionCtx(object):
    """
    ConnectionCtx object that can open and close connection context. ConnectionCtx object can be nested and only the most
    outer connection has effect.
    with connection():
        pass
        with connection():
            pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_cleanup = False
        if self.db_ctx.is_not_init():
            self.db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.should_cleanup:
            self.db_ctx.release()


class TransactionCtx(object):
    """
    TransactionCtx object that can handle transactions.
    with TransactionCtx():
        pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_close_conn = False
        if self.db_ctx.is_not_init():
            # needs open a connection first:
            self.db_ctx.init()
            self.should_close_conn = True
        self.db_ctx.transactions += 1
        logging.debug('Begin transaction...' if self.db_ctx.transactions == 1 else 'Join current transaction...')
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self.db_ctx.transactions -= 1
        try:
            if self.db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                self.db_ctx.release()

    def commit(self):
        try_commit(self.db_ctx)

    def rollback(self):
        logging.warning('Rollback transaction...')
        self.db_ctx.connection.rollback()
        logging.debug('Rollback ok.')


class DBError(Exception):
    pass


class MapperError(DBError):
    pass


class MultiColumnsError(DBError):
    pass


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class SqlModel:
    from typing import List
    def __init__(self, sql: str, action: str, namespace: str, dynamic=False, includes: List[str] = None):
        self.sql = sql
        self.action = action
        self.namespace = namespace
        self.dynamic = dynamic
        self.includes = includes
        self.mapping = True if dynamic else ':' in sql
        self.placeholder = False if self.mapping else '?' in sql


class SqlAction(Enum):
    CALL = 'call'
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
    SELECT = 'select'


class PkStrategy(Enum):
    """
    DB: 由数据库的AUTO_INCREMENT自动生成主键
    SNOWFLAKE: 由Snowflake算法生成主键

    在Windows上，使用Snowflake可能会报下列错误，这是因为Snowflake生成的id是15位的数字，而Windows上C语言的long类型是32位的
    OverflowError: Python int too large to convert to C long

    如果用的是mysql.connector，且在Windows上开发测试，可以就在初始化数据库的时候加上参数'use_pure'为True用纯python的connect; 在linux是部署生成环境时去掉'use_pure'用
    C语言写的connect, 以提高性能.
    """
    DB = 'db'
    SNOWFLAKE = 'snowflake'
