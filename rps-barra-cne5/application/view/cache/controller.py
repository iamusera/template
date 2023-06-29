import json
import os.path
import time
from datetime import datetime
from typing import Optional

from clickhouse_connect.driver import ProgrammingError

from application.common.utils import shard
from models import get_tables, BaseModel
from models.base.model_enum import ModelEnum
from loguru import logger


def trans_ora_2_ck(tables: Optional[list],
                   start: Optional[str],
                   end: Optional[str]) -> bool:
    """
    读取指定Oracle数据缓存到clickhouse
    """

    return True


def init_table():
    tables = get_tables()
    for model_clas in tables.values():
        model_obj: BaseModel = model_clas()
        model_obj.create()
        logger.info("创建缓存表：{}", model_obj.table_name)


def recreate_table(table_list: list):
    tables = get_tables()
    for model_clas in tables.values():
        if isinstance(model_clas, type) and issubclass(model_clas, BaseModel):
            if not table_list or model_clas.table_name in table_list:
                model_obj: BaseModel = model_clas()
                model_obj.drop()
                model_obj.create()
                logger.info("重建缓存表：{}", model_obj.table_name)


def load_cache(tables: Optional[list], start: Optional[str], end: str, append: bool = False):
    return _load_cache(tables, start, end, append)


def _load_cache(tables: Optional[list], start: Optional[str], end: str, append: bool = False):
    """
    增量更新缓存
    :param tables 为空时代表所有
    :param start 开始日期 %Y%m%d，全量模式忽略此参数
    :param end 结束日期 %Y%m%d
    :param append 增量模式，默认False
    """
    # 初始化参数
    if tables is None:
        tables = []
    table_dict = get_tables()
    table_list = table_dict.items()
    # table_list = table_list if len(tables) == 0 else filter(lambda item: item[0] in tables, table_dict.items())

    result_list = list()
    for (table_name, model_cls) in table_list:
        if len(tables) != 0 and table_name not in tables:
            continue

        if isinstance(model_cls, type) and issubclass(model_cls, BaseModel):
            model_obj: BaseModel = model_cls()
            row_count = 0
            timer = dict()
            time_start = time.time()
            try:
                if append:
                    logger.info("开始处理缓存表增量数据：{} {} {} ============", model_obj.table_name, start, end)
                    if model_obj.model_type == ModelEnum.BASE_INFO:
                        df_result = model_obj.query_db(None, None)
                    else:
                        df_result = model_obj.query_db(start, end)

                else:
                    logger.info("开始处理缓存表全量数据：{} {} ============", model_obj.table_name, end)
                    start_default = model_obj.start
                    if start_default:
                        df_result = model_obj.query_db(start_default, end)
                    elif model_obj.model_type == ModelEnum.MARKET_DATA:
                        df_result = model_obj.query_db("20060101", end)
                    elif model_obj.model_type == ModelEnum.FINA_REPORT:
                        df_result = model_obj.query_db("20030101", end)
                    else:
                        df_result = model_obj.query_db(None, None)

                row_count = df_result.shape[0]
                timer['time_query_db'] = round(time.time() - time_start, 4)
                time_start = time.time()
                if append:
                    logger.info("==删除缓存表数据{}条：{}  ", row_count, model_obj.table_name)
                    model_obj.delete(start, end)
                else:
                    logger.info("==清空缓存表：{}", model_obj.table_name)
                    model_obj.truncate()
                timer['time_delete_ck'] = round(time.time() - time_start, 4)
                time_start = time.time()
                if df_result is not None:
                    if not df_result.empty:
                        logger.info("==存入缓存表{}条：{}", row_count, model_obj.table_name)
                        model_obj.insert_df(df_result)
                timer['time_insert_ck'] = round(time.time() - time_start, 4)
                result = {
                    "table_name": table_name,
                    "success": True,
                    "row_count": row_count
                }
                result_list.append(result.update(timer))
                logger.info("==处理结果：{}", result)
                yield result
                # ****************** 存入文件，测试用
                save2csv(append, df_result, end, table_name)

            except Exception as e:
                logger.error(f"存入缓存表{table_name}失败", e)
                logger.exception(e)
                result = {
                    "table_name": table_name,
                    "success": False,
                    "row_count": row_count
                }
                result_list.append(result.update(timer))
                logger.error("==处理失败结果：{}", result)
                yield result

    logger.info("执行完成结果：{}", json.dumps(result_list))


def save2csv(append, df_result, end, table_name):
    """
    存入文件，测试用
    :param append:
    :param df_result:
    :param end:
    :param table_name:
    """
    base_path = "/opt/test/barra/"
    if os.path.isdir(base_path):
        if append:
            path = base_path + "append/" + end + "/"
        else:
            path = base_path + "all/" + end + "/"
        os.makedirs(path, exist_ok=True)

        file = path + table_name + ".csv"
        logger.info(f"准备保存到文件：{file}")
        df_result.to_csv(file)


def init_cache(table_list: list):
    # 初始化参数
    today = datetime.today().strftime('%Y%m%d')
    return [res for res in _load_cache(table_list, None, today)]


def increase_cache(tables: Optional[list], start: Optional[str], end: str):
    """
    增量更新缓存
    :return:
    """
    return [res for res in _load_cache(tables, start, end, True)]


def init_cache_shard(curr: int, total: int):
    table_dict = get_tables()
    table_list = list(table_dict.keys())
    logger.info("总任务序列：{}", table_list)
    task_list = shard.get_curr_shard(table_list, curr, total)
    logger.info("当前子任务序列：{}", task_list)

    today = datetime.today().strftime('%Y%m%d')
    return [res for res in _load_cache(task_list, None, today)]


def query_cache(tables: Optional[list], start: Optional[str], end: str):
    """
    增量更新缓存
    :param tables 为空时代表所有
    :param start 开始日期 %Y%m%d，全量模式忽略此参数
    :param end 结束日期 %Y%m%d
    :param append 增量模式，默认False
    """

    # 初始化参数
    if tables is None:
        tables = []
    table_dict = get_tables()
    table_list = table_dict.items()
    table_list = table_list if len(tables) == 0 else filter(lambda item: item[0] in tables, table_dict.items())

    for (table_name, model_cls) in table_list:
        if isinstance(model_cls, type) and issubclass(model_cls, BaseModel):
            model_obj: BaseModel = model_cls()
            logger.info(f"==开始查询数据：{table_name} {start} {end}")
            time_start = time.time()
            df = model_obj.query_df(start, end)
            timer = time.time() - time_start
            logger.info(f"查询数据：{table_name}, 数量: {df.shape}, 时长：{timer}")
