# class SingletonType(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#     def __new__(cls, name, bases, attrs):
#         attrs['__init__'] = cls._singleton_init
#         return super().__new__(cls, name, bases, attrs)
#
#     def _singleton_init(cls, *args, **kwargs):
#         if hasattr(cls, '_initialized'):
#             return
#         cls._initialized = True
#         return super().__init__(*args, **kwargs)
import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
