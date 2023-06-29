import queue
import time
import clickhouse_driver as ch


class Connection:
    """包含连接对象和相关信息的类"""

    def __init__(self, conn, created_at=None):
        self.conn = conn
        self.created_at = created_at or time.time()

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.created_at = time.time()


class ConnectionPool:
    """用于管理ClickHouse连接池的类"""

    _instance = None

    def __new__(cls, uri, max_pool_size=10, max_idle_seconds=30, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, uri, max_pool_size=10, max_idle_seconds=30, **kwargs):
        if self.__initialized:
            return
        self.__initialized = True

        self.uri = uri
        self.max_pool_size = max_pool_size
        self.max_idle_seconds = max_idle_seconds
        self.connections = queue.Queue(maxsize=max_pool_size)

        self._initialize_connection_pool()

    def _initialize_connection_pool(self):
        for i in range(self.max_pool_size):
            conn = self._create_connection()
            self.connections.put(Connection(conn))

    def _create_connection(self):
        return ch.connect(self.uri)

    def _replenish_connection_pool(self):
        if self.connections.qsize() < self.max_pool_size:
            conn = self._create_connection()
            self.connections.put(Connection(conn))

    def acquire(self):
        """获取连接池中的连接"""
        try:
            while True:
                connection = self.connections.get_nowait()
                if time.time() - connection.created_at < self.max_idle_seconds:
                    return connection
                else:
                    connection.conn.disconnect()
        except queue.Empty:
            self._replenish_connection_pool()
            connection = self.connections.get(block=True)
            return connection

    def release(self, connection):
        """将连接返还连接池"""
        self.connections.put(connection)

    def close(self):
        """关闭所有连接并清空连接池"""
        while not self.connections.empty():
            connection = self.connections.get()
            connection.conn.disconnect()
        del self._instance
        self.__initialized = False
