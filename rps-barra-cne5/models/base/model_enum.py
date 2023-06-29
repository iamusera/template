from enum import Enum


class ModelEnum(Enum):
    """
    模型枚举，针对对缓存数据特性分类指定枚举
    """
    # 行情数据，日期条件为交易日
    MARKET_DATA = 1
    # 财报数据，日期条件为报告期，一般3个月一次
    FINA_REPORT = 2
    # 基本信息，一般没有日期条件，每次获取全量数据，不做增量处理
    BASE_INFO = 3
