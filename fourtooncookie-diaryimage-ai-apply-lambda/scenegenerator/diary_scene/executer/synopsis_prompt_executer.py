from executer.prompt_executer import PromptExecuter
from llm.llm_service import LLMService
import json

SYNOPSIS_PROMPT: str = ""
SYNOPSIS_PROMPT_FILE_PATH = './prompt/synopsis_prompt.txt'

with open(SYNOPSIS_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    SYNOPSIS_PROMPT = f.read()


class SynopsisPromptExecuter(PromptExecuter):

    __llm_service: LLMService

    def __init__(self, llm_service: LLMService):
        self.__llm_service = llm_service
    
    def execute(self, variables: str):
        result = self.__llm_service.get_llm(SYNOPSIS_PROMPT, variables)
        data = json.loads(result)
        return data
    
    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)

