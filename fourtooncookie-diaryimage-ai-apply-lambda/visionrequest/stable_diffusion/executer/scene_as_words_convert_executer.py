from executer.convert.convert_executer import ConvertExecuter

class SceneAsWordsConvertExecuter(ConvertExecuter):
    
    def execute(self, varaibles):
        return varaibles.split(" ")
    
    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)