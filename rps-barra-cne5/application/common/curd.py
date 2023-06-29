#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 13:05
    @description: 
"""
from application.extensions import db


def get_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    return model.query.filter_by(id=id).first()


def get_filed_by_id(model: db.Model, id, field):
    return get_one_by_id(model, id).as_dict().get(field)


def update_one_by_id(model: db.Model, id, state, msg=None):
    """
    更新一条数据的状态
    :param model: 
    :param id: 
    :param state: 出错情况下写入错误信息
    :return: 
    """
    r = get_one_by_id(model, id)
    r.state = state
    if msg:
        r.err_msg = msg
    db.session.commit()


def insert_data(model, data):
    """
    插入数据
    """
    db.session.execute(model.__table__.insert(), data)
    db.session.commit()
