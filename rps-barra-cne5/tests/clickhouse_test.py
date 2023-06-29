# 以下是使用 ClickHouse 的 JDBC 连接器和 Oracle 的 JDBC 驱动程序将查询结果直接加载到 ClickHouse 表中的 Python示例代码：
import jaydebeapi

# 连接 ClickHouse
clickhouse_conn = jaydebeapi.connect('ru.yandex.clickhouse.ClickHouseDriver',
                                     'jdbc:clickhouse://10.10.3.40:18123/my_database',
                                     {'user': 'admin', 'password': 123456},
                                     'D:\\Users\\tjxm\Desktop\\code\\rps-barra-cne5\\lib\\clickhouse-jdbc-0.4.5-all.jar')

# 连接 Oracle
oracle_conn = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver',
                                 'jdbc:oracle:thin:@//10.10.3.34:1521/orcl',
                                 {'user': 'irs', 'password': 'irs_2021'},
                                 'D:\\Users\\tjxm\Desktop\\code\\rps-barra-cne5\\lib\\ojdbc8.jar')

# 执行 SELECT 查询
query = """ select s_info_windcode, trade_dt, s_dq_close from wind.AIndexEODPrices a """
cursor = oracle_conn.cursor()
cursor.execute(query)

# 获取结果并将其写入 ClickHouse 表中
clickhouse_cursor = clickhouse_conn.cursor()
clickhouse_cursor.executemany('INSERT INTO ASHAREEODPRICE VALUES (?, ?, ?)', cursor.fetchall())

# 提交事务并关闭连接
clickhouse_conn.commit()
clickhouse_conn.close()

oracle_conn.commit()
oracle_conn.close()