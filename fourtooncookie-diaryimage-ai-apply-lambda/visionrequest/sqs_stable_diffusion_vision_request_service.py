from visionrequest.vision_request_service import VisionRequestService
from llm.llm_service import LLMService
from prompt import get_stable_diffusion_modify_prompt

import boto3
import json

class SQSStableDiffusionVisionRequestService(VisionRequestService):

    __sqs: boto3.client
    __queue_url: str
    __llm_service: LLMService

    def __init__(self, sqsclient: boto3.client, queue_url: str, llm_service: LLMService):
        self.__sqs = sqsclient
        self.__queue_url = queue_url
        self.__llm_service = llm_service
    
    def __modify_prompt(self, prompt: str) -> str:
        result = self.__llm_service.get_llm(get_stable_diffusion_modify_prompt(), prompt)
        result_json: dict = json.loads(result)
        return ", ".join(result_json.values())

    def request_vision(self, diary_id: int, character_id: int, character_base_prompt: str, prompts: list[str]):
        for i, prompt in enumerate(prompts):
            modified_prompt = self.__modify_prompt(prompt)

            self.__sqs.send_message(
                QueueUrl=self.__queue_url,
                MessageBody=json.dumps({
                    'diaryId': diary_id,
                    'characterId': character_id,
                    'prompt': character_base_prompt + ', ' + modified_prompt,
                    'gridPosition': i
                })
            )