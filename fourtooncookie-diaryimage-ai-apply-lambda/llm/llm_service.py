from abc import ABCMeta, abstractmethod

class LLMService(metaclass=ABCMeta):

    @abstractmethod
    def get_llm(self, system_prompt: str, user_prompt: str):
        pass