from executer.convert.convert_executer import ConvertExecuter
import json

class StringToJsonConvertExecuter(ConvertExecuter):

    def execute(self, variables: str):
        return json.loads(variables)

    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)