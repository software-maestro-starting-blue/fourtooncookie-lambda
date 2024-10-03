from visionrequest.vision_request_service import VisionRequestService
from visionrequest.stable_diffusion.executer.scene_as_words_convert_executer import SceneAsWordsConvertExecuter

import boto3
import json

class SQSStableDiffusionVisionRequestService(VisionRequestService):

    __sqs: boto3.client
    __queue_url: str
    __scene_as_words_convert_executer: SceneAsWordsConvertExecuter

    def __init__(self, sqsclient: boto3.client, queue_url: str, scene_as_words_convert_executer: SceneAsWordsConvertExecuter):
        self.__sqs = sqsclient
        self.__queue_url = queue_url
        self.__scene_as_words_convert_executer = scene_as_words_convert_executer

    def request_vision(self, diary_id: int, character_id: int, character_base_prompt: str, scenes: list[str]):
        for i, scene in enumerate(scenes):
            scene_words = self.__scene_as_words_convert_executer.execute(scene)
            
            self.__sqs.send_message(
                QueueUrl=self.__queue_url,
                MessageBody=json.dumps({
                    'diaryId': diary_id,
                    'characterId': character_id,
                    'prompt': character_base_prompt + ', ' + ", ".join(scene_words),
                    'gridPosition': i
                })
            )