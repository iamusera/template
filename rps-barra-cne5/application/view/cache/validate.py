from datetime import datetime, timedelta

from application.exception import ParameterException


class Param:
    """
    参数校验
    """

    def __init__(self,
                 tables: list,
                 start: str,
                 end: str):
        self._tables = tables
        self._start = str(start)
        self._end = str(end)

    @property
    def tables(self):
        if not self._tables:
            return []
        return self._tables

    @property
    def start(self):
        if not self._start:
            return (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
        return self._start

    @property
    def end(self):
        if not self._end:
            return datetime.today().strftime('%Y%m%d')
        return self._end


class ShardParam:
    """
    参数校验
    """

    def __init__(self,
                 curr: int,
                 total: int):
        self._curr = curr
        self._total = total

    @property
    def curr(self):
        if not self._curr:
            return 1
        if self._curr < 1:
            raise ParameterException('curr不能小于1')
        return self._curr

    @property
    def total(self):
        if not self._total:
            return 1
        if self._total < 1:
            raise ParameterException('total不能小于1')
        if self._total <= self._curr:
            raise ParameterException('total不能小于curr')
        return self._total
