from abc import ABCMeta, abstractmethod

class Executer(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, variables):
        pass

    @abstractmethod
    def validate_variables(self, variables) -> bool:
        pass