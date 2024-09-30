from visionrequest.vision_request_service import VisionRequestService

import boto3
import json

class StableDiffusionVisionRequestService(VisionRequestService):

    __sqs: boto3.client
    __queue_url: str

    def __init__(self, sqsclient: boto3.client, queue_url: str):
        self.__sqs = sqsclient
        self.__queue_url = queue_url

    def request_vision(self, diary_id: int, character_id: int, character_base_prompt: str, prompts: list[str]):
        for i, prompt in enumerate(prompts):
            self.__sqs.send_message(
                QueueUrl=self.__queue_url,
                MessageBody=json.dumps({
                    'diaryId': diary_id,
                    'characterId': character_id,
                    'prompt': character_base_prompt + ' ' + prompt,
                    'gridPosition': i
                })
            )