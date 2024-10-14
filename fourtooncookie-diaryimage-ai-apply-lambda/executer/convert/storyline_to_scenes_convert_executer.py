import re

from executer.convert.convert_executer import ConvertExecuter

class StorylineToScenesConvertExecuter(ConvertExecuter):

    def execute(self, variables: str) -> list[str]:
        pattern = r"기:\s*(.*?)\s*승:\s*(.*?)\s*전:\s*(.*?)\s*결:\s*(.*)"

        # 패턴에 맞는 부분 추출
        match = re.search(pattern, variables, re.DOTALL)

        return [
            match.group(i) for i in range(1, 5)
        ]
    

    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)