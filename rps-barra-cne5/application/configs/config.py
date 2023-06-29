#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-03-06 16:22
    @description: 
"""
from application.common.utils import load_yaml


class Config:

    @staticmethod
    def load_cfg(cfg_path):
        config, cfg = load_yaml(f'{cfg_path}.yaml')
        return config


class Dev(Config):
    ...


class Prod(Config):
    ...


class Sit(Config):
    # @staticmethod
    # def load_cfg(cfg_path):
    #     config, cfg = load_yaml(f'{cfg_path}.yaml')
    #     db_cfg = cfg["base"]["rps_db"]
    #     config['SQLALCHEMY_BINDS'] = {
    #         "rps_db": 'oracle://{username}:{password}@{host}:{port}/{schema}'.format(**db_cfg)
    #     }
    #
    #     return config
    pass


config = {
    'dev': Dev,
    'sit': Sit,
    'prod': Prod
}


def get_cfg(env='dev'):
    cls = config.get(env)
    cfg = cls.load_cfg(env)
    return cfg
