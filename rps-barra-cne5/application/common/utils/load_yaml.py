import os
import codecs
import yaml
import logging

from urllib import parse

from application.common.utils.encrypt import decrypt


def load_yaml(path):
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    path = os.path.join(ROOT_PATH, 'etc', path)
    with codecs.open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        db_cfg = cfg["base"]["wind_db"]
        config = {}
        # 数据库用户名和密码解密
        ext = cfg.get("extra")
        if ext:
            if "db_security_key" in cfg.get("extra"):
                key = cfg["extra"]["db_security_key"]
                if key is not None:
                    user_name = decrypt(cfg["base"]["wind_db"]["username"], key)
                    password = decrypt(cfg["base"]["wind_db"]["password"], key)
                    cfg["base"]["wind_db"]["username"] = parse.quote_plus(user_name)
                    cfg["base"]["wind_db"]["password"] = parse.quote_plus(password)
        config['SQLALCHEMY_DATABASE_URI'] = "oracle://{username}:{password}@{host}:{port}/{schema}".format(**db_cfg)

        config['SQLALCHEMY_ECHO'] = db_cfg["echo"]
        config['SQLALCHEMY_POOL_SIZE'] = db_cfg["pool_size"]
        config['SQLALCHEMY_MAX_OVERFLOW'] = db_cfg["max_overflow"]
        config['SQLALCHEMY_POOL_RECYCLE'] = db_cfg["pool_recycle"]
        config['SQLALCHEMY_POOL_TIMEOUT'] = db_cfg["pool_timeout"]
        config['SQLALCHEMY_TRACK_MODIFICATIONS'] = db_cfg["modify"]

        # 多数据库
        rps_db_cfg = cfg["base"]["rps_db"]
        config['SQLALCHEMY_BINDS'] = {
            "rps_db": 'oracle://{username}:{password}@{host}:{port}/{schema}'.format(**rps_db_cfg)
        }

        # 默认日志等级
        config['LOG_LEVEL'] = logging.INFO
        config['INFO_LOG'] = cfg.get('log').get('info')
        config['ERROR_LOG'] = cfg.get('log').get('error')

        # celery配置
        config['CELERY_BROKER_URL'] = cfg["base"]["redis"]["broker"]
        config['CELERY_RESULT_BACKEND'] = cfg["base"]["redis"]["broker"]
        config['CELERY_TIMEZONE'] = cfg["base"]["redis"]["timezone"]
        config['CELERY_IMPORTS'] = ['application.view.predict_mod.controller']

        # grpc
        config['RPC_HOST'] = cfg['base']['grpc']['host']
        config['RPC_PORT'] = cfg['base']['grpc']['port']
        config['RPC_WORKER'] = cfg['base']['grpc']['worker']

        # clickhouse
        ck = cfg["base"]["clickhouse"]
        config['CK_HOST'] = ck['host']
        config['CK_PORT'] = ck['port']
        config['CK_DATABASE'] = ck['schema']
        config['CK_USER'] = ck['username']
        config['CK_PASSWD'] = ck['password']

        return config, cfg
