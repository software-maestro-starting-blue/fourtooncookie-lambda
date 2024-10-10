from executer.executer import Executer
from abc import abstractmethod

class ConvertExecuter(Executer):

    @abstractmethod
    def execute(self, variables):
        pass

    @abstractmethod
    def validate_variables(self, variables) -> bool:
        pass