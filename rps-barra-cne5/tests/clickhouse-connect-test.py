import clickhouse_connect
import functools
import time


def timer(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_cost = time.time() - start_time
        print(time_cost)
        return result
    return clocked


def get_client():
    client = clickhouse_connect.get_client(
        host='10.10.3.40', port=18123, username='admin', password='123456', database='my_database'
    )
    return client


@timer
def query_df_test():
    sql = """ select * from ASHAREEODPRICE """
    client = get_client()
    df = client.query_df(sql)
    print(df.shape)


if __name__ == '__main__':
    query_df_test()

