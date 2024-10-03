from executer.prompt_executer import PromptExecuter
from llm.llm_service import LLMService

class RefineScenePromptExecuter(PromptExecuter):

    __llm_service: LLMService

    def __init__(self, llm_service: LLMService):
        self.__llm_service = llm_service

    def execute(self, variables: dict):
        return self.__llm_service.get_llm(REFINE_SCENE_PROMPT, variables)
    
    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)


REFINE_SCENE_PROMPT: str = ""
REFINE_SCENE_PROMPT_FILE_PATH = '../../prompt/refine_scene_prompt.txt'

with open(REFINE_SCENE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    REFINE_SCENE_PROMPT = f.read()