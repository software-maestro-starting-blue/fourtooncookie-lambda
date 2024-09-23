from llm.llm_service import LLMService
from openai import OpenAI

class GPT4oLLMService(LLMService):

    __open_ai: OpenAI
    __gpt_model: str

    def __init__(self, openai: OpenAI, gpt_model: str = 'gpt-4.0-mini'):
        self.__open_ai = openai
        self.__gpt_model = gpt_model

    def get_llm(self, system_prompt: str, user_prompt: str) -> str:
        response = self.__open_ai.create_completion(
            model=self.__gpt_model, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=20
        )

        return response['choices'][0]['message']['content']