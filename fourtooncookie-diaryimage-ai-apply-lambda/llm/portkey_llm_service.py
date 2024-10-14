from llm.llm_service import LLMService
from portkey_ai import Portkey

class PortkeyLLMService(LLMService):

    __portkey: Portkey
    __gpt_model: str

    def __init__(self, portkey: Portkey, gpt_model: str = 'gpt-4o'):
        self.__portkey = portkey
        self.__gpt_model = gpt_model

    def get_llm(self, system_prompt: str, user_prompt: str) -> str:
        response = self.__portkey.chat.completions.create(
            model=self.__gpt_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=20
        )

        return response.choices[0].message.content
    
    def get_llm_using_portkey(self, prompt_id: str, variables: dict) -> str:
        response = self.__portkey.prompts.completions.create(
            prompt_id=prompt_id,
            variables=variables,
            timeout=20
        )

        return response.choices[0].message.content