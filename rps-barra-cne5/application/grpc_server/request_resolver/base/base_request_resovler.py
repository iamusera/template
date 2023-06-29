from abc import ABC, abstractmethod


class BaseRequestResolver(ABC):

    @abstractmethod
    def execute(self, json: str):
        ...