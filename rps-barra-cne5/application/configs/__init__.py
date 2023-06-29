from .config import get_cfg
# import logging
# import os
# from urllib import parse
# from application.common.utils import load_yaml, decrypt
# from application.configs.dev_config import DevelopmentConfig
# from application.configs.prod_config import ProductionConfig
# from application.configs.test_config import TestConfig
# 
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestConfig,
#     'production': ProductionConfig
# }
# 
# class Config:
#     ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
#     etc_path = os.path.join(ROOT_PATH, 'etc', 'dev.yaml')
#     cfg = load_yaml(etc_path)
# 
#     db_cfg = cfg["base"]["database"]
# 
#     # 数据库用户名和密码解密
#     ext = cfg.get("extra")
#     if ext:
#         if "db_security_key" in cfg.get("extra"):
#             key = cfg["extra"]["db_security_key"]
#             if key is not None:
#                 user_name = decrypt(cfg["base"]["database"]["username"], key)
#                 password = decrypt(cfg["base"]["database"]["password"], key)
#                 cfg["base"]["database"]["username"] = parse.quote_plus(user_name)
#                 cfg["base"]["database"]["password"] = parse.quote_plus(password)
#     # 数据库配置
#     # SQLALCHEMY_DATABASE_URI = "oracle://{username}:{password}@{host}:{port}/{service}".format(**db_cfg)
#     # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{service}".format(**db_cfg)
#     SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{username}:{password}@{host}:{port}/{schema}?charset=utf8".format(**db_cfg)
#     SQLALCHEMY_ECHO = db_cfg["echo"]
#     SQLALCHEMY_POOL_SIZE = db_cfg["pool_size"]
#     SQLALCHEMY_MAX_OVERFLOW = db_cfg["max_overflow"]
#     SQLALCHEMY_POOL_RECYCLE = db_cfg["pool_recycle"]
#     SQLALCHEMY_POOL_TIMEOUT = db_cfg["pool_timeout"]
#     SQLALCHEMY_TRACK_MODIFICATIONS = db_cfg["modify"]
# 
#     # 默认日志等级
#     LOG_LEVEL = logging.INFO
#     INFO_LOG = cfg.get('log').get('info')
#     ERROR_LOG = cfg.get('log').get('error')
# 
#     # celery配置
#     CELERY_BROKER_URL = cfg["base"]["redis"]["broker"]
#     CELERY_RESULT_BACKEND = cfg["base"]["redis"]["broker"]
#     CELERY_TIMEZONE = cfg["base"]["redis"]["timezone"]
    # CELERY_IMPORTS = ['application.view.predict_mod.controller']