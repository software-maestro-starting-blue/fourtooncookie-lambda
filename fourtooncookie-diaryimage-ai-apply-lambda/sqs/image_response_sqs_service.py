import boto3
import json

class ImageResponseSQSService():

    __sqs: boto3.client
    __queue_url: str

    def __init__(self, sqs, queue_url):
        self.__sqs = sqs
        self.__queue_url = queue_url
    
    def send_image_success_response(self, diary_id: int):
        for grid_position in range(4):
            self.__sqs.send_message(
                QueueUrl=self.__queue_url,
                MessageBody=json.dumps({
                    "diaryId": diary_id,
                    "gridPosition": grid_position,
                    "status": True
                })
            )
    
    def send_image_failure_response(self, diary_id: int):
        for grid_position in range(4):
            self.__sqs.send_message(
                QueueUrl=self.__queue_url,
                MessageBody=json.dumps({
                    "diaryId": diary_id,
                    "gridPosition": grid_position,
                    "status": False
                })
            )