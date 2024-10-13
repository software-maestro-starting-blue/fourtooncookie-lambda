from visionrequest.vision_request_service import VisionRequestService

import boto3
import json

class SQSStableDiffusionVisionRequestService(VisionRequestService):

    __sqs: boto3.client
    __queue_url: str

    def __init__(self, sqsclient: boto3.client, queue_url: str):
        self.__sqs = sqsclient
        self.__queue_url = queue_url

    def request_vision(self, diary_id: int, character_id: int, character_base_prompt: str, scenes: list[str]):
        for i, scene_words in enumerate(scenes):
            
            self.__sqs.send_message(
                QueueUrl=self.__queue_url,
                MessageBody=json.dumps({
                    'diaryId': diary_id,
                    'characterId': character_id,
                    'prompt': character_base_prompt + ', ' + ", ".join(scene_words),
                    'gridPosition': i
                }),
                MessageGroupId=str(diary_id)
            )