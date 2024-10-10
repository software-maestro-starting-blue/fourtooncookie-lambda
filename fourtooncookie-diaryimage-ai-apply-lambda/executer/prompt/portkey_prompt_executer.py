from executer.prompt.prompt_executer import PromptExecuter
from llm.portkey_llm_service import PortkeyLLMService

class PortkeyPromptExecuter(PromptExecuter):

    __portkey_llm_service: PortkeyLLMService
    __prompt_id: str

    def __init__(self, portkey_llm_service: PortkeyLLMService, prompt_id: str):
        self.__portkey_llm_service = portkey_llm_service
        self.__prompt_id = prompt_id
    
    def execute(self, variables: dict) -> str:
        return self.__portkey_llm_service.get_llm_using_portkey(self.__prompt_id, variables)

    def validate_variables(self, variables) -> bool:
        return isinstance(variables, dict)