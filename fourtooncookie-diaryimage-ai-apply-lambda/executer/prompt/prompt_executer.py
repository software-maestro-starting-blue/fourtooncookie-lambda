from executer.executer import Executer
from abc import abstractmethod

class PromptExecuter(Executer):

    @abstractmethod
    def execute(self, variables):
        pass

    def validate_variables(self, variables) -> bool:
        return not isinstance(variables, dict) or "default" in variables.keys()