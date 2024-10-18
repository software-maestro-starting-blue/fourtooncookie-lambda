import re

from executer.convert.convert_executer import ConvertExecuter

class SceneToSDPromptConvertExecuter(ConvertExecuter):

    def execute(self, variables: str) -> str:
        pattern = r'Time:\s*(.*)\nBackground:\s*(.*)\nWeather:\s*(.*)\nAction:\s*(.*)\nExpression:\s*(.*)'

        # 패턴에 맞는 부분 추출
        match = re.search(pattern, variables, re.DOTALL)

        time = match.group(1).strip()
        background = match.group(2).strip()
        weather = match.group(3).strip()
        action = match.group(4).strip()
        expression = match.group(5).strip()


        return "{}, in the {}, {}, {}, {}".format(time, background, weather, action, expression)
    

    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)