import clickhouse_connect
from flask import current_app
from clickhouse_connect.datatypes.format import set_read_format

def ck_client():
    client = clickhouse_connect.get_client(
        host=current_app.config['CK_HOST'],
        port=current_app.config['CK_PORT'],
        username=current_app.config['CK_USER'],
        password=current_app.config['CK_PASSWD'],
        database=current_app.config['CK_DATABASE'],
    settings={"connect_timeout": 10, "receive_timeout": 3000, "send_timeout": 3000}
    )
    set_read_format('FixedString', 'string')
    client.ping()
    return client
