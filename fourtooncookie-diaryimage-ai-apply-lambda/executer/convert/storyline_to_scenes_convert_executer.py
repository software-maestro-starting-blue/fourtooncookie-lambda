import re

from executer.convert.convert_executer import ConvertExecuter

class StorylineToScenesConvertExecuter(ConvertExecuter):

    def execute(self, variables: str) -> list[str]:
        pattern = r"Introduction:\s*(.*?)\n*Development:\s*(.*?)\n*Turn:\s*(.*?)\n*Conclusion:\s*(.*)"

        # 패턴에 맞는 부분 추출
        match = re.search(pattern, variables, re.DOTALL)

        return [
            match.group(i) for i in range(1, 5)
        ]
    

    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)