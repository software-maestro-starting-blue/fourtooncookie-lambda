from executer.executer import Executer

class BatchExecuter(Executer):

    __executer: Executer

    def __init__(self, executer: Executer):
        self.__executer = executer

    def execute(self, variables: list):
        return [
            self.__executer.execute(variable)
            for variable in variables
        ]
    
    def validate_variables(self, variables) -> bool:
        if not isinstance(variables, list):
            return False

        return all([
            self.__executer.validate_variables(variable)
            for variable in variables
        ])