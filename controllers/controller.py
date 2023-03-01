from abc import abstractmethod, ABC
from flask import Flask

class Controller(ABC):
    def __init__(self, app: Flask):
        self._app = app

        self.register_routes()

    @abstractmethod
    def register_routes(self):
        pass
