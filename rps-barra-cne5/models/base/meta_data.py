from application.common.utils import SingletonType


class MetaData(metaclass=SingletonType):
    """
    对已存储到ck的数据管理
    """
    def __init__(self):
        self._tables = {}

    def add_table(self, key, value):
        setattr(self, key, value)
        self._tables[key] = value

    def add_dict(self, d: dict):
        for (key, value) in d.items():
            setattr(self, key, value)
            self._tables[key] = value

    @property
    def tables(self):
        return self._tables

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError("property '%s' is read-only" % key)
        else:
            self.__dict__[key] = value

    def __delattr__(self, name):
        raise AttributeError(f"{type(self).__name__!r} object attribute {name!r} is read-only")
