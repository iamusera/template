#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author: iamusera
    @date: 2023-04-21 14:29
    @description: 
"""
from application.grpc_server.request_resolver import cache_request_resolver
from application.grpc_server.request_resolver.base.base_request_resovler import BaseRequestResolver
from application.grpc_server.request_resolver.cache_request_resolver import InitCache

code_mapping = {
    "/cache/init_cache": InitCache
}


def request_resolve(code, json):
    resolver = code_mapping[code]
    if issubclass(resolver, BaseRequestResolver):
        return resolver().execute(json)

